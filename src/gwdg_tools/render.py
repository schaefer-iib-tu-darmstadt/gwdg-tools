"""Render probe results into the Markdown reports under docs/."""
from datetime import datetime, timezone

from .probes import EMBEDDING_MODELS, is_reasoning


def _now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def render_models_md(rows: list[dict], base_url: str) -> str:
    lines = [
        "# GWDG Chat-AI — verfügbare Modelle",
        "",
        f"> Auto-generiert von `gwdg models` (gwdg-tools) — Stand **{_now()}**.",
        f"> Quelle: `{base_url}/models` (OpenAI-kompatibler Endpoint).",
        f"> Aktuell **{len(rows)} Chat-Modelle** im Katalog.",
        "",
        "| Modell-ID | Name | Eingang | Ausgang | Reasoning |",
        "|---|---|---|---|:--:|",
    ]
    for r in rows:
        eingang = ", ".join(r.get("input") or [])
        ausgang = ", ".join(r.get("output") or [])
        rea = "Y" if is_reasoning(r) else "n"
        lines.append(f"| `{r['id']}` | {r.get('name', '')} | {eingang} | {ausgang} | {rea} |")
    lines += [
        "",
        "_Eingang/Ausgang = Modalitäten (text/image/audio/video). "
        "Reasoning Y = Modell kann einen Denk-Stream (`thought`) ausgeben "
        "(deklarierte Fähigkeit laut Katalog; ob er pro Antwort wirklich auftritt, "
        "zeigt der Live-Probe in `gwdg_status.md`)._",
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


def _ratelimit_footer(snap: dict) -> str:
    labels = {"minute": "pro Minute", "hour": "pro Stunde", "day": "pro Tag"}
    parts = [f"{snap[k][0]}/{snap[k][1]} {lab}" for k, lab in labels.items() if k in snap]
    return ("Rate-Limit: (redacted)


def render_status_md(results, base_url: str, timeout: int, embeddings=None, ratelimit=None) -> str:
    lines = [
        "# GWDG Chat-AI — Status / Latenz-Probe",
        "",
        f"> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **{_now()}**.",
        f"> Quelle: `{base_url}` · eine neutrale Sanity-Anfrage (kalt) pro Modell.",
        f"> Timeout {timeout}s. Latenz = eine Anfrage, kalt (kein Mittelwert).",
        "",
        "| Modell | Latenz | finish | Denk-Stream | demand | status | Sanity |",
        "|---|--:|---|:--:|--:|:--:|:--:|",
    ]
    for r in results:
        lat = f"{r.lat:.1f}s" if r.lat is not None else "-"
        demand = "" if r.demand is None else str(r.demand)
        sane = r.sane + (f" — {r.err}" if r.err else "")
        lines.append(
            f"| `{r.id}` | {lat} | {r.finish} | {'Y' if r.reasoning else 'n'} | "
            f"{demand} | {r.status} | {sane} |"
        )
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
        "**Legende:** `demand` = Auslastung beim Katalog-Abruf zu Probe-Beginn (Snapshot; "
        "höher = stärker ausgelastet; Skala von GWDG nicht dokumentiert). `Denk-Stream` Y "
        "= bei dieser knappen Sanity-Anfrage tatsächlich ein Reasoning-Stream beobachtet "
        "(variiert je Prompt; deklarierte Fähigkeit siehe `gwdg_models.md`). Sanity `OK` = "
        "korrekte Ein-Wort-Antwort (Paris), `WRONG` = unerwartet, `ERR` = Fehler/Timeout. "
        "Hohe Latenz / `ERR` ⇒ überlastet oder down.",
    ]
    footer = _ratelimit_footer(ratelimit) if ratelimit else ""
    if footer:
        lines += ["", f"> {footer}"]
    lines.append("")
    return "\n".join(lines)
