"""Compare LLaMA 3.1 70B (NIM vs Groq) vs Mistral Nemo 12B (NIM) vs GPT-4o mini (OpenAI).
Pure HTTP — no Python SDK dependencies needed."""

import asyncio
import json
import os
import sys
import time
import urllib.request
import urllib.error


def load_env(path: str):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ[k] = v.strip('"').strip("'")

_env_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(_env_path):
    _env_path = os.path.expanduser("~/Sagatoy-LLM-TTS-VPS/backend/.env")
load_env(_env_path)


def chat_request(messages, model, provider="nvidia"):
    """Make a single chat completion request and return response + latency."""
    key_map = {
        "nvidia": "NVIDIA_API_KEY" or os.getenv("NEMOTRON_API_KEY"),
        "openai": "OPENAI_API_KEY",
        "groq": "GROQ_API_KEY",
    }
    api_key = os.getenv(key_map.get(provider, "NVIDIA_API_KEY"))
    if not api_key:
        return None, 0, "No API key"

    if provider == "nvidia":
        api_base = os.getenv("NEMOTRON_API_BASE", "https://integrate.api.nvidia.com/v1")
        url = api_base if "chat/completions" in api_base else api_base + "/chat/completions"
    elif provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
    elif provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 200,
        "top_p": 0.9,
    }).encode()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if provider == "nvidia":
        headers["Authorization"] = f"Bearer {api_key}"
    elif provider == "openai":
        headers["Authorization"] = f"Bearer {api_key}"
    elif provider == "groq":
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, data=payload, headers=headers)
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            latency = (time.time() - start) * 1000
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"]
            return content, latency, None
    except urllib.error.HTTPError as e:
        latency = (time.time() - start) * 1000
        body = e.read().decode("utf-8", errors="replace")
        return None, latency, f"HTTP {e.code}: {body[:200]}"
    except Exception as e:
        latency = (time.time() - start) * 1000
        return None, latency, str(e)


async def test_model(name, model, provider, tests):
    print(f"\n{'='*60}")
    print(f"MODEL: {name}")
    print(f"{'='*60}")
    results = {}
    for label, prompt, lang, system in tests:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
        content, latency, err = chat_request(messages, model, provider)
        status = "OK" if err is None else f"FAIL ({err[:80]})"
        resp_preview = content[:180].replace("\n", " ") if content else ""
        print(f"  [{label}] {status} ({latency:.0f}ms)")
        if resp_preview:
            print(f"         -> {resp_preview}")
        results[label] = {"response": content, "latency_ms": latency, "error": err}
    return results


async def main():
    print("="*70)
    print("NIM Model Comparison — Nordic Kids Toy")
    print("="*70)

    keys = {
        "NVIDIA": os.getenv("NVIDIA_API_KEY") or os.getenv("NEMOTRON_API_KEY"),
        "OpenAI": os.getenv("OPENAI_API_KEY"),
        "Groq": os.getenv("GROQ_API_KEY"),
    }
    for k, v in keys.items():
        print(f"  {k}: {'YES' if v else 'NO'}")
    print()

    system_sv = """Du är en vänlig AI-assistent i en mjuk leksak som pratar med barn 3-10 år.
Använd enkelt, varmt och uppmuntrande språk. Håll svaren korta (2-3 meningar).
Var lekfull och fantasifull. Använd aldrig upprepningar eller konstiga fraser."""

    tests = [
        ("SV-story", "Berätta en kort godnatt-saga om en liten kanin.", "sv", system_sv),
        ("SV-math", "Om jag har 3 äpplen och får 5 till, hur många har jag?", "sv", system_sv),
        ("DA-story", "Fortæl en kort godnat-historie om en lille hund.", "da",
         "Du er en venlig AI-assistent for børn 3-10 år. Korte svar (2-3 sætninger)."),
        ("NO-story", "Fortell en kort godnatt-historie om en liten fisk.", "no",
         "Du er en vennlig AI-assistent for barn 3-10 år. Korte svar (2-3 setninger)."),
        ("FI-story", "Kerro lyhyt tarina kissasta, joka rakentaa pihlajasta linnaa.", "fi",
         "Olet ystävällinen tekoälylelu, joka puhuu 3-10-vuotiaille lapsille. Lyhyet vastaukset."),
        ("ZH-math", "100减去37等于多少？", "zh",
         "你是一个友好的玩具助手，和3-10岁的孩子聊天。回答简短（2-3句话）。"),
        ("EN-math", "What is 17 times 24?", "en",
         "You are a friendly AI toy for children. Answer math questions clearly."),
        ("DA-greet", "Sig noget sjovt på dansk!", "da",
         "Du er en venlig AI-assistent for børn 3-10 år. Korte svar."),
        ("NO-weather", "Hva er været i Oslo idag?", "no",
         "Du er en vennlig AI-assistent for barn 3-10 år. Korte svar."),
        ("FI-math", "Mikä on 8 kertaa 9?", "fi",
         "Olet ystävällinen tekoälylelu. Lyhyet vastaukset."),
    ]

    results = {}

    # Only run tests for models that have keys
    if keys["NVIDIA"]:
        for label, model in [("LLaMA 3.1 70B", "meta/llama-3.1-70b-instruct"),
                              ("Mistral Nemo 12B", "mistralai/mistral-nemo-12b-instruct-v2")]:
            r = await test_model(model, model, "nvidia", tests)
            results[f"NIM: {label}"] = r

    if keys["OpenAI"]:
        r = await test_model("GPT-4o mini", "gpt-4o-mini", "openai", tests)
        results["GPT-4o mini"] = r

    if keys["Groq"]:
        r = await test_model("LLaMA 3.1 70B", "llama-3.1-70b-versatile", "groq", tests)
        results["Groq LLaMA 3.1 70B"] = r

    # Summary
    print("\n\n" + "="*70)
    print("LATENCY SUMMARY (all tests)")
    print("="*70)
    for name, res in results.items():
        avg = sum(r["latency_ms"] for r in res.values()) / len(res)
        ok = sum(1 for r in res.values() if r["error"] is None)
        print(f"  {name}: {ok}/{len(res)} OK, avg {avg:.0f}ms")


if __name__ == "__main__":
    asyncio.run(main())
