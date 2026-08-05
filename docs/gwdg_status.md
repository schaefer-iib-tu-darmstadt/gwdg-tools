# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-08-05 16:23 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | demand | Tools | Sanity |
|---|--:|--:|:--:|:--:|
| `apertus-70b-instruct-2509` | 13.2s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `deepseek-v4-flash` | 13.7s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `devstral-2-123b-instruct-2512` | 13.8s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `gemma-4-31b-it` | 13.5s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `glm-4.7` | 13.8s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `medgemma-27b-it` | 0.9s | 0 |  | ERR — Error code: 500 |
| `meta-llama-3.1-8b-instruct` | 13.9s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `mistral-medium-3.5-128b` | 13.9s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `openai-gpt-oss-120b` | 13.9s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `qwen3-30b-a3b-instruct-2507` | 13.8s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `qwen3-coder-next` | 14.0s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `qwen3-omni-30b-a3b-instruct` | 13.7s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `qwen3.5-122b-a10b` | 13.8s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `qwen3.5-397b-a17b` | 13.9s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `qwen3.6-27b` | 18.6s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `qwen3.6-35b-a3b` | 13.5s | 0 |  | ERR — Model Not Loaded. Please try again in a few minutes. |

## Embedding-Modelle

| Modell | Latenz | Dim | Verfügbarkeit |
|---|--:|--:|:--:|
| `e5-mistral-7b-instruct` | 18.6s |  | ERR — Model Not Loaded. Please try again in a few minutes. |
| `multilingual-e5-large-instruct` | 12.8s | 1024 | OK |
| `qwen3-embedding-4b` | 3.6s | 2560 | OK |

**Legende:** `demand` = Auslastung zu Probe-Beginn (höher = stärker ausgelastet; Skala undokumentiert). `Tools` Y = Modell löste bei einem Test-Tool (`get_weather`) einen `tool_call` aus, `n` = direkt geantwortet, `ERR` = Fehler. `Sanity` OK = korrekte Ein-Wort-Antwort (Paris), WRONG/ERR = unerwartet/Fehler. Hohe Latenz oder `ERR` ⇒ überlastet oder down.
