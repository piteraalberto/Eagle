"""Drawing primitives: base-space shapes drawn on the canvas through a Viewport."""

from frontend.fonts import tk_font

SCENE_TAG = "scene"  # items redrawn on every frame; embedded widgets are not tagged
ANCHORS = {"left": "w", "center": "center", "right": "e"}


class View:
    def __init__(self, canvas, viewport):
        self.canvas = canvas
        self.viewport = viewport

    def clear(self):
        self.canvas.delete(SCENE_TAG)

    def rect(self, x, y, w, h, color):
        x0, y0 = self.viewport.to_canvas(x, y)
        x1, y1 = self.viewport.to_canvas(x + w, y + h)
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="", tags=SCENE_TAG)

    def outline(self, x, y, w, h, color, thickness):
        """Unfilled rectangle: four strips drawn inside the (x, y, w, h) area."""
        t = thickness
        for strip in [(x, y, w, t), (x, y + h - t, w, t), (x, y, t, h), (x + w - t, y, t, h)]:
            self.rect(*strip, color)

    def oval(self, x, y, w, h, fill=None, outline=None, thickness=2):
        """Circle/ellipse in the (x, y, w, h) area; the outline is drawn inside that area."""
        x0, y0 = self.viewport.to_canvas(x, y)
        x1, y1 = self.viewport.to_canvas(x + w, y + h)
        width = max(1, round(thickness * self.viewport.scale)) if outline else 0
        inset = width / 2  # Tk centers the outline on the edge: move it inward
        self.canvas.create_oval(x0 + inset, y0 + inset, x1 - inset, y1 - inset,
                                fill=fill or "", outline=outline or "", width=width,
                                tags=SCENE_TAG)

    def polygon(self, points, color):
        flat = [c for p in points for c in self.viewport.to_canvas(*p)]
        self.canvas.create_polygon(*flat, fill=color, outline="", tags=SCENE_TAG)

    def line(self, points, color, width=2):
        if len(points) < 2:
            return
        flat = [c for p in points for c in self.viewport.to_canvas(*p)]
        self.canvas.create_line(*flat, fill=color, width=max(1, round(width * self.viewport.scale)),
                                smooth=False, joinstyle="miter", capstyle="butt", tags=SCENE_TAG)

    def box(self, x, y, w, h):
        """Base-space box -> canvas pixels (x, y, width, height)."""
        px, py = self.viewport.to_canvas(x, y)
        return px, py, w * self.viewport.scale, h * self.viewport.scale

    def font(self, weight, size):
        return tk_font(weight, size, self.viewport.scale)

    def text(self, x, y, w, h, text, color, size, weight="bold", align="left"):
        """Single-line text vertically centered in the (x, y, w, h) box."""
        anchor_x = {"left": x, "center": x + w / 2, "right": x + w}[align]
        px, py = self.viewport.to_canvas(anchor_x, y + h / 2)
        self.canvas.create_text(px, py, text=text, fill=color, anchor=ANCHORS[align],
                                font=self.font(weight, size), tags=SCENE_TAG)
