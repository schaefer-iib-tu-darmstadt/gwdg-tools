# GWDG Chat-AI — Status / Latenz-Probe

> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **2026-06-26 13:39 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1` · eine neutrale Sanity-Anfrage (kalt) pro Modell.
> Timeout 600s. Latenz = eine Anfrage, kalt (kein Mittelwert).

| Modell | Latenz | finish | Reasoning | r_len | out_len | tok in/out | Sanity |
|---|--:|---|:--:|--:|--:|--:|:--:|
| `apertus-70b-instruct-2509` | 0.2s | stop | n | 0 | 5 | 45/2 | OK |
| `deepseek-r1-distill-llama-70b` | 3.2s | stop | Y | 664 | 6 | 35/157 | OK |
| `devstral-2-123b-instruct-2512` | 0.2s | stop | n | 0 | 5 | 31/2 | OK |
| `gemma-4-31b-it` | 0.1s | stop | n | 0 | 5 | 45/2 | OK |
| `glm-4.7` | 36.6s | stop | n | 0 | 5 | 32/2 | OK |
| `internvl3.5-30b-a3b` | 0.4s | stop | n | 0 | 5 | 43/2 | OK |
| `medgemma-27b-it` | 0.3s | stop | n | 0 | 5 | 36/3 | OK |
| `meta-llama-3.1-8b-instruct` | 0.1s | stop | n | 0 | 6 | 65/3 | OK |
| `mistral-large-3-675b-instruct-2512` | 600.6s | stop | n | 0 | 5 | 31/2 | OK |
| `openai-gpt-oss-120b` | 0.7s | stop | n | 0 | 5 | 97/57 | OK |
| `qwen3-30b-a3b-instruct-2507` | 0.1s | stop | n | 0 | 5 | 43/2 | OK |
| `qwen3-coder-30b-a3b-instruct` | 0.1s | stop | n | 0 | 5 | 43/2 | OK |
| `qwen3-omni-30b-a3b-instruct` | 0.1s | stop | n | 0 | 5 | 43/2 | OK |
| `qwen3.5-122b-a10b` | 7.0s | stop | n | 0 | 5 | 41/227 | OK |
| `qwen3.5-397b-a17b` | 3.0s | stop | n | 0 | 5 | 41/182 | OK |
| `qwen3.6-35b-a3b` | 8.0s | stop | n | 0 | 5 | 41/209 | OK |
| `teuken-7b-instruct-research` | 0.1s | stop | n | 0 | 5 | 34/2 | OK |

**Legende:** Reasoning Y = Modell emittiert einen (unsichtbaren) Denk-Stream → langsamer/teurer pro Call. Sanity `OK` = korrekte Ein-Wort-Antwort (Paris), `WRONG` = unerwartete Ausgabe, `ERR` = Fehler/Timeout (Meldung in der Spalte). Hohe Latenz oder `ERR` ⇒ Modell aktuell überlastet oder nicht verfügbar.
