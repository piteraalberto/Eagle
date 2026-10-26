"""Data of the two analog sticks: position and dead zone.

Positions are Cartesian, as sent by the controller: x grows to the right and y grows
downward (screen convention), both in -1..1. A position outside the unit circle (the
corners of the square range of some controllers) is scaled back onto the circle.

Usage:
    model = JoystickModel()
    model.set_positions([(0.5, -0.5), (0.0, 1.0)])   # one (x, y) per stick, one redraw
    model.sticks[0].deadzone = 25                    # percent, see set_deadzone
"""

import math
from dataclasses import dataclass

STICK_COUNT = 2
DEFAULT_DEADZONE = 10  # percent: 0 = no dead zone, 100 = the whole stick range


def clamp_percent(value):
    return max(0.0, min(100.0, float(value)))


def limit_to_unit_circle(x, y):
    """Scale (x, y) onto the unit circle when it lies outside of it."""
    length = math.hypot(x, y)
    return (x / length, y / length) if length > 1 else (x, y)


@dataclass
class Stick:
    x: float = 0.0
    y: float = 0.0
    deadzone: float = DEFAULT_DEADZONE  # percent of the stick range


class JoystickModel:
    def __init__(self, stick_count=STICK_COUNT, deadzone=DEFAULT_DEADZONE):
        self.sticks = [Stick(deadzone=clamp_percent(deadzone)) for _ in range(stick_count)]
        self._listeners = []

    def subscribe(self, listener):
        """Register a function called with no arguments after every change."""
        self._listeners.append(listener)

    def _notify(self):
        for listener in self._listeners:
            listener()

    def set_positions(self, positions):
        """Set the (x, y) of every stick; listeners run once, only if something changed."""
        changed = False
        for stick, (x, y) in zip(self.sticks, positions):
            x, y = limit_to_unit_circle(x, y)
            if (stick.x, stick.y) != (x, y):
                stick.x, stick.y = x, y
                changed = True
        if changed:
            self._notify()

    def set_deadzone(self, index, percent):
        """Set the dead zone (percent, clamped to 0..100) of one stick."""
        self.sticks[index].deadzone = clamp_percent(percent)
        self._notify()
