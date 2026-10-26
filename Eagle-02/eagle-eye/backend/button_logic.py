"""Button logic: the frontend reports every click here."""


def on_button_change(button_id, is_on):
    """Put the button logic here: called on every click with the button id and its new state."""
    print(f"Button {button_id}: {'ON' if is_on else 'OFF'}")
