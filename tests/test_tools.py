from unittest.mock import MagicMock

from gwdg_tools.probes import probe_tool_call


def _client(finish=None, tool_calls=None, exc=None):
    """Fake OpenAI client whose chat.completions.create() yields one choice
    (or raises exc)."""
    client = MagicMock()
    create = client.chat.completions.create
    if exc is not None:
        create.side_effect = exc
    else:
        choice = MagicMock(finish_reason=finish, message=MagicMock(tool_calls=tool_calls))
        create.return_value = MagicMock(choices=[choice])
    return client


def test_tool_call_yes():
    assert probe_tool_call(_client(finish="tool_calls", tool_calls=[object()]), "test-model") == "Y"


def test_tool_call_no():
    assert probe_tool_call(_client(finish="stop", tool_calls=None), "test-model") == "n"


def test_tool_call_error():
    assert probe_tool_call(_client(exc=RuntimeError("boom")), "test-model") == "ERR"


def test_probe_catalog_tools_flag(monkeypatch):
    """probe_catalog(tools=True) populates res.tools; tools=False leaves it empty
    (also guards that the per-model tool probe only runs when explicitly asked)."""
    import gwdg_tools.probes as p

    monkeypatch.setattr(p, "probe_model",
                        lambda client, mid, timeout=600, max_tokens=None: p.ProbeResult(id=mid))
    monkeypatch.setattr(p, "probe_tool_call",
                        lambda client, mid, timeout=60: "Y")

    on = p.probe_catalog(None, models=["m1"], catalog={"m1": {}}, tools=True)
    assert on[0].tools == "Y"

    off = p.probe_catalog(None, models=["m1"], catalog={"m1": {}}, tools=False)
    assert off[0].tools == ""
