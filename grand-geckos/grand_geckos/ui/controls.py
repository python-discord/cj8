from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding.key_processor import KeyPressEvent


def exit_app(event: KeyPressEvent = None):
    if event is not None:
        event.app.exit()
    else:
        get_app().exit()
