"""Quick test for NVIDIA NIM API."""

import asyncio
import os
import sys
import time

# Load .env manually (no dependency needed)
def load_env(path: str):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                v = v.strip('"').strip("'")
                os.environ[k] = v

load_env(os.path.join(os.path.dirname(__file__), ".env"))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from sagatoyai.services.nemotron import nim_service, NIM_MODELS


async def test_model(model_name: str = "nemotron-mini"):
    """Test a single NIM model."""
    print(f"\n{'='*60}")
    print(f"Testing: {model_name} ({NIM_MODELS[model_name]})")
    print(f"{'='*60}")

    # Temporarily switch model
    nim_service.set_model(model_name)
    print(f"Using model ID: {nim_service.model}")
    print(f"API Key configured: {bool(nim_service.api_key)}")
    print(f"Base URL: {nim_service.base_url}")

    prompt = "Hello! I'm a child. Tell me a very short and fun greeting, one sentence."

    start = time.time()
    try:
        result, intent = await nim_service.generate_conversation_response(
            user_input=prompt,
            language="en",
        )
        latency = (time.time() - start) * 1000
        print(f"\nIntent: {intent}")
        print(f"Response: {result}")
        print(f"Latency: {latency:.0f}ms")
        return True
    except Exception as e:
        print(f"\nFAILED: {e}")
        return False


async def main():
    if not nim_service.api_key:
        print("ERROR: No NVIDIA API key configured")
        print("Set NVIDIA_API_KEY or NEMOTRON_API_KEY in backend/.env")
        sys.exit(1)

    available = nim_service.list_available_models()
    print(f"Available models: {len(available)}")
    print(f"Default model: {nim_service.model}")

    # Test with default first, then a couple others
    results = {}

    results["default"] = await test_model("nemotron-mini")

    # Test with a medium model
    results["llama-3.1-8b"] = await test_model("llama-3.1-8b")

    # Test with a Chinese prompt
    print(f"\n{'='*60}")
    print("Testing Chinese Mandarin with nemotron-mini")
    print(f"{'='*60}")
    result_zh, intent_zh = await nim_service.generate_conversation_response(
        user_input="你好，你叫什么名字？",
        language="zh",
    )
    print(f"Intent: {intent_zh}")
    print(f"Response: {result_zh}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for name, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"  {name}: {status}")

    # Test model switching
    print(f"\nModel list: {nim_service.list_available_models()}")
    nim_service.set_model("unknown-model")  # Should log warning, not crash
    print("set_model('unknown-model') handled gracefully")

    print("\nAll tests complete!")


if __name__ == "__main__":
    asyncio.run(main())
