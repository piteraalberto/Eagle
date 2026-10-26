"""Button definition.

Each button is a rectangle with a linked, centered text box. Buttons are defined
column by column; the text box is derived from the rectangle with a horizontal inset.
"""

from dataclasses import dataclass

from frontend.theme import GREEN, with_opacity

BUTTON_HEIGHT = 26
ROW_PITCH = 36          # vertical distance between two buttons of a column
TEXT_OFFSET_Y = 3       # text box top, relative to the button top
TEXT_HEIGHT = 20
BORDER = 2              # border thickness in base pixels (drawn inside the rectangle)
PRESSED_OPACITY = 0.5   # opacity of a button while it is ON


@dataclass
class Button:
    # rectangle: top-left corner + size (base 2560x1440 pixels)
    x: int
    y: int
    w: int
    h: int
    # linked text box (same fields as TextBox)
    text: str
    text_x: int
    text_y: int
    text_w: int
    text_h: int
    size: int = 15
    weight: str = "bold"    # "regular", "medium", "semibold" or "bold"
    align: str = "center"   # "left", "center" or "right"
    color: str = GREEN      # text color
    border_color: str = GREEN
    id: int = 0             # assigned by ButtonPanel (1, 2, 3, ...)
    on: bool = False        # False = off, True = on (drawn at 50% opacity)

    def contains(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h

    def draw(self, view):
        opacity = PRESSED_OPACITY if self.on else 1.0
        border = with_opacity(self.border_color, opacity)
        view.outline(self.x, self.y, self.w, self.h, border, BORDER)
        view.text(self.text_x, self.text_y, self.text_w, self.text_h, self.text,
                  with_opacity(self.color, opacity), self.size, self.weight, self.align)


def make_button(text, x, y, w, inset, color=GREEN):
    """Button whose text box is the rectangle shrunk by `inset` pixels on the left and right."""
    return Button(x=x, y=y, w=w, h=BUTTON_HEIGHT, text=text,
                  text_x=x + inset, text_y=y + TEXT_OFFSET_Y,
                  text_w=w - 2 * inset, text_h=TEXT_HEIGHT,
                  color=color, border_color=color)


def column(x, y0, w, inset, labels, colors=None):
    """Vertical stack of buttons starting at y0; `colors` maps a row index to a color."""
    colors = colors or {}
    return [make_button(label, x, y0 + i * ROW_PITCH, w, inset, colors.get(i, GREEN))
            for i, label in enumerate(labels)]
