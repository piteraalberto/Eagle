"""The interface: window and layers wired to the backend."""

from frontend.buttons.ai_controls import AiControls
from frontend.buttons.button_log import ButtonLog
from frontend.buttons.layout import AI_PAUSE_BUTTON, AI_START_BUTTON, BUTTONS
from frontend.buttons.panel import ButtonPanel
from frontend.inputs.threshold_input import ThresholdInput
from frontend.static.grid import Grid
from frontend.static.texts import Texts
from frontend.widgets.ai_chart import AiChart
from frontend.widgets.input_log_view import InputLogView
from frontend.widgets.joystick_view import JoystickPanel
from frontend.window import Window


class App:
    """`on_button_change(button_id, is_on)` is called on every button click."""

    def __init__(self, model, joystick, input_log, on_button_change, title="Frontend"):
        self.window = Window(title)
        self.root = self.window.root
        self.buttons = ButtonPanel(BUTTONS, self.window.redraw)

        ai_controls = AiControls(model, AI_PAUSE_BUTTON, AI_START_BUTTON)
        self.buttons.subscribe(ai_controls.on_button_change)
        self.buttons.subscribe(ButtonLog(self.buttons, input_log).on_button_change)
        self.buttons.subscribe(on_button_change)
        model.subscribe(self.window.redraw)
        joystick.subscribe(self.window.redraw)
        input_log.subscribe(self.window.redraw)

        # Drawing order, back to front.
        for layer in (Grid(), Texts(), self.buttons, AiChart(model),
                      ThresholdInput(self.window.canvas, model), InputLogView(input_log),
                      JoystickPanel(joystick)):
            self.window.add_layer(layer)
        self.window.on_click = self.buttons.click

    def get_button_state(self, button_id):
        return self.buttons.get_state(button_id)

    def every(self, interval_ms, callback):
        """Call `callback()` every `interval_ms` from the Tk loop (no threads)."""
        def tick():
            try:
                callback()
            finally:
                self.root.after(interval_ms, tick)
        self.root.after(interval_ms, tick)

    def run(self):
        self.window.run()
