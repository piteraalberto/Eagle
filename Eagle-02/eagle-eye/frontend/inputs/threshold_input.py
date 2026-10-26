"""Confidence threshold input: type a value and press Enter to apply it."""

import re
import tkinter as tk

from frontend.theme import BLACK, GREEN

INPUT_RECT = (469, 430, 49, 26)         # green frame (base pixels)
INPUT_TEXT_BOX = (475, 433, 37, 20)     # where the Entry sits inside the frame
INPUT_BORDER = 2

# Every prefix of a valid value: "", "0", "0.", "0.3", "0.34", "1", "1.0", "1.00"
# ("," also accepted). Anything else (letters, symbols, a 3rd decimal, values above
# 1.00, "33", ...) is rejected while typing.
_PARTIAL_THRESHOLD = re.compile(r"^(0([.,]\d{0,2})?|1([.,]0{0,2})?)?$")


def is_valid_partial_threshold(text):
    return _PARTIAL_THRESHOLD.match(text) is not None


def parse_threshold(text):
    """Convert text like "0,5" to 0.5; returns None for empty text."""
    text = text.replace(",", ".")
    return float(text) if text else None


class ThresholdInput:
    def __init__(self, canvas, model):
        self.canvas = canvas
        self.model = model
        self.entry = tk.Entry(
            canvas, bd=0, highlightthickness=0, relief="flat", justify="center",
            bg=BLACK, fg=GREEN, insertbackground=GREEN,
            selectbackground=GREEN, selectforeground=BLACK,
            validate="key",
            validatecommand=(canvas.register(is_valid_partial_threshold), "%P"))
        self.window_id = canvas.create_window(0, 0, window=self.entry, anchor="nw")
        self.entry.bind("<Return>", self._commit)
        # losing the focus discards any unconfirmed text
        self.entry.bind("<FocusOut>", lambda _: self._show(model.threshold))
        self._show(model.threshold)

    def _show(self, value):
        text = f"{value:.2f}"
        if self.entry.get() != text:
            self.entry.delete(0, "end")
            self.entry.insert(0, text)

    def _commit(self, _event=None):
        value = parse_threshold(self.entry.get())
        if value is not None:
            self.model.threshold = value  # also redraws the chart
        self._show(self.model.threshold)  # normalizes "0,5" -> "0.50"
        self.canvas.focus_set()

    def draw(self, view):
        x, y, w, h = INPUT_RECT
        view.outline(x, y, w, h, GREEN, INPUT_BORDER)

        px, py, pw, ph = view.box(*INPUT_TEXT_BOX)
        self.canvas.coords(self.window_id, px, py)
        self.canvas.itemconfigure(self.window_id, width=max(1, round(pw)), height=max(1, round(ph)))
        self.entry.configure(font=view.font("bold", 15))
        if self.canvas.focus_get() is not self.entry:  # follow programmatic changes
            self._show(self.model.threshold)
