"""Analog stick graphs: target with dead zone and live position, drawn from a JoystickModel."""

from frontend.theme import GREEN, RED, YELLOW, with_opacity

# ----- layout (base 2560x1440 pixels) -----
JOYSTICK_ORIGINS = ((2071, 1228), (2321, 1228))  # top-left corner of each graph (50 px apart)
SIZE = 200                      # square side = diameter of the outer circle = full range
BORDER = 2                      # square and rings, drawn inside their area
RING_DIAMETERS = (200, 150, 100, 50)
CROSSHAIR = True                # axes through the center, as in the reference screenshot
CENTER_DOT = 4                  # filled green dot in the center
POSITION_DOT = 10               # red dot following the physical stick
STICK_RADIUS = SIZE / 2         # distance of the dot from the center at full deflection
LINE_WIDTH = 2

DEADZONE_OPACITY = 0.5          # the red circle is 50% transparent over the black background


class JoystickView:
    """One graph. `stick` has x, y (-1..1, y downward) and deadzone (percent)."""

    def __init__(self, stick, x, y):
        self.stick = stick
        self.x = x
        self.y = y
        self.cx = x + SIZE / 2  # center of the graph
        self.cy = y + SIZE / 2

    def draw(self, view):
        self._draw_deadzone(view)
        self._draw_target(view)
        self._draw_position(view)

    def _circle(self, view, diameter, cx=None, cy=None, **style):
        cx = self.cx if cx is None else cx
        cy = self.cy if cy is None else cy
        view.oval(cx - diameter / 2, cy - diameter / 2, diameter, diameter, **style)

    def _draw_deadzone(self, view):
        """Red circle whose diameter grows linearly: 0% = none, 100% = the whole graph."""
        diameter = SIZE * self.stick.deadzone / 100
        if diameter > 0:
            self._circle(view, diameter, fill=with_opacity(RED, DEADZONE_OPACITY))

    def _draw_target(self, view):
        view.outline(self.x, self.y, SIZE, SIZE, GREEN, BORDER)
        if CROSSHAIR:
            view.rect(self.x, self.cy - BORDER / 2, SIZE, BORDER, GREEN)
            view.rect(self.cx - BORDER / 2, self.y, BORDER, SIZE, GREEN)
        for diameter in RING_DIAMETERS:
            self._circle(view, diameter, outline=GREEN, thickness=BORDER)

    def _draw_position(self, view):
        px = self.cx + self.stick.x * STICK_RADIUS
        py = self.cy + self.stick.y * STICK_RADIUS
        # drawing order: yellow line first, so both dots stay on top of it
        if (px, py) != (self.cx, self.cy):
            view.line([(self.cx, self.cy), (px, py)], YELLOW, LINE_WIDTH)
        self._circle(view, CENTER_DOT, fill=GREEN)
        self._circle(view, POSITION_DOT, cx=px, cy=py, fill=RED)


class JoystickPanel:
    """Both graphs."""

    def __init__(self, model, origins=JOYSTICK_ORIGINS):
        self.views = [JoystickView(stick, x, y) for stick, (x, y) in zip(model.sticks, origins)]

    def draw(self, view):
        for joystick in self.views:
            joystick.draw(view)
