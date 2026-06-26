"""Render probe results into the Markdown reports under docs/."""
from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _fmt_created(val) -> str:
    if not val:
        return ""
    try:
        return datetime.fromtimestamp(int(val), tz=timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, OSError, TypeError):
        return str(val)


def render_models_md(rows: list[dict], base_url: str) -> str:
    lines = [
        "# GWDG Chat-AI — verfügbare Modelle",
        "",
        f"> Auto-generiert von `gwdg models` (gwdg-tools) — Stand **{_now()}**.",
        f"> Quelle: `{base_url}/models` (OpenAI-kompatibler Endpoint).",
        f"> Aktuell **{len(rows)} Modelle** im Katalog.",
        "",
        "| Modell-ID | Anbieter | Erstellt |",
        "|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| `{r['id']}` | {r['owned_by']} | {_fmt_created(r['created'])} |")
    lines.append("")
    return "\n".join(lines)


def render_status_md(results, base_url: str, timeout: int) -> str:
    lines = [
        "# GWDG Chat-AI — Status / Latenz-Probe",
        "",
        f"> Auto-generiert von `gwdg probe` (gwdg-tools) — Stand **{_now()}**.",
        f"> Quelle: `{base_url}` · eine neutrale Sanity-Anfrage (kalt) pro Modell.",
        f"> Timeout {timeout}s. Latenz = eine Anfrage, kalt (kein Mittelwert).",
        "",
        "| Modell | Latenz | finish | Reasoning | r_len | out_len | tok in/out | Sanity |",
        "|---|--:|---|:--:|--:|--:|--:|:--:|",
    ]
    for r in results:
        lat = f"{r.lat:.1f}s" if r.lat is not None else "-"
        tin = r.tok_in if r.tok_in is not None else ""
        tout = r.tok_out if r.tok_out is not None else ""
        sane = r.sane + (f" — {r.err}" if r.err else "")
        lines.append(
            f"| `{r.id}` | {lat} | {r.finish} | {'Y' if r.reasoning else 'n'} | "
            f"{r.r_len} | {r.out_len} | {tin}/{tout} | {sane} |"
        )
    lines += [
        "",
        "**Legende:** Reasoning Y = Modell emittiert einen (unsichtbaren) Denk-Stream "
        "→ langsamer/teurer pro Call. Sanity `OK` = korrekte Ein-Wort-Antwort (Paris), "
        "`WRONG` = unerwartete Ausgabe, `ERR` = Fehler/Timeout (Meldung in der Spalte). "
        "Hohe Latenz oder `ERR` ⇒ Modell aktuell überlastet oder nicht verfügbar.",
        "",
    ]
    return "\n".join(lines)
