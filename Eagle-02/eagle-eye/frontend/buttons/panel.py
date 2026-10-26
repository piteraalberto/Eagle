"""All the buttons of the interface: drawing, clicks and state queries."""


class ButtonPanel:
    """Turns clicks into toggles and notifies listeners as listener(button_id, is_on).

    Button ids are assigned in list order, starting from 1.
    """

    def __init__(self, buttons, redraw):
        self.buttons = list(buttons)
        for number, button in enumerate(self.buttons, start=1):
            button.id = number
        self._redraw = redraw
        self._listeners = []

    def subscribe(self, listener):
        self._listeners.append(listener)

    def get_button(self, button_id):
        return next(b for b in self.buttons if b.id == button_id)

    def get_state(self, button_id):
        return self.get_button(button_id).on

    def draw(self, view):
        for button in self.buttons:
            button.draw(view)

    def click(self, x, y):
        """Toggle the topmost button under the base-space point (x, y)."""
        for button in reversed(self.buttons):
            if button.contains(x, y):
                button.on = not button.on
                self._redraw()
                is_on = button.on  # the same value goes to every listener
                for listener in self._listeners:
                    listener(button.id, is_on)
                break
