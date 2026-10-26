"""Writes every click on a dashboard button in the input log."""

from backend.input_events import format_ui_button


class ButtonLog:
    def __init__(self, panel, log):
        self.panel = panel
        self.log = log

    def on_button_change(self, button_id, _is_on):
        """Listener for ButtonPanel.subscribe."""
        label = self.panel.get_button(button_id).text
        self.log.add("EVT_UI", format_ui_button(button_id, label))
