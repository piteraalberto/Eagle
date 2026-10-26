"""Shared colors and small color helpers."""

BLACK = "#000000"
WHITE = "#FFFFFF"
GREEN = "#34C759"
RED = "#FF383C"
YELLOW = "#FFCC00"
OUTSIDE = "#1c1c1e"  # letterbox area when the window is not 16:9


def with_opacity(color, opacity, base=BLACK):
    """Tk has no alpha channel: simulate opacity by blending `color` over `base`."""
    fg = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    bg = [int(base[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(f * opacity + b * (1 - opacity)) for f, b in zip(fg, bg))
