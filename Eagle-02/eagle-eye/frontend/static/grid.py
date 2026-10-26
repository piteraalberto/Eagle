"""Grid lines that frame the panels."""

from frontend.theme import GREEN

# (x, y, width, height) in base 2560x1440 pixels
VERTICAL_RECTANGLES = [
    (0, 0, 2, 1440),
    (528, 0, 4, 1440),
    (1028, 1102, 4, 336),
    (1528, 1102, 4, 336),
    (2028, 0, 4, 1440),
    (2176, 532, 2, 158),
    (2293, 894, 4, 204),
    (2412, 532, 2, 158),
    (2558, 0, 2, 1440),
]

HORIZONTAL_RECTANGLES = [
    (0, 0, 2560, 2),
    (0, 78, 2560, 4),
    (2032, 282, 526, 4),
    (2032, 326, 526, 2),
    (2, 418, 526, 4),
    (2032, 486, 526, 4),
    (2032, 530, 526, 2),
    (2032, 690, 526, 4),
    (2, 758, 526, 4),
    (2, 798, 526, 2),
    (2032, 894, 526, 4),
    (0, 1098, 2560, 4),
    (2, 1138, 1026, 2),
    (2, 1402, 526, 2),
    (0, 1438, 2560, 2),
]

GRID_RECTANGLES = VERTICAL_RECTANGLES + HORIZONTAL_RECTANGLES


class Grid:
    def __init__(self, rectangles=GRID_RECTANGLES, color=GREEN):
        self.rectangles = list(rectangles)
        self.color = color

    def draw(self, view):
        for x, y, w, h in self.rectangles:
            view.rect(x, y, w, h, self.color)
