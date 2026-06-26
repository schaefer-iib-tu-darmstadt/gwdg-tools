from gwdg_tools.probes import probe_tool_call


class _Msg:
    def __init__(self, tool_calls):
        self.tool_calls = tool_calls


class _Choice:
    def __init__(self, finish, tool_calls):
        self.finish_reason = finish
        self.message = _Msg(tool_calls)


class _Resp:
    def __init__(self, finish, tool_calls):
        self.choices = [_Choice(finish, tool_calls)]


class _Completions:
    def __init__(self, resp, exc=None):
        self._resp, self._exc = resp, exc

    def create(self, **kw):
        if self._exc:
            raise self._exc
        return self._resp


class _Chat:
    def __init__(self, resp, exc=None):
        self.completions = _Completions(resp, exc)


class FakeClient:
    def __init__(self, finish=None, tool_calls=None, exc=None):
        self.chat = _Chat(_Resp(finish, tool_calls), exc)


def test_tool_call_yes():
    assert probe_tool_call(FakeClient(finish="tool_calls", tool_calls=[object()]), "test-model") == "Y"


def test_tool_call_no():
    assert probe_tool_call(FakeClient(finish="stop", tool_calls=None), "test-model") == "n"


def test_tool_call_error():
    assert probe_tool_call(FakeClient(exc=RuntimeError("boom")), "test-model") == "ERR"


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
