"""AI model panel: inference confidence chart, drawn from a backend AiModel."""

from dataclasses import dataclass

from backend.ai_model import clamp01
from frontend.theme import BLACK, GREEN, RED, YELLOW, with_opacity

# ----- layout (base 2560x1440 pixels) -----
CHART_X = 52
CHART_W = 460
GRAPH_X = 71       # the inference line starts here (reference lines start at CHART_X)
GRAPH_END = 491    # ...and ends here, so a centered marker label never leaves the chart
GRAPH_W = GRAPH_END - GRAPH_X
Y_AT_ONE = 528     # vertical center of the 1.00 level
Y_AT_ZERO = 688    # vertical center of the 0.00 level (baseline)

LABEL_W, LABEL_H = 27, 15
LABEL_X = 19       # scale labels are centered in the 12..52 gutter left of the chart
SCALE_VALUES = (1.00, 0.75, 0.50, 0.25, 0.00)

MARKER_SIZE = 10
MARKER_GAP = 3                  # distance between the data point and the marker tip
MARKER_BACKGROUND = (35, 10)    # black rectangle behind each marker value label

LINE_WIDTH = 2


@dataclass
class TickGroup:
    """Vertical tick marks sharing the same y, size and opacity (base pixels)."""
    xs: tuple
    y: int
    w: int
    h: int
    opacity: float = 0.5
    color: str = GREEN


# Drawn in this order: the short ticks first, so the tall ones stay on top where they coincide.
TICK_GROUPS = [
    TickGroup(xs=tuple(range(71, 512, 20)), y=678, w=2, h=9),   # x = 71, 91, ..., 511
    TickGroup(xs=(151, 251, 351, 451), y=668, w=2, h=21),
]


@dataclass
class ReferenceLine:
    """Horizontal line across the chart at a given value."""
    value: float
    color: str = GREEN
    opacity: float = 0.5
    thickness: int = 2
    extend_left: int = 0   # extra pixels added on the left side of the line


# Baseline (0.00) plus one divider at each scale level, all with the same style.
# To add more lines, append e.g. ReferenceLine(0.9).
REFERENCE_LINES = [ReferenceLine(value) for value in SCALE_VALUES]


def value_to_y(value):
    """Vertical position of a 0..1 value, proportional between the 0.00 and 1.00 levels."""
    return Y_AT_ZERO - (Y_AT_ZERO - Y_AT_ONE) * clamp01(value)


class AiChart:
    def __init__(self, model, reference_lines=None):
        self.model = model
        self.reference_lines = list(REFERENCE_LINES if reference_lines is None else reference_lines)

    def draw(self, view):
        self._draw_reference_lines(view)
        self._draw_ticks(view)
        self._draw_scale_labels(view)
        self._draw_threshold(view)
        self._draw_graph(view)
        self._draw_extremes(view)

    def _draw_reference_lines(self, view):
        for line in self.reference_lines:
            y = value_to_y(line.value) - line.thickness / 2
            view.rect(CHART_X - line.extend_left, y, CHART_W + line.extend_left, line.thickness,
                      with_opacity(line.color, line.opacity))

    def _draw_ticks(self, view):
        for group in TICK_GROUPS:
            color = with_opacity(group.color, group.opacity)
            for x in group.xs:
                view.rect(x, group.y, group.w, group.h, color)

    def _visible_scale_values(self):
        """Scale levels whose label does not collide with the threshold label."""
        threshold_y = value_to_y(self.model.threshold)
        return [v for v in SCALE_VALUES if abs(value_to_y(v) - threshold_y) >= LABEL_H]

    def _draw_scale_labels(self, view):
        for value in self._visible_scale_values():
            view.text(LABEL_X, value_to_y(value) - LABEL_H / 2, LABEL_W, LABEL_H,
                      f"{value:.2f}", GREEN, 11, "regular", "center")

    def _draw_threshold(self, view):
        threshold = self.model.threshold
        y = value_to_y(threshold)
        view.rect(CHART_X, y - 1, CHART_W, 2, RED)
        view.text(LABEL_X, y - LABEL_H / 2, LABEL_W, LABEL_H,
                  f"{threshold:.2f}", RED, 11, "medium", "center")

    def _point(self, index):
        values = self.model.values
        step = GRAPH_W / (values.maxlen - 1)
        return GRAPH_X + index * step, value_to_y(values[index])

    def _draw_graph(self, view):
        points = [self._point(i) for i in range(len(self.model.values))]
        view.line(points, YELLOW, LINE_WIDTH)

    def _draw_extremes(self, view):
        values = self.model.values
        if not values:
            return
        indices = range(len(values))
        i_min = min(indices, key=values.__getitem__)
        i_max = max(indices, key=values.__getitem__)

        # Maximum: inverted green triangle above the point, label above the triangle.
        x, y = self._point(i_max)
        top = y - MARKER_GAP - MARKER_SIZE
        self._draw_marker(view, x, GREEN, values[i_max],
                          triangle=[(x - MARKER_SIZE / 2, top), (x + MARKER_SIZE / 2, top),
                                    (x, y - MARKER_GAP)],
                          label_y=top - LABEL_H)

        # Minimum: red triangle below the point, label below the triangle.
        x, y = self._point(i_min)
        bottom = y + MARKER_GAP + MARKER_SIZE
        self._draw_marker(view, x, RED, values[i_min],
                          triangle=[(x, y + MARKER_GAP), (x - MARKER_SIZE / 2, bottom),
                                    (x + MARKER_SIZE / 2, bottom)],
                          label_y=bottom)

    def _draw_marker(self, view, x, color, value, triangle, label_y):
        label_x = x - LABEL_W / 2  # centered on the triangle
        bg_w, bg_h = MARKER_BACKGROUND
        view.rect(label_x + (LABEL_W - bg_w) / 2, label_y + (LABEL_H - bg_h) / 2, bg_w, bg_h, BLACK)
        view.polygon(triangle, color)
        view.text(label_x, label_y, LABEL_W, LABEL_H, f"{value:.2f}", color, 11, "medium", "center")
