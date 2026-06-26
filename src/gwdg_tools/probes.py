"""Probe functions for the GWDG Chat-AI API: catalog, latency, health, full probe."""
import time
from dataclasses import dataclass

from openai import OpenAI

# Neutral, model-agnostic sanity prompt with a checkable one-word answer.
SANITY_SYS = "Antworte extrem knapp, nur das Noetigste."
SANITY_USER = "Was ist die Hauptstadt von Frankreich? Antworte mit einem Wort."
SANITY_EXPECTED = "paris"


def list_models(client: OpenAI) -> list[dict]:
    """Return sorted model metadata from the live /v1/models catalog."""
    rows = []
    for m in client.models.list().data:
        d = m.model_dump() if hasattr(m, "model_dump") else dict(m)
        rows.append(
            {"id": d.get("id", ""), "owned_by": d.get("owned_by", "") or "", "created": d.get("created")}
        )
    rows.sort(key=lambda r: r["id"])
    return rows


@dataclass
class ProbeResult:
    id: str
    lat: float | None = None
    finish: str = ""
    reasoning: bool = False
    r_len: int = 0
    out_len: int = 0
    tok_in: int | None = None
    tok_out: int | None = None
    sane: str = ""  # OK / WRONG / ERR
    err: str = ""


def _sanity(text: str) -> str:
    return "OK" if SANITY_EXPECTED in (text or "").lower() else "WRONG"


def probe_model(client: OpenAI, model_id: str, timeout: int = 600, max_tokens: int | None = None) -> ProbeResult:
    """One representative call against a model; records latency, finish, reasoning, tokens, sanity."""
    msgs = [{"role": "system", "content": SANITY_SYS}, {"role": "user", "content": SANITY_USER}]
    res = ProbeResult(id=model_id)
    t = time.time()
    try:
        kw: dict = {"model": model_id, "messages": msgs, "timeout": timeout}
        if max_tokens is not None:
            kw["max_tokens"] = max_tokens
        r = client.chat.completions.create(**kw)
        res.lat = time.time() - t
        ch = r.choices[0]
        content = (ch.message.content or "").strip()
        rc = getattr(ch.message, "reasoning_content", None)
        res.finish = ch.finish_reason or ""
        res.reasoning = bool(rc)
        res.r_len = len(rc) if rc else 0
        res.out_len = len(content)
        if r.usage:
            res.tok_in = r.usage.prompt_tokens
            res.tok_out = r.usage.completion_tokens
        res.sane = _sanity(content)
    except Exception as e:  # noqa: BLE001 - any failure means "unavailable", record it
        res.lat = time.time() - t
        res.err = str(e)[:60]
        res.sane = "ERR"
    return res


def probe_catalog(client, timeout=600, sleep=3.0, max_tokens=None, models=None, on_result=None):
    """Probe every model (or a given subset) once. `sleep` is rate-limit courtesy between calls."""
    ids = models or [r["id"] for r in list_models(client)]
    results = []
    for i, mid in enumerate(ids):
        res = probe_model(client, mid, timeout=timeout, max_tokens=max_tokens)
        results.append(res)
        if on_result:
            on_result(res)
        if sleep and i < len(ids) - 1:
            time.sleep(sleep)
    return results


def latency(client, models, timeout=60, max_tokens=20, on_result=None):
    """Fast latency variant: short, capped output, no inter-call sleep."""
    return probe_catalog(client, timeout=timeout, sleep=0, max_tokens=max_tokens, models=models, on_result=on_result)


def health_check(client, models, n=8, timeout=60):
    """Hit each model N times; report ok/err counts and avg latency (panel-wide outage detection)."""
    results = []
    msgs = [{"role": "user", "content": "Antworte nur mit OK."}]
    for m in models:
        ok = err = 0
        lats, errs = [], []
        for _ in range(n):
            t = time.time()
            try:
                r = client.chat.completions.create(model=m, messages=msgs, timeout=timeout)
                lats.append(time.time() - t)
                _ = r.choices[0].message.content
                ok += 1
            except Exception as e:  # noqa: BLE001
                err += 1
                errs.append(str(e)[:40])
        avg = sum(lats) / len(lats) if lats else None
        results.append({"id": m, "ok": ok, "err": err, "n": n, "avg_lat": avg, "errs": errs})
    return results
