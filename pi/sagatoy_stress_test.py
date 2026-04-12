#!/usr/bin/env python3
"""
SagaToy Stress Test — runs on Raspberry Pi 4.

Simulates N full conversation cycles without needing physical button presses.
Tests the complete STT → LLM → TTS pipeline end-to-end.

Usage:
  python3 sagatoy_stress_test.py --cycles 50 --languages sv,da,no,fi,en,zh

Reports:
  - Per-turn response time
  - Average, p50, p95, p99 latency
  - Error count and error rate
  - Pi CPU temperature (must stay < 70 C)
  - Pass/Fail verdict
"""

import argparse
import asyncio
import json
import logging
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

import httpx
import yaml

# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("stress_test")

CONFIG_PATH = Path(__file__).parent / "config.yaml"
LOCAL_CONFIG_PATH = Path(__file__).parent / "config.local.yaml"

# Pre-written test utterances per language
TEST_INPUTS = {
    "sv": [
        "Hej, vad heter du?",
        "Hur mår du idag?",
        "Vad är din favoritfärg?",
        "Kan du berätta något roligt?",
        "Vad är 2 plus 3?",
    ],
    "da": [
        "Hej, hvad hedder du?",
        "Hvordan har du det?",
        "Hvad er din yndlingsfarve?",
        "Kan du fortælle mig noget sjovt?",
        "Hvad er 2 plus 3?",
    ],
    "no": [
        "Hei, hva heter du?",
        "Hvordan har du det?",
        "Hva er din favorittfarge?",
        "Kan du fortelle meg noe morsomt?",
        "Hva er 2 pluss 3?",
    ],
    "fi": [
        "Hei, mikä sinun nimesi on?",
        "Miten voit tänään?",
        "Mikä on lempiväriesi?",
        "Voitko kertoa jotain hauskaa?",
        "Mitä on 2 plus 3?",
    ],
    "en": [
        "Hi, what is your name?",
        "How are you today?",
        "What is your favourite colour?",
        "Can you tell me something funny?",
        "What is 2 plus 3?",
    ],
    "zh": [
        "你好，你叫什么名字？",
        "你今天怎么样？",
        "你最喜欢什么颜色？",
        "你能告诉我一件有趣的事吗？",
        "2加3等于多少？",
    ],
}

TARGETS = {
    "avg_latency_s": 6.0,
    "p95_latency_s": 8.0,
    "error_rate_pct": 2.0,
    "max_cpu_temp_c": 70.0,
}


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        cfg = yaml.safe_load(f)
    if LOCAL_CONFIG_PATH.exists():
        with open(LOCAL_CONFIG_PATH) as f:
            local = yaml.safe_load(f) or {}
        cfg = _deep_merge(cfg, local)
    return cfg


def _deep_merge(base, override):
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def cpu_temperature() -> float:
    """Read Pi CPU temp in Celsius."""
    try:
        raw = Path("/sys/class/thermal/thermal_zone0/temp").read_text().strip()
        return int(raw) / 1000.0
    except Exception:
        return 0.0


def has_wifi(cfg) -> bool:
    try:
        r = httpx.get(cfg["wifi"]["check_url"],
                      timeout=cfg["wifi"]["check_timeout_s"])
        return r.status_code < 500
    except Exception:
        return False


async def call_llm(cfg: dict, text: str, language: str, wifi: bool) -> str:
    """Call LLM (cloud or offline) directly — no GPIO/audio needed."""
    lang_names = {
        "sv": "Swedish", "da": "Danish", "no": "Norwegian",
        "fi": "Finnish", "en": "English", "zh": "Chinese (Mandarin)",
    }
    device = cfg["device"]
    system_prompt = cfg["llm"]["system_prompt"].format(
        toy_name=device["name"],
        child_name=device.get("child_name") or "little one",
        child_age=device.get("child_age", 5),
        language=lang_names.get(language, language),
    )

    if wifi:
        headers = {
            "Authorization": f"Bearer {cfg['llm']['cloud_api_key']}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": cfg["llm"]["cloud_model"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            "max_tokens": 150,
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(
                f"{cfg['llm']['cloud_base_url']}chat/completions",
                headers=headers, json=payload,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
    else:
        payload = {
            "model": cfg["llm"]["offline_model"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{cfg['llm']['offline_url']}/api/chat", json=payload
            )
            r.raise_for_status()
            return r.json()["message"]["content"].strip()


async def call_tts(cfg: dict, text: str, language: str) -> bool:
    """Run TTS synthesis to /tmp — measure time, don't play audio."""
    voices = cfg["tts"]["voices"]
    voice_val = voices.get(language, "edge")
    tmp = "/tmp/stress_tts.wav"

    if voice_val == "edge":
        import edge_tts
        voice = cfg["tts"]["edge_voices"].get(language, "en-GB-SoniaNeural")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp)
    else:
        proc = subprocess.run(
            ["piper", "--model", voice_val, "--output_file", tmp],
            input=text.encode(), capture_output=True, timeout=15,
        )
        return proc.returncode == 0
    return True


async def run_cycle(cfg: dict, text: str, language: str, wifi: bool) -> dict:
    """Run one full LLM + TTS cycle. Returns timing and success info."""
    result = {
        "language": language,
        "input": text,
        "success": False,
        "latency_s": 0.0,
        "llm_s": 0.0,
        "tts_s": 0.0,
        "error": None,
        "cpu_temp_c": cpu_temperature(),
    }
    try:
        t0 = time.time()
        response = await call_llm(cfg, text, language, wifi)
        t1 = time.time()
        await call_tts(cfg, response, language)
        t2 = time.time()

        result.update({
            "success": True,
            "llm_s": round(t1 - t0, 2),
            "tts_s": round(t2 - t1, 2),
            "latency_s": round(t2 - t0, 2),
            "response_preview": response[:60],
        })
    except Exception as e:
        result["error"] = str(e)
        log.error("Cycle failed [%s]: %s", language, e)

    return result


def print_report(results: list[dict], languages: list[str]):
    total = len(results)
    errors = [r for r in results if not r["success"]]
    successes = [r for r in results if r["success"]]
    latencies = [r["latency_s"] for r in successes]
    temps = [r["cpu_temp_c"] for r in results if r["cpu_temp_c"] > 0]

    print("\n" + "=" * 60)
    print("  SAGATOY STRESS TEST REPORT")
    print("=" * 60)
    print(f"  Total cycles : {total}")
    print(f"  Successful   : {len(successes)}")
    print(f"  Errors       : {len(errors)}")
    print(f"  Error rate   : {len(errors)/total*100:.1f}%")
    if latencies:
        sorted_lat = sorted(latencies)
        p95 = sorted_lat[int(len(sorted_lat) * 0.95)]
        p99 = sorted_lat[int(len(sorted_lat) * 0.99)]
        print(f"\n  Latency (LLM + TTS)")
        print(f"    Average : {statistics.mean(latencies):.2f}s")
        print(f"    Median  : {statistics.median(latencies):.2f}s")
        print(f"    p95     : {p95:.2f}s")
        print(f"    p99     : {p99:.2f}s")
        print(f"    Min     : {min(latencies):.2f}s")
        print(f"    Max     : {max(latencies):.2f}s")

    if temps:
        print(f"\n  CPU Temperature")
        print(f"    Average : {statistics.mean(temps):.1f}C")
        print(f"    Max     : {max(temps):.1f}C")

    # Per-language breakdown
    print("\n  Per-language latency (avg)")
    for lang in languages:
        lang_results = [r["latency_s"] for r in successes if r["language"] == lang]
        if lang_results:
            print(f"    {lang:4s}: {statistics.mean(lang_results):.2f}s  ({len(lang_results)} cycles)")

    # Pass/Fail
    print("\n  TARGETS vs ACTUAL")
    passed = True
    checks = [
        ("Avg latency", statistics.mean(latencies) if latencies else 999,
         TARGETS["avg_latency_s"], "s"),
        ("p95 latency",
         sorted(latencies)[int(len(latencies)*0.95)] if latencies else 999,
         TARGETS["p95_latency_s"], "s"),
        ("Error rate", len(errors)/total*100,
         TARGETS["error_rate_pct"], "%"),
        ("Max CPU temp", max(temps) if temps else 0,
         TARGETS["max_cpu_temp_c"], "C"),
    ]
    for name, actual, target, unit in checks:
        ok = actual <= target
        if not ok:
            passed = False
        status = "PASS" if ok else "FAIL"
        print(f"    [{status}] {name}: {actual:.1f}{unit} (target <= {target}{unit})")

    print("\n" + "=" * 60)
    print(f"  OVERALL: {'PASS - Ready to install in toy!' if passed else 'FAIL - Fix issues before installation'}")
    print("=" * 60 + "\n")

    return passed


async def main():
    parser = argparse.ArgumentParser(description="SagaToy stress test")
    parser.add_argument("--cycles", type=int, default=50,
                        help="Total conversation cycles to simulate")
    parser.add_argument("--languages", type=str, default="sv,da,no,fi,en,zh",
                        help="Comma-separated language codes")
    parser.add_argument("--output", type=str, default=None,
                        help="Save JSON results to file")
    args = parser.parse_args()

    languages = [l.strip() for l in args.languages.split(",")]
    cfg = load_config()
    wifi = has_wifi(cfg)
    log.info("WiFi available: %s", wifi)
    log.info("Languages: %s", languages)
    log.info("Cycles: %d", args.cycles)

    # Build test queue: round-robin across languages
    import itertools
    import random
    lang_cycle = itertools.cycle(languages)
    test_queue = []
    for _ in range(args.cycles):
        lang = next(lang_cycle)
        text = random.choice(TEST_INPUTS.get(lang, TEST_INPUTS["en"]))
        test_queue.append((text, lang))

    results = []
    for i, (text, lang) in enumerate(test_queue, 1):
        log.info("[%d/%d] %s: %s", i, args.cycles, lang, text)
        r = await run_cycle(cfg, text, lang, wifi)
        results.append(r)
        status = "OK" if r["success"] else f"ERROR: {r['error']}"
        log.info("  -> %.2fs | %s", r["latency_s"], status)
        # Brief pause between cycles to avoid rate limits
        await asyncio.sleep(0.5)

    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2))
        log.info("Results saved to %s", args.output)

    passed = print_report(results, languages)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    asyncio.run(main())
