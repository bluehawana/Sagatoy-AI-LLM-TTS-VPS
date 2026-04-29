"""Test Groq directly on VPS."""
import os
import json
import time
import urllib.request

# Load .env
env_path = os.path.expanduser("~/Sagatoy-LLM-TTS-VPS/backend/.env")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k] = v.strip('"').strip("'")

api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"
payload = json.dumps({
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Berätta en kort godnatt-saga om en liten kanin."}],
    "max_tokens": 200,
    "top_p": 0.9,
}).encode()

req = urllib.request.Request(url, data=payload, headers={
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
})

start = time.time()
resp = urllib.request.urlopen(req, timeout=30)
elapsed = (time.time() - start) * 1000
data = json.loads(resp.read())

print(f"Groq OK: {elapsed:.0f}ms")
print(data["choices"][0]["message"]["content"])
