# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-10-19 12:35 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | demand | Tools | Sanity |
|---|--:|--:|:--:|:--:|
| `deepseek-v4-flash-0731` | 0.1s | 11 |  | ERR — Error code: 500 |
| `gemma-4-31b-it` | 1.1s | 2 | Y | OK |
| `glm-5.3-flash` | 0.1s | 20 |  | ERR — Error code: 500 |
| `meta-llama-3.1-8b-instruct` | 0.7s | 0 | ERR | OK |
| `qwen3-30b-a3b-instruct-2507` | 0.7s | 1 | Y | OK |
| `qwen3-coder-next` | 0.2s | 0 | Y | OK |
| `qwen3-omni-30b-a3b-instruct` | 0.2s | 0 | ERR | OK |
| `qwen3.5-397b-a17b` | 600.6s | 4 |  | ERR — Request timed out. |
| `qwen3.6-35b-a3b` | 4.1s | 2 | ERR | OK |
| `qwen3.8-27b` | 1.7s | 16 | Y | OK |

## Embedding-Modelle

| Modell | Latenz | Dim | Verfügbarkeit |
|---|--:|--:|:--:|
| `e5-mistral-7b-instruct` | 0.3s | 4096 | OK |
| `multilingual-e5-large-instruct` | 0.4s | 1024 | OK |
| `qwen3-embedding-4b` | 0.6s | 2560 | OK |

**Legende:** `demand` = Auslastung zu Probe-Beginn (höher = stärker ausgelastet; Skala undokumentiert). `Tools` Y = Modell löste bei einem Test-Tool (`get_weather`) einen `tool_call` aus, `n` = direkt geantwortet, `ERR` = Fehler. `Sanity` OK = korrekte Ein-Wort-Antwort (Paris), WRONG/ERR = unerwartet/Fehler. Hohe Latenz oder `ERR` ⇒ überlastet oder down.
