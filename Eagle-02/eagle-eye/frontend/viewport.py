"""Window resizing: maps the fixed 2560x1440 base space onto the canvas.

All coordinates in the interface are base pixels. The base area is scaled uniformly
to fit the window and centered (letterboxed) when the window is not 16:9.
"""

from dataclasses import dataclass

BASE_W, BASE_H = 2560, 1440


@dataclass(frozen=True)
class Viewport:
    scale: float
    ox: float  # canvas position of the base-space origin
    oy: float

    @classmethod
    def fit(cls, width, height):
        scale = min(width / BASE_W, height / BASE_H)
        return cls(scale, (width - BASE_W * scale) / 2, (height - BASE_H * scale) / 2)

    def to_canvas(self, x, y):
        return self.ox + x * self.scale, self.oy + y * self.scale

    def to_base(self, px, py):
        return (px - self.ox) / self.scale, (py - self.oy) / self.scale
