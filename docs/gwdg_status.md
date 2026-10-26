# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-10-26 12:27 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | demand | Tools | Sanity |
|---|--:|--:|:--:|:--:|
| `deepseek-v4-flash-0731` | 0.2s | 5 |  | ERR — Error code: 500 |
| `gemma-4-31b-it` | 0.6s | 1 |  | ERR — Error code: 500 |
| `glm-5.3-flash` | 5.8s | 4 | Y | OK |
| `meta-llama-3.1-8b-instruct` | 0.2s | 0 |  | ERR — Error code: 500 |
| `qwen3-30b-a3b-instruct-2507` | 1.0s | 1 | ERR | OK |
| `qwen3-coder-next` | 0.7s | 0 |  | ERR — Error code: 500 |
| `qwen3-omni-30b-a3b-instruct` | 0.5s | 0 |  | ERR — Error code: 500 |
| `qwen3.5-397b-a17b` | 17.9s | 3 | ERR | OK |
| `qwen3.6-35b-a3b` | 0.7s | 0 |  | ERR — Error code: 500 |
| `qwen3.8-27b` | 49.9s | 6 | ERR | OK |

## Embedding-Modelle

| Modell | Latenz | Dim | Verfügbarkeit |
|---|--:|--:|:--:|
| `e5-mistral-7b-instruct` | 0.9s |  | ERR — Error code: 500 |
| `multilingual-e5-large-instruct` | 0.7s | 1024 | OK |
| `qwen3-embedding-4b` | 0.8s | 2560 | OK |

**Legende:** `demand` = Auslastung zu Probe-Beginn (höher = stärker ausgelastet; Skala undokumentiert). `Tools` Y = Modell löste bei einem Test-Tool (`get_weather`) einen `tool_call` aus, `n` = direkt geantwortet, `ERR` = Fehler. `Sanity` OK = korrekte Ein-Wort-Antwort (Paris), WRONG/ERR = unerwartet/Fehler. Hohe Latenz oder `ERR` ⇒ überlastet oder down.
