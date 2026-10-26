"""Application entry point: builds the backend and the window, then starts the UI loop.

Run with:  python main.py      (F11 toggles full screen, Escape leaves it)
"""

from backend.ai_model import AiModel
from backend.button_logic import on_button_change
from backend.controller import Controller
from backend.input_log import InputLog
from backend.joystick_model import JoystickModel
from frontend.app import App

DEFAULT_THRESHOLD = 0.65
CONTROLLER_POLL_MS = 10  # how often the USB controller is read


def build_app():
    """Create the backend model and the window wired to it; returns (app, model)."""
    model = AiModel(threshold=DEFAULT_THRESHOLD)
    joystick = JoystickModel()
    input_log = InputLog()
    app = App(model, joystick, input_log, on_button_change)
    app.every(CONTROLLER_POLL_MS, Controller(joystick, input_log).poll)
    return app, model


def main():
    app, _model = build_app()
    app.run()  # the chart starts paused; live code calls model.push(value) after START


if __name__ == "__main__":
    main()
