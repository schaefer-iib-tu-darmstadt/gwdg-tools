# GWDG Chat-AI — verfügbare Modelle

> Auto-generiert von `gwdg models` (gwdg-tools) — Stand **2026-06-29 11:03 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1/models` (OpenAI-kompatibler Endpoint).
> Aktuell **17 Chat-Modelle** im Live-Katalog.

| Modell-ID | Name | Eingang | Ausgang |
|---|---|---|---|
| `apertus-70b-instruct-2509` | Apertus 70B Instruct 2509 | text | text |
| `deepseek-r1-distill-llama-70b` | DeepSeek R1 Distill Llama 70B | text | text, thought |
| `devstral-2-123b-instruct-2512` | Devstral 2 123B Instruct 2512 | text | text |
| `gemma-4-31b-it` | Gemma 4 31B Instruct | text, image | text |
| `glm-4.7` | GLM-4.7 | text | text |
| `internvl3.5-30b-a3b` | InternVL 3.5 30B A3B | text, image, video | text |
| `medgemma-27b-it` | MedGemma 27B Instruct | text, image | text |
| `meta-llama-3.1-8b-instruct` | Meta Llama 3.1 8B Instruct | text | text |
| `mistral-large-3-675b-instruct-2512` | Mistral Large 3 675B Instruct 2512 | text, image | text |
| `openai-gpt-oss-120b` | OpenAI GPT OSS 120B | text | text |
| `qwen3-30b-a3b-instruct-2507` | Qwen 3 30B A3B Instruct 2507 | text | text |
| `qwen3-coder-30b-a3b-instruct` | Qwen 3 Coder 30B A3B Instruct | text | text |
| `qwen3-omni-30b-a3b-instruct` | Qwen 3 Omni 30B A3B Instruct | text, image, audio | text |
| `qwen3.5-122b-a10b` | Qwen 3.5 122B A10B | text, image | text, thought |
| `qwen3.5-397b-a17b` | Qwen 3.5 397B A17B | text, image | text, thought |
| `qwen3.6-35b-a3b` | Qwen 3.6 35B A3B | text, image | text |
| `teuken-7b-instruct-research` | Teuken 7B Instruct Research | text | text |

_Eingang/Ausgang = Modalitäten (text, image, audio, video, thought). `thought` im Ausgang = Modell liefert seinen Denkprozess als separates `reasoning_content`-Feld._

> **Kontextfenster, Parametergröße, Anbieter, Lizenz, Datenschutz-Tier und Reasoning-/Capability-Details** liefert die API nicht (zuverlässig) — dafür die GWDG-Doku nutzen: <https://docs.hpc.gwdg.de/services/ai-services/chat-ai/models/index.html>. Dort stehen auch externe Modelle (z. B. Claude, GPT), die am selben Endpoint laufen, aber nicht im Live-Katalog erscheinen.

## Embedding-Modelle

> Nicht über `/v1/models` auflistbar — nur via `/v1/embeddings` mit bekannter ID erreichbar. Latenz / Dimension / Verfügbarkeit siehe `gwdg_status.md`.

| Modell-ID |
|---|
| `e5-mistral-7b-instruct` |
| `multilingual-e5-large-instruct` |
| `qwen3-embedding-4b` |
