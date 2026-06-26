from gwdg_tools.probes import reasoning_kind


def test_thought_channel_is_separat():
    assert reasoning_kind({"id": "deepseek-r1", "output": ["text", "thought"]}) == "separat"


def test_curated_text_only_is_inline():
    assert reasoning_kind({"id": "glm-4.7", "output": ["text"]}) == "inline"


def test_unknown_text_only_is_n():
    assert reasoning_kind({"id": "some-instruct-model", "output": ["text"]}) == "n"


def test_separat_wins_over_inline():
    # glm-4.7 is curated inline but if it ever declares thought, separat wins.
    assert reasoning_kind({"id": "glm-4.7", "output": ["text", "thought"]}) == "separat"
