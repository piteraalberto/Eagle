"""INPUT box: the latest input events, newest at the bottom, drawn from a backend InputLog."""

from frontend.theme import GREEN, WHITE

# ----- layout (base 2560x1440 pixels) -----
FRAME = (2135, 1112, 386, 66)    # green frame
FRAME_BORDER = 2
TEXT_X, TEXT_Y = 2137, 1115      # top-left corner of the text box (381 x 60)
TEXT_W, TEXT_H = 381, 60
LINES = 4
LINE_H = TEXT_H // LINES

FONT_SIZE = 11
FONT_WEIGHT = "medium"
CHAR_ADVANCE = 0.6               # Roboto Mono character width / font size
MAX_CHARS = int(TEXT_W / (FONT_SIZE * CHAR_ADVANCE))  # longer lines are cut to stay in the box


class InputLogView:
    def __init__(self, log):
        self.log = log

    def draw(self, view):
        x, y, w, h = FRAME
        view.outline(x, y, w, h, GREEN, FRAME_BORDER)
        for row, line in enumerate(list(self.log.lines)[-LINES:]):
            view.text(TEXT_X, TEXT_Y + row * LINE_H, TEXT_W, LINE_H, line[:MAX_CHARS], WHITE,
                      FONT_SIZE, FONT_WEIGHT)
