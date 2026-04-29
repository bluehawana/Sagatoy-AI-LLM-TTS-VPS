"""Compare Llama 3.1 70B vs Mistral Nemo 12B vs GPT-4o mini vs Groq Llama 3.1 70B."""

import asyncio
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def load_env(path: str):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ[k] = v.strip('"').strip("'")

load_env(os.path.join(os.path.dirname(__file__), ".env"))


async def test_nim(model_id: str, prompt: str, language: str, system: str = None) -> dict:
    """Test a NIM model."""
    api_base = os.getenv("NEMOTRON_API_BASE", "https://integrate.api.nvidia.com/v1")
    url = api_base if "chat/completions" in api_base else api_base + "/chat/completions"
    api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("NEMOTRON_API_KEY")

    if not api_key:
        return {"error": "No NVIDIA API key", "latency_ms": 0}

    payload = json.dumps({
        "model": model_id,
        "messages": [
            {"role": "system", "content": system or f"You are a friendly AI toy for children aged 3-10. Respond in {language}. Keep it short (2-3 sentences)."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 200,
        "top_p": 0.9,
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            latency = (time.time() - start) * 1000
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"]
            return {"response": content, "latency_ms": latency, "error": None}
    except Exception as e:
        latency = (time.time() - start) * 1000
        return {"response": "", "latency_ms": latency, "error": str(e)}


async def test_openai(prompt: str, language: str, system: str = None) -> dict:
    """Test GPT-4o mini via OpenAI."""
    import openai
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    if not client.api_key:
        return {"error": "No OpenAI key", "latency_ms": 0}

    start = time.time()
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system or f"You are a friendly AI toy for children aged 3-10. Respond in {language}. Keep it short."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        latency = (time.time() - start) * 1000
        return {"response": resp.choices[0].message.content, "latency_ms": latency, "error": None}
    except Exception as e:
        latency = (time.time() - start) * 1000
        return {"response": "", "latency_ms": latency, "error": str(e)}


async def test_groq(prompt: str, language: str, system: str = None) -> dict:
    """Test Llama 3.1 70B via Groq."""
    from groq import AsyncGroq
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY", ""))
    if not client.api_key:
        return {"error": "No Groq key", "latency_ms": 0}

    start = time.time()
    try:
        resp = await client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": system or f"You are a friendly AI toy for children aged 3-10. Respond in {language}. Keep it short."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        latency = (time.time() - start) * 1000
        return {"response": resp.choices[0].message.content, "latency_ms": latency, "error": None}
    except Exception as e:
        latency = (time.time() - start) * 1000
        return {"response": "", "latency_ms": latency, "error": str(e)}


async def run_test(label: str, fn, *args):
    result = await fn(*args)
    status = "OK" if result.get("error") is None else f"FAIL: {result['error']}"
    latency_str = f"{result['latency_ms']:.0f}ms"
    resp_preview = result.get("response", "")[:180].replace("\n", " ")
    print(f"  [{label}] {status} ({latency_str})")
    if result.get("response"):
        print(f"         -> {resp_preview}")
    return result


async def main():
    print("="*70)
    print("NIM Model Comparison — Nordic Kids Toy")
    print("="*70)
    print()

    # Check keys
    nim_key = os.getenv("NVIDIA_API_KEY") or os.getenv("NEMOTRON_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    print(f"NVIDIA key: {'YES' if nim_key else 'NO'}")
    print(f"OpenAI key: {'YES' if openai_key else 'NO'}")
    print(f"Groq key:   {'YES' if groq_key else 'NO'}")
    print()

    system_sv = """Du är en vänlig AI-assistent i en mjuk leksak som pratar med barn 3-10 år.
Använd enkelt, varmt och uppmuntrande språk. Håll svaren korta (2-3 meningar).
Var lekfull och fantasifull. Använd aldrig upprepningar eller konstiga fraser."""

    tests = [
        ("SV-story", "Hej! Berätta en kort godnatt-saga om en liten kanin.", "sv", system_sv),
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

    models = {
        "LLaMA 3.1 70B (NIM)": ("meta/llama-3.1-70b-instruct", test_nim),
        "Mistral Nemo 12B (NIM)": ("mistralai/mistral-nemo-12b-instruct-v2", test_nim),
        "GPT-4o mini": ("", test_openai),
        "LLaMA 3.1 70B (Groq)": ("", test_groq),
    }

    all_results = {}

    for model_name, (model_id, test_fn) in models.items():
        print(f"\n{'='*60}")
        print(f"MODEL: {model_name}")
        print(f"{'='*60}")

        all_results[model_name] = {}
        if model_name == "LLaMA 3.1 70B (NIM)":
            for label, prompt, lang, system in tests:
                result = await run_test(label, test_nim, model_id, prompt, lang, system)
                all_results[model_name][label] = result
        elif model_name == "Mistral Nemo 12B (NIM)":
            for label, prompt, lang, system in tests:
                result = await run_test(label, test_nim, model_id, prompt, lang, system)
                all_results[model_name][label] = result
        elif model_name == "GPT-4o mini":
            for label, prompt, lang, system in tests:
                result = await run_test(label, test_openai, prompt, lang, system)
                all_results[model_name][label] = result
        elif model_name == "LLaMA 3.1 70B (Groq)":
            for label, prompt, lang, system in tests:
                result = await run_test(label, test_groq, prompt, lang, system)
                all_results[model_name][label] = result

    print("\n\n" + "="*70)
    print("DONE")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
