# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-09-21 12:20 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | demand | Tools | Sanity |
|---|--:|--:|:--:|:--:|
| `apertus-70b-instruct-2509` | 0.5s | 1 | Y | OK |
| `deepseek-v4-flash-0731` | 0.2s | 4 |  | ERR — Error code: 500 |
| `devstral-2-123b-instruct-2512` | 0.8s | 0 | Y | OK |
| `gemma-4-31b-it` | 0.2s | 0 |  | ERR — Error code: 500 |
| `glm-5.3-flash` | 1.3s | 5 | Y | OK |
| `meta-llama-3.1-8b-instruct` | 0.2s | 0 | Y | OK |
| `mistral-medium-3.5-128b` | 0.3s | 11 | ERR | OK |
| `openai-gpt-oss-120b` | 0.8s | 0 |  | ERR — Error code: 500 |
| `qwen3-30b-a3b-instruct-2507` | 0.9s | 1 | ERR | OK |
| `qwen3-coder-next` | 0.9s | 0 | Y | OK |
| `qwen3-omni-30b-a3b-instruct` | 0.3s | 0 | ERR | OK |
| `qwen3.5-397b-a17b` | 6.0s | 5 | Y | OK |
| `qwen3.6-35b-a3b` | 2.2s | 0 | Y | OK |
| `qwen3.8-27b` | 29.7s | 5 | Y | OK |

## Embedding-Modelle

| Modell | Latenz | Dim | Verfügbarkeit |
|---|--:|--:|:--:|
| `e5-mistral-7b-instruct` | 0.6s | 4096 | OK |
| `multilingual-e5-large-instruct` | 0.1s |  | ERR — Error code: 500 |
| `qwen3-embedding-4b` | 1.1s | 2560 | OK |

**Legende:** `demand` = Auslastung zu Probe-Beginn (höher = stärker ausgelastet; Skala undokumentiert). `Tools` Y = Modell löste bei einem Test-Tool (`get_weather`) einen `tool_call` aus, `n` = direkt geantwortet, `ERR` = Fehler. `Sanity` OK = korrekte Ein-Wort-Antwort (Paris), WRONG/ERR = unerwartet/Fehler. Hohe Latenz oder `ERR` ⇒ überlastet oder down.
