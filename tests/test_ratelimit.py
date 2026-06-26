"""Unit tests for the time-of-day-aware RateLimiter (no network, injected clock)."""
from datetime import datetime, timedelta

import pytest
from zoneinfo import ZoneInfo

from gwdg_tools.ratelimit import RateLimiter

TZ = ZoneInfo("Europe/Berlin")


class FakeClock:
    """Controllable clock: now() returns a fixed datetime; sleep() advances it."""
    def __init__(self, start: datetime):
        self.dt = start
        self.slept: list[float] = []

    def now(self) -> datetime:
        return self.dt

    def sleep(self, secs: float) -> None:
        self.slept.append(secs)
        self.dt = self.dt + timedelta(seconds=secs)


def _limiter(clock, **kw):
    return RateLimiter(now_fn=clock.now, sleep=clock.sleep, **kw)


@pytest.mark.parametrize("hour,expected", [
    (6, 60), (7, 15), (12, 15), (18, 15), (19, 60), (23, 60), (0, 60),
])
def test_cap_by_hour(hour, expected):
    clock = FakeClock(datetime(2026, 6, 26, hour, 0, tzinfo=TZ))
    rl = _limiter(clock)
    assert rl.current_limit() == expected


def test_daytime_blocks_16th_call_within_minute():
    clock = FakeClock(datetime(2026, 6, 26, 10, 0, tzinfo=TZ))  # daytime -> 15/min
    rl = _limiter(clock, min_interval=0.0)
    for _ in range(15):
        rl.wait()
    assert clock.slept == []          # first 15 do not sleep
    rl.wait()                          # 16th must wait out the window
    assert len(clock.slept) == 1
    assert abs(clock.slept[0] - 60) < 1.0


def test_offpeak_allows_60_blocks_61st():
    clock = FakeClock(datetime(2026, 6, 26, 2, 0, tzinfo=TZ))   # off-peak -> 60/min
    rl = _limiter(clock, min_interval=0.0)
    for _ in range(60):
        rl.wait()
    assert clock.slept == []
    rl.wait()
    assert len(clock.slept) == 1
    assert abs(clock.slept[0] - 60) < 1.0


def test_min_interval_enforced():
    clock = FakeClock(datetime(2026, 6, 26, 2, 0, tzinfo=TZ))
    rl = _limiter(clock, min_interval=0.5)
    rl.wait()              # first call: no spacing sleep
    assert clock.slept == []
    rl.wait()              # immediate second call: must space by 0.5s
    assert clock.slept == [0.5]
