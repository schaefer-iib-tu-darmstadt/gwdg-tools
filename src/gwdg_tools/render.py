"""Render probe results into the Markdown reports under docs/."""
from datetime import datetime, timezone

from .probes import EMBEDDING_MODELS

# Per-model details the API does not expose (context window, parameter size, real
# provider, license, data-privacy tier, reasoning/capabilities) — point readers to
# the GWDG docs instead of hand-maintaining a stale copy here.
GWDG_MODELS_DOC = "https://docs.hpc.gwdg.de/services/ai-services/chat-ai/models/index.html"


def _now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def render_models_md(rows: list[dict], base_url: str) -> str:
    lines = [
        "# GWDG Chat-AI — verfügbare Modelle",
        "",
        f"> Auto-generiert von `gwdg models` (gwdg-tools) — Stand **{_now()}**.",
        f"> Quelle: `{base_url}/models` (OpenAI-kompatibler Endpoint).",
        f"> Aktuell **{len(rows)} Chat-Modelle** im Live-Katalog.",
        "",
        "| Modell-ID | Name | Eingang | Ausgang |",
        "|---|---|---|---|",
    ]
    for r in rows:
        eingang = ", ".join(r.get("input") or [])
        ausgang = ", ".join(r.get("output") or [])
        lines.append(f"| `{r['id']}` | {r.get('name', '')} | {eingang} | {ausgang} |")
    lines += [
        "",
        "_Eingang/Ausgang = Modalitäten (text, image, audio, video, thought). "
        "`thought` im Ausgang = Modell liefert seinen Denkprozess als separates "
        "`reasoning_content`-Feld._",
        "",
        "> **Kontextfenster, Parametergröße, Anbieter, Lizenz, Datenschutz-Tier und "
        "Reasoning-/Capability-Details** liefert die API nicht (zuverlässig) — dafür die "
        f"GWDG-Doku nutzen: <{GWDG_MODELS_DOC}>. Dort stehen auch externe Modelle "
        "(z. B. Claude, GPT), die am selben Endpoint laufen, aber nicht im Live-Katalog erscheinen.",
        "",
        "## Embedding-Modelle",
        "",
        "> Nicht über `/v1/models` auflistbar — nur via `/v1/embeddings` mit bekannter ID "
        "erreichbar. Latenz / Dimension / Verfügbarkeit siehe `gwdg_status.md`.",
        "",
        "| Modell-ID |",
        "|---|",
    ]
    for mid in EMBEDDING_MODELS:
        lines.append(f"| `{mid}` |")
    lines.append("")
    return "\n".join(lines)


def render_status_md(results, base_url: str, timeout: int, embeddings=None) -> str:
    lines = [
        "# GWDG Chat-AI — Status / Latenz-Probe",
        "",
        f"> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **{_now()}**.",
        f"> Quelle: `{base_url}` · eine neutrale Sanity-Anfrage (kalt) pro Modell.",
        f"> Timeout {timeout}s. Latenz = eine Anfrage, kalt (kein Mittelwert).",
        "",
        "| Modell | Latenz | demand | Tools | Sanity |",
        "|---|--:|--:|:--:|:--:|",
    ]
    for r in results:
        lat = f"{r.lat:.1f}s" if r.lat is not None else "-"
        demand = "" if r.demand is None else str(r.demand)
        sane = r.sane + (f" — {r.err}" if r.err else "")
        lines.append(f"| `{r.id}` | {lat} | {demand} | {r.tools} | {sane} |")
    if embeddings:
        lines += [
            "",
            "## Embedding-Modelle",
            "",
            "| Modell | Latenz | Dim | Verfügbarkeit |",
            "|---|--:|--:|:--:|",
        ]
        for e in embeddings:
            lat = f"{e.lat:.1f}s" if e.lat is not None else "-"
            dim = e.dim if e.dim is not None else ""
            avail = "OK" if not e.err else f"ERR — {e.err}"
            lines.append(f"| `{e.id}` | {lat} | {dim} | {avail} |")
    lines += [
        "",
        "**Legende:** `demand` = Auslastung zu Probe-Beginn (höher = stärker ausgelastet; "
        "Skala undokumentiert). `Tools` Y = Modell löste bei einem Test-Tool (`get_weather`) "
        "einen `tool_call` aus, `n` = direkt geantwortet, `ERR` = Fehler. `Sanity` OK = "
        "korrekte Ein-Wort-Antwort (Paris), WRONG/ERR = unerwartet/Fehler. Hohe Latenz oder "
        "`ERR` ⇒ überlastet oder down.",
        "",
    ]
    return "\n".join(lines)
