"""Last input events, shown in the INPUT box of the interface.

Usage:
    log = InputLog()
    log.add("EVT_BTN", "[BTN_02] PRESSED")   # -> "[0.000123] EVT_BTN: [BTN_02] PRESSED"
    log.lines                                # the latest lines, oldest first

Listeners (see subscribe) run synchronously in the caller's thread.
"""

import time
from collections import deque

MAX_LINES = 4


class InputLog:
    def __init__(self, max_lines=MAX_LINES, clock=time.perf_counter):
        self.lines = deque(maxlen=max_lines)  # oldest first, the newest is the last one
        self._clock = clock
        self._start = clock()
        self._listeners = []

    def subscribe(self, listener):
        """Register a function called with no arguments after every new line."""
        self._listeners.append(listener)

    def add(self, tag, message):
        """Append one line stamped with the seconds elapsed since the log was created."""
        self.lines.append(f"[{self._clock() - self._start:.6f}] {tag}: {message}")
        for listener in self._listeners:
            listener()
