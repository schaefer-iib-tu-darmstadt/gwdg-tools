"""Probe functions for the GWDG Chat-AI API: catalog, latency, health, full probe."""
import time
from dataclasses import dataclass
from typing import TypedDict

from openai import OpenAI, RateLimitError

from . import ratelimit


def _guarded(call):
    """Rate-limit and apply one 429 retry around a single API call."""
    for attempt in (0, 1):
        ratelimit.wait()
        try:
            return call()
        except RateLimitError as e:
            if attempt == 1:
                raise
            reset = 1.0
            try:
                reset = float(e.response.headers.get("ratelimit-reset", 1))
            except Exception:
                pass
            time.sleep(max(reset, 0.5))

# Neutral, model-agnostic sanity prompt with a checkable one-word answer.
SANITY_SYS = "Antworte extrem knapp, nur das Noetigste."
SANITY_USER = "Was ist die Hauptstadt von Frankreich? Antworte mit einem Wort."
SANITY_EXPECTED = "paris"


class ModelInfo(TypedDict):
    id: str
    name: str
    input: list[str]
    output: list[str]
    demand: int | None
    status: str
    owned_by: str
    created: int | None


def _to_modelinfo(m) -> ModelInfo:
    d = m.model_dump() if hasattr(m, "model_dump") else dict(m)
    return {
        "id": d.get("id", ""),
        "name": d.get("name", "") or "",
        "input": list(d.get("input") or []),
        "output": list(d.get("output") or []),
        "demand": d.get("demand"),
        "status": d.get("status", "") or "",
        "owned_by": d.get("owned_by", "") or "",
        "created": d.get("created"),
    }


def list_models_with_meta(client):
    """Catalog rows plus the raw response headers (for the rate-limit snapshot)."""
    raw = _guarded(lambda: client.models.with_raw_response.list())
    rows = [_to_modelinfo(m) for m in raw.parse().data]
    rows.sort(key=lambda r: r["id"])
    return rows, raw.headers


def list_models(client) -> list[ModelInfo]:
    """Return sorted model metadata from the live /v1/models catalog (dicts)."""
    rows, _ = list_models_with_meta(client)
    return rows


def modalities(m: ModelInfo) -> str:
    return ", ".join(m.get("input") or [])


# Windows the server reports via x-ratelimit-*-{window} headers, tightest first.
RATELIMIT_WINDOWS = ("second", "minute", "hour", "day", "month")


def ratelimit_snapshot(headers) -> dict:
    """Extract (remaining, limit) per window from x-ratelimit-* response headers.

    Returns an ordered dict keyed by window (tightest first); windows the server
    does not report are omitted. These numbers are account-specific -- callers
    must keep them out of any committed file (see CLAUDE.md / repo is public).
    """
    snap = {}
    for k in RATELIMIT_WINDOWS:
        rem = headers.get(f"x-ratelimit-remaining-{k}")
        lim = headers.get(f"x-ratelimit-limit-{k}")
        if rem is not None and lim is not None:
            snap[k] = (str(rem), str(lim))
    return snap


def get_ratelimit(client) -> dict:
    """Read the account's live rate limits via one cheap /v1/models call.

    Returns the ratelimit_snapshot dict. Uses the shared limiter/429 retry like
    every other probe. Account-specific -- print only, never write to docs/.
    """
    raw = _guarded(lambda: client.models.with_raw_response.list())
    return ratelimit_snapshot(raw.headers)


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
    demand: int | None = None
    status: str = ""
    tools: str = ""  # Y / n / ERR


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
        r = _guarded(lambda: client.chat.completions.create(**kw))
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


def probe_catalog(client, timeout=600, sleep=0.0, max_tokens=None, models=None,
                  on_result=None, catalog=None, tools=False):
    """Probe every model (or a subset) once; sleep is courtesy spacing between calls.

    tools=True adds one extra tool-calling probe per model (sets ProbeResult.tools).
    """
    if catalog is None:
        catalog = {m["id"]: m for m in list_models(client)}
    ids = models or list(catalog.keys())
    results = []
    for i, mid in enumerate(ids):
        res = probe_model(client, mid, timeout=timeout, max_tokens=max_tokens)
        info = catalog.get(mid, {})
        res.demand = info.get("demand")
        res.status = info.get("status", "")
        # Skip the tool probe if the sanity call already failed: the model is down,
        # and a second long call would just double the timeout wait.
        if tools and not res.err:
            res.tools = probe_tool_call(client, mid, timeout=timeout)
        results.append(res)
        if on_result:
            on_result(res)
        if sleep and i < len(ids) - 1:
            time.sleep(sleep)
    return results


def latency(client, models, timeout=60, max_tokens=20, on_result=None):
    """Fast latency variant: short, capped output, no inter-call sleep.

    Passes catalog={} so probe_catalog does not fetch the catalog for demand/status
    (which latency does not render) -- `models` is always given here, so no extra call.
    """
    return probe_catalog(client, timeout=timeout, sleep=0, max_tokens=max_tokens,
                         models=models, on_result=on_result, catalog={})


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
                r = _guarded(lambda: client.chat.completions.create(model=m, messages=msgs, timeout=timeout))
                lats.append(time.time() - t)
                _ = r.choices[0].message.content
                ok += 1
            except Exception as e:  # noqa: BLE001
                err += 1
                errs.append(str(e)[:40])
        avg = sum(lats) / len(lats) if lats else None
        results.append({"id": m, "ok": ok, "err": err, "n": n, "avg_lat": avg, "errs": errs})
    return results


# Embedding models are NOT listable via /v1/models (verified). Known-id list,
# validated by an actual /embeddings call. Maintain manually when GWDG adds models.
EMBEDDING_MODELS = [
    "e5-mistral-7b-instruct",
    "multilingual-e5-large-instruct",
    "qwen3-embedding-4b",
]
EMBED_INPUT = "Hauptstadt von Frankreich"


TOOL_PROBE = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}]
TOOL_PROBE_PROMPT = "What's the weather in Paris right now?"


def probe_tool_call(client, model_id: str, timeout: int = 60) -> str:
    """'Y' if the model emits a tool_call for a simple tool, 'n' if it answers
    directly, 'ERR' on failure."""
    try:
        r = _guarded(lambda: client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": TOOL_PROBE_PROMPT}],
            tools=TOOL_PROBE, tool_choice="auto", timeout=timeout))
        ch = r.choices[0]
        return "Y" if (ch.finish_reason == "tool_calls" or ch.message.tool_calls) else "n"
    except Exception:  # noqa: BLE001 - any failure = unknown/unsupported
        return "ERR"


@dataclass
class EmbeddingResult:
    id: str
    lat: float | None = None
    dim: int | None = None
    err: str = ""


def probe_embedding(client, model_id: str, timeout: int = 60) -> EmbeddingResult:
    """One embeddings call; records latency, vector dimension, availability."""
    res = EmbeddingResult(id=model_id)
    t = time.time()
    try:
        r = _guarded(lambda: client.embeddings.create(
            model=model_id, input=EMBED_INPUT, timeout=timeout))
        res.lat = time.time() - t
        res.dim = len(r.data[0].embedding)
    except Exception as e:  # noqa: BLE001 - any failure means "unavailable"
        res.lat = time.time() - t
        res.err = str(e)[:60]
    return res


def probe_embeddings(client, models=None, timeout: int = 60, on_result=None):
    """Probe each known embedding model once."""
    ids = models or EMBEDDING_MODELS
    out = []
    for mid in ids:
        res = probe_embedding(client, mid, timeout=timeout)
        out.append(res)
        if on_result:
            on_result(res)
    return out
