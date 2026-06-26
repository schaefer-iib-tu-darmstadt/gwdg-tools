# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-06-26 15:29 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | finish | Denk-Stream | demand | status | Sanity |
|---|--:|---|:--:|--:|:--:|:--:|
| `apertus-70b-instruct-2509` | 0.9s | stop | n | 0 | ready | OK |
| `deepseek-r1-distill-llama-70b` | 3.3s | stop | Y | 1 | ready | OK |
| `devstral-2-123b-instruct-2512` | 0.3s | stop | n | 0 | ready | OK |
| `gemma-4-31b-it` | 0.3s | stop | n | 0 | ready | OK |
| `glm-4.7` | 0.3s | stop | n | 0 | ready | OK |
| `internvl3.5-30b-a3b` | 0.2s | stop | n | 0 | ready | OK |
| `medgemma-27b-it` | 0.4s | stop | n | 0 | ready | OK |
| `meta-llama-3.1-8b-instruct` | 0.3s | stop | n | 0 | ready | OK |
| `mistral-large-3-675b-instruct-2512` | 0.3s | stop | n | 4 | ready | OK |
| `openai-gpt-oss-120b` | 0.4s | stop | n | 0 | ready | OK |
| `qwen3-30b-a3b-instruct-2507` | 0.3s | stop | n | 0 | ready | OK |
| `qwen3-coder-30b-a3b-instruct` | 0.2s | stop | n | 0 | ready | OK |
| `qwen3-omni-30b-a3b-instruct` | 0.3s | stop | n | 0 | ready | OK |
| `qwen3.5-122b-a10b` | 5.8s | stop | n | 0 | ready | OK |
| `qwen3.5-397b-a17b` | 6.7s | stop | n | 1 | ready | OK |
| `qwen3.6-35b-a3b` | 3.1s | stop | n | 1 | ready | OK |
| `teuken-7b-instruct-research` | 0.3s | stop | n | 0 | ready | OK |

## Embedding-Modelle

| Modell | Latenz | Dim | Verfügbarkeit |
|---|--:|--:|:--:|
| `e5-mistral-7b-instruct` | 0.7s | 4096 | OK |
| `multilingual-e5-large-instruct` | 1.7s | 1024 | OK |
| `qwen3-embedding-4b` | 3.4s | 2560 | OK |

**Legende:** `demand` = Auslastung beim Katalog-Abruf zu Probe-Beginn (Snapshot; höher = stärker ausgelastet; Skala von GWDG nicht dokumentiert). `Denk-Stream` Y = bei dieser knappen Sanity-Anfrage tatsächlich ein Reasoning-Stream beobachtet (variiert je Prompt; deklarierte Fähigkeit siehe `gwdg_models.md`). Sanity `OK` = korrekte Ein-Wort-Antwort (Paris), `WRONG` = unerwartet, `ERR` = Fehler/Timeout. Hohe Latenz / `ERR` ⇒ überlastet oder down.

> Rate-Limit: (redacted)
