"""Fonts: Figma sizes (em, in base pixels) converted to Tk pixel sizes."""

import tkinter.font as tkfont
from functools import lru_cache

FONT_FAMILY = "Roboto Mono"
# Tk has no medium/semibold weights, so those are separate installed font families.
FONTS = {
    "regular": (FONT_FAMILY, "normal"),
    "medium": ("Roboto Mono Medium", "normal"),
    "semibold": ("Roboto Mono SemiBold", "normal"),
    "bold": (FONT_FAMILY, "bold"),
}
ROBOTO_MONO_LINESPACE = 2701 / 2048  # (ascent + descent) / em, from the font metrics


@lru_cache(maxsize=None)
def _em_ratio(family, style):
    """Ratio between a Tk pixel font size and the font's em size (cached per font)."""
    probe = tkfont.Font(family=family, size=-100, weight=style)
    return probe.metrics("linespace") / 100 / ROBOTO_MONO_LINESPACE


def tk_font(weight, size, scale):
    """Tk font tuple for a Figma font size (em, in base pixels) at the given scale."""
    family, style = FONTS[weight]
    pixels = max(1, round(size * scale / _em_ratio(family, style)))
    return family, -pixels, style
