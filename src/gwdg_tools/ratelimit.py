"""Time-of-day-aware client-side rate limiter for the GWDG API.

Server limits: 2/s, 60/min. As a courtesy during German business hours we
self-throttle to 15/min. A single shared limiter gates every outbound call.
"""
import os
import time
from collections import deque
from datetime import datetime
from zoneinfo import ZoneInfo

DAYTIME_LIMIT = 15        # calls/min during business hours
OFFPEAK_LIMIT = 60        # calls/min otherwise (server hard cap)
DAYTIME_START = 7         # 07:00 inclusive
DAYTIME_END = 19          # 19:00 exclusive
MIN_INTERVAL = 0.5        # seconds between calls (2/s server cap)
DEFAULT_TZ = "Europe/Berlin"


class RateLimiter:
    """Sliding-window limiter with a per-second guard and a time-of-day cap."""

    def __init__(self, now_fn=None, sleep=time.sleep, daytime_limit=DAYTIME_LIMIT,
                 offpeak_limit=OFFPEAK_LIMIT, min_interval=MIN_INTERVAL, tz=None):
        self._tz = ZoneInfo(tz or os.environ.get("GWDG_RATE_TZ", DEFAULT_TZ))
        self._now_fn = now_fn or (lambda: datetime.now(self._tz))
        self._sleep = sleep
        self._daytime = daytime_limit
        self._offpeak = offpeak_limit
        self._min_interval = min_interval
        self._calls: deque[float] = deque()
        self._last = 0.0
        self._notified = False

    def current_limit(self) -> int:
        hour = self._now_fn().hour
        return self._daytime if DAYTIME_START <= hour < DAYTIME_END else self._offpeak

    def wait(self) -> None:
        limit = self.current_limit()
        if not self._notified:
            # ASCII only (Windows cp1252): hyphen, not en-dash.
            print(f"[RateLimiter] active: {limit}/min "
                  f"(07:00-19:00 {self._tz.key} -> {self._daytime}/min, else {self._offpeak}/min)")
            self._notified = True

        now = self._now_fn().timestamp()
        # per-second guard
        gap = now - self._last
        if 0 <= gap < self._min_interval:
            self._sleep(self._min_interval - gap)
            now = self._now_fn().timestamp()
        # per-minute sliding window
        while self._calls and now - self._calls[0] > 60:
            self._calls.popleft()
        if len(self._calls) >= limit:
            sleep_for = 60 - (now - self._calls[0])
            if sleep_for > 0:
                self._sleep(sleep_for)
                now = self._now_fn().timestamp()
            while self._calls and now - self._calls[0] > 60:
                self._calls.popleft()
        self._calls.append(now)
        self._last = now


_limiter = RateLimiter()


def wait() -> None:
    """Gate the shared singleton limiter (used by probes at each API call)."""
    _limiter.wait()
