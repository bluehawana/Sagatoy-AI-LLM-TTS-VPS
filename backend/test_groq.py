"""Test Groq API key."""
import json
import os
import time
import urllib.request

# Load .env
with open(os.path.join(os.path.dirname(__file__), ".env")) as f:
    for line in f:
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k] = v.strip('"').strip("'")

api_key = os.getenv("GROQ_API_KEY")
print(f"Key: {api_key[:20]}...")
print(f"Key length: {len(api_key)}")

url = "https://api.groq.com/openai/v1/chat/completions"
payload = json.dumps({
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "hi"}],
    "max_tokens": 10,
}).encode()

req = urllib.request.Request(url, data=payload, headers={
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "*/*",
})

start = time.time()
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        elapsed = (time.time() - start) * 1000
        data = json.loads(resp.read())
        print(f"OK: {elapsed:.0f}ms | {data['choices'][0]['message']['content']}")
except urllib.error.HTTPError as e:
    elapsed = (time.time() - start) * 1000
    print(f"HTTP {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    elapsed = (time.time() - start) * 1000
    print(f"Error: {elapsed:.0f}ms | {e}")
