from gwdg_tools.probes import ProbeResult
from gwdg_tools.render import render_models_md, render_status_md


def _model(mid, output):
    return {"id": mid, "name": mid, "input": ["text"], "output": output,
            "demand": 0, "status": "ready", "owned_by": "chat-ai", "created": 0}


def test_models_md_reasoning_cells():
    rows = [
        _model("deepseek-r1", ["text", "thought"]),  # separat
        _model("glm-4.7", ["text"]),                  # inline (curated)
        _model("teuken-7b-instruct-research", ["text"]),  # n
    ]
    md = render_models_md(rows, "https://x/v1")
    assert "Y (separat)" in md
    assert "Y (inline)" in md
    assert "| n |" in md


def test_status_md_has_no_denkstream_column():
    results = [ProbeResult(id="m1", lat=0.5, finish="stop", sane="OK",
                           demand=0, status="ready")]
    md = render_status_md(results, "https://x/v1", 600)
    assert "Denk-Stream" not in md


def test_status_md_tools_column():
    results = [
        ProbeResult(id="m1", lat=0.5, finish="stop", sane="OK",
                    demand=0, status="ready", tools="Y"),
        ProbeResult(id="m2", lat=0.5, finish="stop", sane="OK",
                    demand=0, status="ready", tools="ERR"),
    ]
    md = render_status_md(results, "https://x/v1", 600)
    assert "Tools" in md          # header present
    assert "| Y |" in md          # m1 tool cell
    assert "| ERR |" in md        # m2 tool cell
