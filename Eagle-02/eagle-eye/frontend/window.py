"""Tk window: full-screen toggle, resize handling and click routing."""

import sys
import tkinter as tk

from frontend.theme import BLACK, OUTSIDE
from frontend.view import View
from frontend.viewport import BASE_H, BASE_W, Viewport


def enable_dpi_awareness():
    """Prevent Windows display scaling from blurring or resizing the window."""
    if sys.platform == "win32":
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()


class Window:
    """Full-screen window with one canvas; every resize redraws all the layers."""

    def __init__(self, title="Frontend"):
        enable_dpi_awareness()  # must run before tk.Tk()
        self.root = tk.Tk()
        self.root.title(title)
        self.fullscreen = True
        self.root.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(self.root, bg=OUTSIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.layers = []      # objects exposing draw(view); drawn in order, the last one on top
        self.on_click = None  # callback(x, y) with the click position in base coordinates

        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.canvas.bind("<Configure>", lambda _: self.redraw())
        self.canvas.bind("<Button-1>", self._handle_click)

    def add_layer(self, layer):
        self.layers.append(layer)

    def toggle_fullscreen(self, _=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, _=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def viewport(self):
        return Viewport.fit(self.canvas.winfo_width(), self.canvas.winfo_height())

    def redraw(self):
        view = View(self.canvas, self.viewport())
        view.clear()
        view.rect(0, 0, BASE_W, BASE_H, BLACK)
        for layer in self.layers:
            layer.draw(view)

    def _handle_click(self, event):
        self.canvas.focus_set()  # leaves any text input that has the keyboard focus
        if self.on_click:
            self.on_click(*self.viewport().to_base(event.x, event.y))

    def run(self):
        self.root.mainloop()
