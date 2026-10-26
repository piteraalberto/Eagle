"""Text of the input log: pure functions, no pygame and no tkinter.

Every function returns the message part of a log line, e.g. "[BTN_02] PRESSED (Abort)".
"""

import math

# Hat switch directions by angle (0 = North, clockwise).
HAT_DIRECTIONS = {
    0: "North/Up",
    45: "North-East/Up-Right",
    90: "East/Right",
    135: "South-East/Down-Right",
    180: "South/Down",
    225: "South-West/Down-Left",
    270: "West/Left",
    315: "North-West/Up-Left",
}


def hat_angle(value):
    """Angle in degrees (0 = North/Up, clockwise) of a hat value (x, y); None when centered."""
    x, y = value
    if x == 0 and y == 0:
        return None
    return round(math.degrees(math.atan2(x, y))) % 360


def format_hat(hat_index, value):
    """Message of a hat switch movement; None when the hat returns to the center."""
    angle = hat_angle(value)
    if angle is None:
        return None
    name = "HAT_SWITCH" if hat_index == 0 else f"HAT_SWITCH_{hat_index}"
    return f"[{name}] angle={angle}deg ({HAT_DIRECTIONS.get(angle, '?')})"


def format_button(number, label=None):
    """Message of a controller button press (`number` starts from 1)."""
    suffix = f" ({label})" if label else ""
    return f"[BTN_{number:02d}] PRESSED{suffix}"


def format_ui_button(button_id, label):
    """Message of a click on a dashboard button."""
    return f"[UI_{button_id:02d}] PRESSED ({label})"
