# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-08-31 13:05 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | demand | Tools | Sanity |
|---|--:|--:|:--:|:--:|
| `apertus-70b-instruct-2509` | 0.2s | 1 |  | ERR — Error code: 500 |
| `deepseek-v4-flash-0731` | 3.6s | 3 | Y | OK |
| `devstral-2-123b-instruct-2512` | 8.9s | 0 | Y | OK |
| `gemma-4-31b-it` | 0.2s | 1 | Y | OK |
| `glm-4.7` | 319.1s | 13 |  | ERR — Connection error. |
| `meta-llama-3.1-8b-instruct` | 0.9s | 0 | Y | OK |
| `mistral-medium-3.5-128b` | 0.2s | 1 |  | ERR — Error code: 500 |
| `openai-gpt-oss-120b` | 37.4s | 0 | ERR | OK |
| `qwen3-30b-a3b-instruct-2507` | 38.8s | 1 | Y | OK |
| `qwen3-coder-next` | 0.2s | 0 | Y | OK |
| `qwen3-omni-30b-a3b-instruct` | 0.2s | 0 | ERR | OK |
| `qwen3.5-122b-a10b` | 3.5s | 1 | Y | OK |
| `qwen3.5-397b-a17b` | 0.1s | 5 |  | ERR — Error code: 500 |
| `qwen3.6-35b-a3b` | 0.6s | 1 |  | ERR — Error code: 500 |
| `qwen3.8-27b` | 0.6s | 12 |  | ERR — Error code: 500 |

## Embedding-Modelle

| Modell | Latenz | Dim | Verfügbarkeit |
|---|--:|--:|:--:|
| `e5-mistral-7b-instruct` | 0.5s |  | ERR — Error code: 500 |
| `multilingual-e5-large-instruct` | 0.4s | 1024 | OK |
| `qwen3-embedding-4b` | 0.3s | 2560 | OK |

**Legende:** `demand` = Auslastung zu Probe-Beginn (höher = stärker ausgelastet; Skala undokumentiert). `Tools` Y = Modell löste bei einem Test-Tool (`get_weather`) einen `tool_call` aus, `n` = direkt geantwortet, `ERR` = Fehler. `Sanity` OK = korrekte Ein-Wort-Antwort (Paris), WRONG/ERR = unerwartet/Fehler. Hohe Latenz oder `ERR` ⇒ überlastet oder down.
