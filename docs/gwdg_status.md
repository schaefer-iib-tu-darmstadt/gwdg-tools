# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-06-29 11:05 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | demand | Tools | Sanity |
|---|--:|--:|:--:|:--:|
| `apertus-70b-instruct-2509` | 0.3s | 2 | Y | OK |
| `deepseek-r1-distill-llama-70b` | 3.7s | 1 | ERR | OK |
| `devstral-2-123b-instruct-2512` | 1.0s | 1 | Y | OK |
| `gemma-4-31b-it` | 0.3s | 0 | Y | OK |
| `glm-4.7` | 0.4s | 1 | Y | OK |
| `internvl3.5-30b-a3b` | 0.2s | 0 | ERR | OK |
| `medgemma-27b-it` | 0.8s | 0 | ERR | OK |
| `meta-llama-3.1-8b-instruct` | 28.0s | 1 | Y | OK |
| `mistral-large-3-675b-instruct-2512` | 0.3s | 1 | Y | OK |
| `openai-gpt-oss-120b` | 1.0s | 0 | Y | OK |
| `qwen3-30b-a3b-instruct-2507` | 0.2s | 3 | Y | OK |
| `qwen3-coder-30b-a3b-instruct` | 0.2s | 0 | Y | OK |
| `qwen3-omni-30b-a3b-instruct` | 0.2s | 0 | ERR | OK |
| `qwen3.5-122b-a10b` | 6.4s | 1 | Y | OK |
| `qwen3.5-397b-a17b` | 1.9s | 1 | Y | OK |
| `qwen3.6-35b-a3b` | 1.2s | 2 | Y | OK |
| `teuken-7b-instruct-research` | 0.3s | 0 | ERR | OK |

## Embedding-Modelle

| Modell | Latenz | Dim | Verfügbarkeit |
|---|--:|--:|:--:|
| `e5-mistral-7b-instruct` | 1.8s | 4096 | OK |
| `multilingual-e5-large-instruct` | 4.0s | 1024 | OK |
| `qwen3-embedding-4b` | 0.5s | 2560 | OK |

**Legende:** `demand` = Auslastung zu Probe-Beginn (höher = stärker ausgelastet; Skala undokumentiert). `Tools` Y = Modell löste bei einem Test-Tool (`get_weather`) einen `tool_call` aus, `n` = direkt geantwortet, `ERR` = Fehler. `Sanity` OK = korrekte Ein-Wort-Antwort (Paris), WRONG/ERR = unerwartet/Fehler. Hohe Latenz oder `ERR` ⇒ überlastet oder down.
