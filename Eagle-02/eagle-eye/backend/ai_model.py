"""Data of the AI model panel: inference confidence values, threshold and run state.

Usage:
    model = AiModel(threshold=0.65)
    model.running = True       # while False, push() ignores new values
    model.push(0.72)           # append one inference value (clamped to 0..1)
    model.threshold = 0.8      # move the threshold (clamped to 0..1)

Listeners (see subscribe) run synchronously in the caller's thread, so with the Tk
interface attached call push() and the setters from the Tk thread, e.g. via root.after.
"""

from collections import deque

MAX_POINTS = 100


def clamp01(value):
    return max(0.0, min(1.0, float(value)))


class AiModel:
    def __init__(self, threshold=0.65, max_points=MAX_POINTS):
        self.values = deque(maxlen=max_points)  # latest inference values, oldest first
        self._threshold = clamp01(threshold)
        self._running = False  # starts paused
        self._listeners = []

    def subscribe(self, listener):
        """Register a function called with no arguments after every change."""
        self._listeners.append(listener)

    def _notify(self):
        for listener in self._listeners:
            listener()

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = clamp01(value)
        self._notify()

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running):
        self._running = running
        self._notify()

    def push(self, value):
        """Append one inference value; the oldest one is dropped when the buffer is full.

        Ignored while the model is not running.
        """
        if not self._running:
            return
        self.values.append(clamp01(value))
        self._notify()

    def set_value(self, index, value):
        """Set the value at `index` (0 = oldest); index == len(values) appends."""
        value = clamp01(value)
        if index == len(self.values):
            self.values.append(value)
        else:
            self.values[index] = value
        self._notify()

    def set_values(self, values):
        self.values.clear()
        self.values.extend(clamp01(v) for v in values)
        self._notify()
