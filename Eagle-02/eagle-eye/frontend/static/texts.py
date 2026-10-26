"""Static text boxes of the interface."""

from dataclasses import dataclass

from frontend.theme import GREEN, WHITE


@dataclass
class TextBox:
    text: str
    x: int                  # top-left corner of the box, in base 2560x1440 pixels
    y: int
    w: int                  # box width and height
    h: int
    size: int = 32          # font size in pixels
    weight: str = "bold"    # "regular", "medium", "semibold" or "bold"
    align: str = "left"     # "left", "center" or "right"
    color: str = WHITE


TEXTS = [
    TextBox("TRACKING WITH TAP NET", x=2039, y=500, w=190, h=20, size=15),
    TextBox("Do NOT press this button while the robot is armed", x=2108, y=455, w=442, h=20, size=15,
            align="right"),
    TextBox("STATUS", x=2457, y=418, w=55, h=20, size=15),
    TextBox("GPIO RASPBERRY PI ZERO 2W", x=2039, y=296, w=226, h=20, size=15),
    TextBox("GPU", x=2152, y=116, w=44, h=32, size=24, weight="semibold"),
    TextBox("VRAM", x=2152, y=216, w=58, h=32, size=24, weight="semibold"),
    TextBox("CPU", x=2330, y=116, w=44, h=32, size=24, weight="semibold"),
    TextBox("RAM", x=2330, y=216, w=44, h=32, size=24, weight="semibold"),
    TextBox("NET", x=2494, y=116, w=44, h=32, size=24, weight="semibold"),
    TextBox("SSD", x=2494, y=216, w=44, h=32, size=24, weight="semibold"),
    TextBox("EAGLE EYE", x=100, y=8, w=300, h=63, size=48, color=GREEN),
    TextBox("EVERY MACHINE IS A SMOKE MACHINE IF YOU OPERATE IT WRONG ENOUGH",
            x=556, y=19, w=1136, h=40, size=30, color=GREEN),
    TextBox("CONF THRESHOLD", x=283, y=433, w=127, h=20, size=15, color=GREEN),
    TextBox("INPUT:", x=2071, y=1112, w=55, h=20, size=15, color=GREEN),
    TextBox("JOYSTICK 01", x=2071, y=1198, w=100, h=20, size=15, color=GREEN),
    TextBox("JOYSTICK 02", x=2321, y=1198, w=100, h=20, size=15, color=GREEN),
]


class Texts:
    def __init__(self, texts=TEXTS):
        self.texts = list(texts)

    def draw(self, view):
        for t in self.texts:
            view.text(t.x, t.y, t.w, t.h, t.text, t.color, t.size, t.weight, t.align)
