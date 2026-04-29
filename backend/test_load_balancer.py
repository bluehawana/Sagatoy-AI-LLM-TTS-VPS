"""Test the full load balancer chain."""
import asyncio
import os
import sys
import time

_base = os.path.dirname(__file__)
_src = os.path.join(_base, "src")
if not os.path.exists(_src):
    _src = os.path.expanduser("~/Sagatoy-LLM-TTS-VPS/backend/src")
sys.path.insert(0, _src)

def load_env(path: str):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ[k] = v.strip('"').strip("'")

_env_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(_env_path):
    _env_path = os.path.expanduser("~/Sagatoy-LLM-TTS-VPS/backend/.env")
load_env(_env_path)

from sagatoyai.services.llm_load_balancer import LLMLoadBalancer, Provider


async def test_balancer(balancer, label: str, prompt: str, language: str):
    """Test a single prompt through the load balancer."""
    start = time.time()
    result = await balancer.generate_response(prompt, language)
    elapsed = (time.time() - start) * 1000
    status = "OK" if result.provider else "FAIL"
    resp = result.text[:180].replace("\n", " ")
    print(f"  [{status}] provider={result.provider} latency={elapsed:.0f}ms")
    if result.text and not result.fallback_used:
        print(f"         -> {resp}")
    elif result.fallback_reason:
        print(f"         -> fallback: {result.fallback_reason}")
    return result


async def main():
    print("="*60)
    print("Load Balancer Test — Full Chain")
    print("="*60)
    print()

    balancer = LLMLoadBalancer(
        primary=Provider.GROQ,
        premium_fallbacks=[Provider.OPENAI, Provider.GEMINI],
        speed_backup=Provider.NVIDIA,
    )

    print(f"Configured providers: {balancer._configured_providers}")
    print(f"Primary: {balancer.primary}")
    print(f"Premium fallbacks: {balancer.premium_fallbacks}")
    print(f"Speed backup: {balancer.speed_backup}")
    print()

    tests = [
        ("SV story", "Berätta en kort godnatt-saga om en liten kanin.", "sv"),
        ("SV math", "Om jag har 3 äpplen och får 5 till, hur många har jag?", "sv"),
        ("DA story", "Fortæl en kort godnat-historie om en lille hund.", "da"),
        ("ZH math", "100减去37等于多少？", "zh"),
        ("EN math", "What is 17 times 24?", "en"),
        ("DA greet", "Sig noget sjovt på dansk!", "da"),
        ("FI math", "Mikä on 8 kertaa 9?", "fi"),
    ]

    results = {}
    for label, prompt, lang in tests:
        print(f"[{label}]")
        r = await test_balancer(balancer, label, prompt, lang)
        results[label] = r
        print()

    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    for label, r in results.items():
        ok = "OK" if r.provider and not r.text.startswith("Hoppsan") else "!!"
        print(f"  {ok} {label}: provider={r.provider} latency={r.latency_ms:.0f}ms")

    print()
    print("Health status:")
    for k, v in balancer.status().items():
        status = "healthy" if v.get("healthy") else "unavailable"
        print(f"  {k}: {status} (failures={v.get('failures', 0)})")


if __name__ == "__main__":
    asyncio.run(main())
