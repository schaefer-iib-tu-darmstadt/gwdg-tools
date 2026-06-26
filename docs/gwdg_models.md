# GWDG Chat-AI — verfügbare Modelle

> Auto-generiert von `gwdg models` (gwdg-tools) — Stand **2026-06-26 15:28 UTC**.
> Quelle: `https://chat-ai.academiccloud.de/v1/models` (OpenAI-kompatibler Endpoint).
> Aktuell **17 Chat-Modelle** im Katalog.

| Modell-ID | Name | Eingang | Ausgang | Reasoning |
|---|---|---|---|:--:|
| `apertus-70b-instruct-2509` | Apertus 70B Instruct 2509 | text | text | n |
| `deepseek-r1-distill-llama-70b` | DeepSeek R1 Distill Llama 70B | text | text, thought | Y |
| `devstral-2-123b-instruct-2512` | Devstral 2 123B Instruct 2512 | text | text | n |
| `gemma-4-31b-it` | Gemma 4 31B Instruct | text, image | text | n |
| `glm-4.7` | GLM-4.7 | text | text | n |
| `internvl3.5-30b-a3b` | InternVL 3.5 30B A3B | text, image, video | text | n |
| `medgemma-27b-it` | MedGemma 27B Instruct | text, image | text | n |
| `meta-llama-3.1-8b-instruct` | Meta Llama 3.1 8B Instruct | text | text | n |
| `mistral-large-3-675b-instruct-2512` | Mistral Large 3 675B Instruct 2512 | text, image | text | n |
| `openai-gpt-oss-120b` | OpenAI GPT OSS 120B | text | text | n |
| `qwen3-30b-a3b-instruct-2507` | Qwen 3 30B A3B Instruct 2507 | text | text | n |
| `qwen3-coder-30b-a3b-instruct` | Qwen 3 Coder 30B A3B Instruct | text | text | n |
| `qwen3-omni-30b-a3b-instruct` | Qwen 3 Omni 30B A3B Instruct | text, image, audio | text | n |
| `qwen3.5-122b-a10b` | Qwen 3.5 122B A10B | text, image | text, thought | Y |
| `qwen3.5-397b-a17b` | Qwen 3.5 397B A17B | text, image | text, thought | Y |
| `qwen3.6-35b-a3b` | Qwen 3.6 35B A3B | text, image | text | n |
| `teuken-7b-instruct-research` | Teuken 7B Instruct Research | text | text | n |

_Eingang/Ausgang = Modalitäten (text/image/audio/video). Reasoning Y = Modell kann einen Denk-Stream (`thought`) ausgeben (deklarierte Fähigkeit laut Katalog; ob er pro Antwort wirklich auftritt, zeigt der Live-Probe in `gwdg_status.md`)._

## Embedding-Modelle

> Nicht über `/v1/models` auflistbar — nur via `/v1/embeddings` mit bekannter ID erreichbar. Latenz / Dimension / Verfügbarkeit siehe `gwdg_status.md`.

| Modell-ID |
|---|
| `e5-mistral-7b-instruct` |
| `multilingual-e5-large-instruct` |
| `qwen3-embedding-4b` |
