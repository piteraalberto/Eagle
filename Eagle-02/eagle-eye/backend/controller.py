"""USB controller reader (pygame): feeds the JoystickModel and the InputLog.

Call poll() periodically from the thread that owns the interface (see App.every):
it reads the pending events and updates the model and the log. Analog sticks only move
the model; buttons and the hat switch also write a line in the log.

Axis numbers depend on the controller: adjust STICK_AXES if the sticks do not match.
"""

import os

# Must be set before importing pygame: no real video system (it would only interfere
# with Tk) and joystick events even when the window of another program has the focus.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS", "1")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame  # noqa: E402

from backend.input_events import format_button, format_hat  # noqa: E402

# (x axis, y axis) of each stick, in the order JOYSTICK 01, JOYSTICK 02.
STICK_AXES = ((0, 1), (2, 3))
BUTTON_NAMES = {}  # optional labels by button number (from 1), e.g. {2: "Abort"}


class Controller:
    def __init__(self, model, log, stick_axes=STICK_AXES, button_names=None):
        self.model = model
        self.log = log
        self.stick_axes = stick_axes
        self.button_names = BUTTON_NAMES if button_names is None else button_names
        self.joystick = None
        pygame.display.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self._open(0)

    def _open(self, device_index):
        self.joystick = pygame.joystick.Joystick(device_index)
        self.log.add("LOG", f"Controller connected: {self.joystick.get_name()}")

    def _close(self):
        self.joystick = None
        self.model.set_positions([(0.0, 0.0)] * len(self.model.sticks))
        self.log.add("LOG", "Controller disconnected")

    def poll(self):
        """Handle the pending events, then refresh the position of the sticks."""
        for event in pygame.event.get():
            self._handle(event)
        self._update_sticks()

    def _handle(self, event):
        if event.type == pygame.JOYDEVICEADDED and self.joystick is None:
            self._open(event.device_index)
        elif event.type == pygame.JOYDEVICEREMOVED and self.joystick is not None:
            if event.instance_id == self.joystick.get_instance_id():
                self._close()
        elif event.type == pygame.JOYBUTTONDOWN:
            number = event.button + 1
            self.log.add("EVT_BTN", format_button(number, self.button_names.get(number)))
        elif event.type == pygame.JOYHATMOTION:
            message = format_hat(event.hat, event.value)
            if message:  # None when the hat returns to the center
                self.log.add("EVT_POV", message)

    def _axis(self, index):
        if index >= self.joystick.get_numaxes():
            return 0.0
        return self.joystick.get_axis(index)

    def _update_sticks(self):
        if self.joystick is None:
            return
        self.model.set_positions(
            [(self._axis(ax), self._axis(ay)) for ax, ay in self.stick_axes])
