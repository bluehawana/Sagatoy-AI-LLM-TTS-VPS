"""Direct NVIDIA NIM API test — no project dependencies needed."""

import asyncio
import json
import os
import sys
import time
import urllib.request


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

_env_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(_env_path):
    _env_path = os.path.expanduser("~/Sagatoy-LLM-TTS-VPS/backend/.env")
load_env(_env_path)


async def test_nim(model: str = "nvidia/nemotron-mini-4b-instruct", prompt: str = "Hello!"):
    api_base = os.getenv("NEMOTRON_API_BASE", "https://integrate.api.nvidia.com/v1")
    # If .env has full endpoint, use it directly
    if "chat/completions" in api_base:
        url = api_base
    else:
        url = api_base + "/chat/completions"
    api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("NEMOTRON_API_KEY")

    if not api_key:
        print("ERROR: No API key")
        return False

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a friendly AI toy. Be brief and warm."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 200,
        "top_p": 0.9,
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            latency = (time.time() - start) * 1000
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"]
            print(f"Model: {model}")
            print(f"Response: {content}")
            print(f"Latency: {latency:.0f}ms")
            return True
    except Exception as e:
        latency = (time.time() - start) * 1000
        print(f"FAILED after {latency:.0f}ms: {e}")
        return False


async def main():
    print("="*50)
    print("NVIDIA NIM API Test")
    print("="*50)
    api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("NEMOTRON_API_KEY")
    base_url = os.getenv('NEMOTRON_API_BASE', 'https://integrate.api.nvidia.com/v1/chat/completions')
    print(f"Base URL: {base_url}")
    api_status = "YES" if api_key else "NO"
    print(f"API Key configured: {api_status}")
    print(f"Default model: nvidia/nemotron-mini-4b-instruct")

    # Test 1: English
    print("\n[1] English greeting:")
    r1 = await test_nim("nvidia/nemotron-mini-4b-instruct", "Tell me a short fun greeting in one sentence.")
    ok = 1 if r1 else 0

    # Test 2: Chinese
    print("\n[2] Chinese (Mandarin):")
    r2 = await test_nim("nvidia/nemotron-mini-4b-instruct", "你好，你叫什么名字？")
    ok += 1 if r2 else 0

    # Test 3: Swedish
    print("\n[3] Swedish:")
    r3 = await test_nim("nvidia/nemotron-mini-4b-instruct", "Hej! Berätta en kort godnatt-saga.")
    ok += 1 if r3 else 0

    # Test 4: Danish
    print("\n[4] Danish:")
    r4 = await test_nim("nvidia/nemotron-mini-4b-instruct", "Hej! Sig noget sjovt på dansk.")
    ok += 1 if r4 else 0

    models_to_test = [
        ("llama-3.1-70b", "meta/llama-3.1-70b-instruct", "LLama 3.1 70B"),
        ("mistral-nemo", "mistralai/mistral-nemo-12b-instruct-v2", "Mistral Nemo 12B"),
    ]

    for model_key, model_id, label in models_to_test:
        nim_service.set_model(model_key)
        print(f"\n{'='*60}")
        print(f"MODEL: {label} ({model_id})")
        print(f"{'='*60}")

        # Swedish story
        print("\n  [SV] Story (2-3 short sentences):")
        resp_sv, _ = await nim_service.generate_conversation_response(
            "Hej! Berätta en kort godnatt-saga om en liten kanin.", "sv")
        print(f"  {resp_sv[:200]}")

        # Math
        print("\n  [Math] 17 x 24 = ?")
        resp_math, _ = await nim_service.generate_conversation_response(
            "What is 17 times 24?", "en")
        print(f"  {resp_math[:200]}")

        # Danish
        print("\n  [DA] Greeting:")
        resp_da, _ = await nim_service.generate_conversation_response(
            "Hej! Sig noget sjovt på dansk.", "da")
        print(f"  {resp_da[:200]}")

        # Norwegian
        print("\n  [NO] Weather:")
        resp_no, _ = await nim_service.generate_conversation_response(
            "Hva er været i Oslo idag?", "no")
        print(f"  {resp_no[:200]}")

        # Finnish
        print("\n  [FI] Story:")
        resp_fi, _ = await nim_service.generate_conversation_response(
            "Kerro lyhyt tarina kissasta.", "fi")
        print(f"  {resp_fi[:200]}")

        # Math in Chinese
        print("\n  [ZH] Math 100-37:")
        resp_zh, _ = await nim_service.generate_conversation_response(
            "100减去37等于多少？", "zh")
        print(f"  {resp_zh[:200]}")

        # Latency
        start = time.time()
        await nim_service.generate_conversation_response(
            "Hej! Hur är läget?", "sv")
        latency = (time.time() - start) * 1000
        print(f"\n  Latency (SV): {latency:.0f}ms")


if __name__ == "__main__":
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
