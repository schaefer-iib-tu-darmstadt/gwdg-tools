# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-06-26 16:52 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | finish | demand | status | Tools | Sanity |
|---|--:|---|--:|:--:|:--:|:--:|
| `apertus-70b-instruct-2509` | 0.1s | stop | 0 | ready | n | OK |
| `deepseek-r1-distill-llama-70b` | 2.6s | stop | 0 | ready | ERR | OK |
| `devstral-2-123b-instruct-2512` | 0.4s | stop | 0 | ready | Y | OK |
| `gemma-4-31b-it` | 0.3s | stop | 0 | ready | Y | OK |
| `glm-4.7` | 0.1s | stop | 0 | ready | Y | OK |
| `internvl3.5-30b-a3b` | 0.1s | stop | 0 | ready | ERR | OK |
| `medgemma-27b-it` | 0.4s | stop | 0 | ready | ERR | OK |
| `meta-llama-3.1-8b-instruct` | 30.2s | stop | 0 | ready | Y | OK |
| `mistral-large-3-675b-instruct-2512` | 602.4s | stop | 0 | ready | Y | OK |
| `openai-gpt-oss-120b` | 0.3s | stop | 0 | ready | Y | OK |
| `qwen3-30b-a3b-instruct-2507` | 0.1s | stop | 0 | ready | Y | OK |
| `qwen3-coder-30b-a3b-instruct` | 0.3s | stop | 0 | ready | Y | OK |
| `qwen3-omni-30b-a3b-instruct` | 0.1s | stop | 0 | ready | ERR | OK |
| `qwen3.5-122b-a10b` | 4.6s | stop | 0 | ready | Y | OK |
| `qwen3.5-397b-a17b` | 2.0s | stop | 0 | ready | Y | OK |
| `qwen3.6-35b-a3b` | 2.4s | stop | 0 | ready | Y | OK |
| `teuken-7b-instruct-research` | 15.1s | stop | 0 | ready | ERR | OK |

## Embedding-Modelle

| Modell | Latenz | Dim | Verfügbarkeit |
|---|--:|--:|:--:|
| `e5-mistral-7b-instruct` | 1.1s | 4096 | OK |
| `multilingual-e5-large-instruct` | 2.9s | 1024 | OK |
| `qwen3-embedding-4b` | 0.5s | 2560 | OK |

**Legende:** `demand` = Auslastung beim Katalog-Abruf zu Probe-Beginn (Snapshot; höher = stärker ausgelastet; Skala von GWDG nicht dokumentiert). Reasoning-Fähigkeit siehe `gwdg_models.md`. `Tools` Y = Modell löste bei einem Test-Tool (`get_weather`) einen `tool_call` aus (`finish_reason=tool_calls`); `n` = direkt geantwortet; `ERR` = Fehler. Sanity `OK` = korrekte Ein-Wort-Antwort (Paris), `WRONG` = unerwartet, `ERR` = Fehler/Timeout. Hohe Latenz / `ERR` ⇒ überlastet oder down.

> Rate-Limit: (redacted)
