"""CLI for gwdg-tools: probe the GWDG Chat-AI API (catalog, latency, health)."""
import argparse
import sys
from pathlib import Path

from . import probes, render
from .client import create_client


def _base_url(client) -> str:
    return str(client.base_url).rstrip("/")


def _split_models(arg):
    return [m.strip() for m in arg.split(",") if m.strip()] if arg else None


def _write(path: str, text: str, n: int) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"\nGeschrieben: {out} ({n} Modelle).")


def cmd_models(args):
    client = create_client()
    rows = probes.list_models(client)
    print(f"{len(rows)} Modelle im GWDG-Katalog:")
    for r in rows:
        cap = ",".join(r.get("input") or [])
        print(f"  {r['id']:36s} [{cap}]")
    if not args.no_write:
        _write(args.out, render.render_models_md(rows, _base_url(client)), len(rows))


def cmd_probe(args):
    client = create_client()
    models = _split_models(args.models)
    print(f"Probe (timeout={args.timeout}s, sleep={args.sleep}s) ...\n")
    hdr = f"{'model':36s} {'lat':>7s} {'finish':>8s} {'dmd':>3s} {'status':>6s} {'tool':>4s}  sanity"
    print(hdr)
    print("-" * len(hdr))

    def show(res):
        lat = f"{res.lat:.1f}s" if res.lat is not None else "-"
        tail = res.err if res.err else res.sane
        dmd = "" if res.demand is None else str(res.demand)
        print(
            f"{res.id:36s} {lat:>7s} {res.finish:>8s} "
            f"{dmd:>3s} {res.status:>6s} {res.tools:>4s}  {tail}",
            flush=True,
        )

    rows, headers = probes.list_models_with_meta(client)
    catalog = {m["id"]: m for m in rows}
    results = probes.probe_catalog(
        client, timeout=args.timeout, sleep=args.sleep, max_tokens=args.max_tokens,
        models=models, on_result=show, catalog=catalog, tools=not args.no_tools,
    )

    embeddings = None
    if not args.no_embeddings:
        print("\nEmbeddings:")
        def show_e(e):
            lat = f"{e.lat:.1f}s" if e.lat is not None else "-"
            print(f"  {e.id:34s} {lat:>7s}  dim={e.dim or '-'}  {e.err or 'OK'}", flush=True)
        embeddings = probes.probe_embeddings(client, timeout=args.timeout, on_result=show_e)

    snap = probes.ratelimit_snapshot(headers)
    if not args.no_write:
        text = render.render_status_md(results, _base_url(client), args.timeout,
                                       embeddings=embeddings, ratelimit=snap)
        _write(args.out, text, len(results))


def cmd_latency(args):
    client = create_client()
    models = _split_models(args.models) or [r["id"] for r in probes.list_models(client)]
    print(f"{'model':40s} {'latency':>9s}  sanity")
    print("-" * 60)

    def show(res):
        lat = f"{res.lat:.1f}s" if res.lat is not None else "-"
        print(f"{res.id:40s} {lat:>9s}  {res.err or res.sane}", flush=True)

    probes.latency(client, models, timeout=args.timeout, max_tokens=args.max_tokens, on_result=show)


def cmd_health(args):
    client = create_client()
    models = _split_models(args.models) or [r["id"] for r in probes.list_models(client)]
    print(f"Health: {len(models)} Modelle x {args.n} Calls (timeout={args.timeout}s)\n")
    for r in probes.health_check(client, models, n=args.n, timeout=args.timeout):
        avg = f"{r['avg_lat']:.1f}s" if r["avg_lat"] is not None else "-"
        tag = "  <-- DEGRADED" if r["err"] else ""
        print(f"{r['id']:32s}  ok={r['ok']:2d}/{r['n']}  err={r['err']:2d}  avg_lat={avg}{tag}")
        for e in r["errs"][:3]:
            print(f"      err: {e}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gwdg", description="Probe the GWDG Chat-AI API.")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("models", help="List the live catalog and write the models Markdown.")
    m.add_argument("--out", default="docs/gwdg_models.md")
    m.add_argument("--no-write", action="store_true", help="Print only, do not write the MD.")
    m.set_defaults(func=cmd_models)

    pr = sub.add_parser("probe", help="One representative call per model -> status Markdown.")
    pr.add_argument("--out", default="docs/gwdg_status.md")
    pr.add_argument("--timeout", type=int, default=600)
    pr.add_argument("--sleep", type=float, default=0.0, help="Extra pause between models (limiter already paces; default 0).")
    pr.add_argument("--no-embeddings", action="store_true", help="Skip the embedding-model probes.")
    pr.add_argument("--no-tools", action="store_true", help="Skip the per-model tool-calling probe.")
    pr.add_argument("--max-tokens", type=int, default=None)
    pr.add_argument("--models", default=None, help="Comma-separated subset (default: whole catalog).")
    pr.add_argument("--no-write", action="store_true")
    pr.set_defaults(func=cmd_probe)

    la = sub.add_parser("latency", help="Quick latency table (print only).")
    la.add_argument("--models", default=None, help="Comma-separated subset (default: whole catalog).")
    la.add_argument("--timeout", type=int, default=60)
    la.add_argument("--max-tokens", type=int, default=20)
    la.set_defaults(func=cmd_latency)

    he = sub.add_parser("health", help="Repeated-call error rate per model (print only).")
    he.add_argument("--models", default=None, help="Comma-separated subset (default: whole catalog).")
    he.add_argument("--n", type=int, default=8)
    he.add_argument("--timeout", type=int, default=60)
    he.set_defaults(func=cmd_health)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
