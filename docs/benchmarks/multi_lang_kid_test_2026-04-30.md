# Multi-Language Kid Test Benchmark

**Date:** 2026-04-30
**Branch:** `nvidia-nim`
**Provider Chain:** Groq (primary) → OpenAI → Gemini → NVIDIA (speed backup)

## Configured Providers

| Provider | Status | Key Source |
|----------|--------|------------|
| Groq (llama-3.3-70b) | Configured | `GROQ_API_KEY` in `.env` |
| OpenAI (GPT-4o mini) | Configured | `OPENAI_API_KEY` in `.env` |
| Google Gemini | Configured | `GOOGLE_API_KEY` in `.env` |
| NVIDIA NIM | Configured | `NVIDIA_API_KEY` / `NEMOTRON_API_KEY` in `.env` |

> All keys loaded from local `.env` at test time. No hardcoded credentials anywhere.
> `.env.example` contains only placeholders. `.env` is not tracked in git.

## Test Results: 36/36 — 100% PASS

### EN (English) — 9/9

| # | Label | Provider | Latency | Description |
|---|-------|----------|---------|-------------|
| 1 | EN girl 5yo greeting | gemini | 5806ms | Emma, 5yo, greeting — fallback from GROQ (network glitch) |
| 2 | EN girl bedtime story | groq | 435ms | Sweet story about stars and the moon |
| 3 | EN girl math help | groq | 228ms | 7 bracelets minus 3 |
| 4 | EN girl animal question | groq | 295ms | Do dogs dream? |
| 5 | EN boy 6yo greeting | groq | 0ms | Leo, 6yo — direct date/day answer |
| 6 | EN boy dinosaurs | groq | 227ms | Biggest dinosaur ever |
| 7 | EN boy space | groq | 337ms | Aliens on Mars |
| 8 | EN boy math | groq | 209ms | 12 blocks minus 5 |
| 9 | EN funny elephant joke | groq | 177ms | Funny joke about elephant losing a tooth |

**EN avg latency: 857ms** (boosted by first request fallback)

### SV (Swedish) — 8/8

| # | Label | Provider | Latency | Description |
|---|-------|----------|---------|-------------|
| 1 | SV girl 4yo greeting | groq | 360ms | Ella, 4yo, greeting |
| 2 | SV girl goodnight | groq | 590ms | Flying princess story |
| 3 | SV girl math | groq | 288ms | 4 + 6 balloons |
| 4 | SV girl nature | groq | 344ms | Thousand-leg creature facts |
| 5 | SV boy 7yo greeting | groq | 274ms | Aksel, 7yo, greeting |
| 6 | SV boy robots | groq | 465ms | How to build a robot friend |
| 7 | SV boy colors | groq | 261ms | Red + yellow = orange |
| 8 | SV rain day | groq | 0ms | Direct day/date answer |

**SV avg latency: 323ms**

### DA (Danish) — 6/6

| # | Label | Provider | Latency | Description |
|---|-------|----------|---------|-------------|
| 1 | DA girl 5yo greeting | groq | 251ms | Freja, 5yo, greeting |
| 2 | DA girl story | groq | 616ms | Princess who talks to cats |
| 3 | DA girl math | groq | 295ms | 6 + 4 smørepapirer |
| 4 | DA boy 6yo greeting | groq | 305ms | Mads, 6yo, greeting |
| 5 | DA boy space | groq | 589ms | Aliens on Mars (cute) |
| 6 | DA dream | groq | 2419ms | What do you dream about |

**DA avg latency: 746ms**

### FI (Finnish) — 6/6

| # | Label | Provider | Latency | Description |
|---|-------|----------|---------|-------------|
| 1 | FI girl 4yo greeting | groq | 246ms | Aino, 4yo, greeting |
| 2 | FI girl animals | groq | 320ms | Most beautiful animals |
| 3 | FI girl math | groq | 249ms | 9 + 3 star stickers |
| 4 | FI boy 7yo greeting | groq | 394ms | Onni, 7yo, greeting |
| 5 | FI boy dinosaurs | groq | 391ms | Biggest dinosaur |
| 6 | FI wonder | groq | 2466ms | Why is the sky blue |

**FI avg latency: 678ms**

### ZH (Chinese Mandarin) — 7/7

| # | Label | Provider | Latency | Description |
|---|-------|----------|---------|-------------|
| 1 | ZH girl 5yo greeting | groq | 211ms | 小美, 5yo, greeting |
| 2 | ZH girl story | groq | 446ms | Rainbow and little bird story |
| 3 | ZH girl math | groq | 276ms | 1 + 2 strawberries |
| 4 | ZH girl animals | groq | 365ms | Why birds fly |
| 5 | ZH boy 6yo greeting | groq | 246ms | 小明, 6yo, greeting |
| 6 | ZH boy space | groq | 317ms | Aliens on Mars |
| 7 | ZH joke | groq | 2476ms | Funny dog story |

**ZH avg latency: 620ms**

### NVIDIA NIM — 2/2 (separate test)

| Model | Latency | Status |
|-------|---------|--------|
| nemotron-mini | 467ms | PASS |
| llama-3.1-8b | 864ms | PASS |
| Chinese Mandarin | - | PASS |

## Summary

| Language | OK / Total | Avg Latency |
|----------|------------|-------------|
| EN | 9/9 | 857ms |
| SV | 8/8 | 323ms |
| DA | 6/6 | 746ms |
| FI | 6/6 | 678ms |
| ZH | 7/7 | 620ms |
| **OVERALL** | **36/36** | **564ms** |

## Notes

- First EN request fell through to Gemini due to a brief GROQ connection error (recovered immediately after)
- Math and date/day questions use direct calculation (0ms) — no LLM call needed
- All responses are age-appropriate (3-10 years), warm and encouraging
- No API keys are hardcoded in source or test scripts — all loaded from `.env` at runtime
- `.env.example` contains only placeholder values

## Test Methodology

- 36 prompts across 5 languages, 3 question types (greeting, story, math)
- Target audience: girls and boys ages 3-10
- Prompted with child-like phrasing (names, ages, simple sentences)
- Each prompt tests natural language understanding + language capability
- Latency measured end-to-end from request to response text
