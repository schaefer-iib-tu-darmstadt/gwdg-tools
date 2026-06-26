from gwdg_tools.probes import ProbeResult
from gwdg_tools.render import render_models_md, render_status_md


def _model(mid, output):
    return {"id": mid, "name": mid, "input": ["text"], "output": output,
            "demand": 0, "status": "ready", "owned_by": "chat-ai", "created": 0}


def test_models_md_is_live_api_only():
    """No curated reasoning column; output modalities (incl. thought) stay verbatim,
    and details the API lacks are delegated to the GWDG docs."""
    rows = [
        _model("deepseek-r1", ["text", "thought"]),
        _model("teuken-7b-instruct-research", ["text"]),
    ]
    md = render_models_md(rows, "https://x/v1")
    assert "| Reasoning |" not in md        # curated column dropped
    assert "Y (inline)" not in md
    assert "Y (separat)" not in md
    assert "text, thought" in md            # raw output modality preserved
    assert "docs.hpc.gwdg.de" in md         # pointer to the docs for the rest


def test_status_md_has_no_denkstream_column():
    results = [ProbeResult(id="m1", lat=0.5, sane="OK", demand=0)]
    md = render_status_md(results, "https://x/v1", 600)
    assert "Denk-Stream" not in md


def test_status_md_drops_noise_columns_and_ratelimit():
    """finish/status columns are constant noise; the rate-limit footer is account
    data that must not be published."""
    md = render_status_md([ProbeResult(id="m1", lat=0.5, sane="OK", demand=0)],
                          "https://x/v1", 600)
    assert "finish" not in md
    assert "Rate-Limit" not in md


def test_status_md_tools_column():
    results = [
        ProbeResult(id="m1", lat=0.5, sane="OK", demand=0, tools="Y"),
        ProbeResult(id="m2", lat=0.5, sane="OK", demand=0, tools="ERR"),
    ]
    md = render_status_md(results, "https://x/v1", 600)
    assert "Tools" in md          # header present
    assert "| Y |" in md          # m1 tool cell
    assert "| ERR |" in md        # m2 tool cell
