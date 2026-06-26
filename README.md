# gwdg-tools

Kleines CLI rund um die **GWDG Chat-AI** (OpenAI-kompatible API,
`https://chat-ai.academiccloud.de/v1`). Beantwortet die Fragen, die die offizielle
GWDG-Doku nur veraltet/ungenau beantwortet:

- **Welche Modelle gibt's gerade?** (Live-Katalog aus `/v1/models`)
- **Wie schnell / verfügbar ist ein Modell *jetzt*?** (selbst gemessene Latenz statt
  Doku-Versprechen — inkl. überlasteter / nicht erreichbarer Modelle)

Die Messergebnisse landen in zwei auto-generierten Markdown-Dateien unter `docs/`, die
ein GitHub-Actions-Job wöchentlich aktualisiert. Andere Projekte **verlinken** diese
Dateien einfach (kein Klonen nötig) — oder ziehen das Package als Dependency, wenn sie
die Probes programmatisch brauchen (siehe [Nutzung in anderen Projekten](#nutzung-in-anderen-projekten)).

## Generierte Reports

- [`docs/gwdg_models.md`](docs/gwdg_models.md) — aktueller Modell-Katalog (ID, Anbieter, Datum)
- [`docs/gwdg_status.md`](docs/gwdg_status.md) — Latenz / finish / Reasoning / Verfügbarkeit pro Modell

## Setup

```bash
uv sync
cp .env.example .env      # GWDG_API_KEY eintragen
```

## CLI

```bash
uv run gwdg models                       # Katalog -> docs/gwdg_models.md
uv run gwdg probe                        # eine Anfrage/Modell -> docs/gwdg_status.md (Latenz, Verfügbarkeit)
uv run gwdg latency --models gemma-3-27b-it,qwen3.5-397b-a17b   # schnelle Latenz-Tabelle (nur Ausgabe)
uv run gwdg health  --models gemma-3-27b-it --n 8              # Fehlerrate über N Calls (nur Ausgabe)
```

Nützliche Flags: `--no-write` (nur Ausgabe, keine MD), `--models a,b,c` (Subset),
`--timeout`, `--sleep` (Pause zwischen Modellen, Rate-Limit-schonend; Default 3 s),
`--out PATH` (Ziel-MD).

> **Rate-Limit:** Die GWDG-API drosselt (~15 req/min). `probe` läuft default mit
> `--sleep 3` über den ganzen Katalog — nicht aggressiv im Loop aufrufen.

## Auto-Refresh (GitHub Actions)

`.github/workflows/refresh.yml` läuft wöchentlich (+ manuell via *Run workflow*),
probt den Katalog + Latenz und committet die aktualisierten `docs/*.md` zurück.

Einmalig im Repo einrichten:
- **Settings → Secrets and variables → Actions → New repository secret:** `GWDG_API_KEY`
- (optional) **Variable** `GWDG_BASE_URL`, falls vom Default abweichend

Die publizierten MDs enthalten keine Geheimdaten (nur Modell-Liste + Latenzen) — das
Repo darf öffentlich sein; der API-Key bleibt Secret.

## Nutzung in anderen Projekten

**Variante A — nur lesen (empfohlener Default):** im README/der Doku des anderen
Projekts auf die Raw-URL der MD verlinken, z. B.

```
https://raw.githubusercontent.com/schaefer-iib-tu-darmstadt/gwdg-tools/main/docs/gwdg_status.md
```

Kein Install, kein Klonen — immer der zuletzt von CI gemessene Stand.

**Variante B — programmatisch nutzen:** das Package als Git-Dependency ziehen und die
Probes selbst aufrufen (z. B. zur Laufzeit das schnellste gesunde Modell wählen):

```bash
uv add git+https://github.com/schaefer-iib-tu-darmstadt/gwdg-tools
```

```python
from gwdg_tools.client import create_client
from gwdg_tools.probes import list_models, latency

client = create_client()                      # braucht GWDG_API_KEY in der Env
print([m["id"] for m in list_models(client)])
```

Jedes Projekt / jede Person entscheidet selbst zwischen A und B.
