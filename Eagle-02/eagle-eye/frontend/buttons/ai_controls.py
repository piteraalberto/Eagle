"""START / PAUSE buttons of the AI chart."""


class AiControls:
    """Starts and stops the AI model from its two buttons.

    Only one of the two is active (full brightness) at a time; the other one is
    dimmed to 50%. At startup the model is paused, so START is the active button.
    """

    def __init__(self, model, pause_button, start_button):
        self.model = model
        self.pause_button = pause_button
        self.start_button = start_button
        self._set_running(False)

    def _set_running(self, running):
        # In Button, on=True means "drawn at 50%": START is dimmed while the model runs,
        # PAUSE is dimmed while it is paused.
        self.start_button.on = running
        self.pause_button.on = not running
        self.model.running = running  # last: it triggers the redraw

    def on_button_change(self, button_id, _is_on):
        """Listener for ButtonPanel.subscribe."""
        if button_id == self.start_button.id:
            self._set_running(True)
        elif button_id == self.pause_button.id:
            self._set_running(False)
