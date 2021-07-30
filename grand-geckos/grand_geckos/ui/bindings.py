from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

from grand_geckos.ui import controls


def _get_bindings(next_key, prev_key):
    bindings = KeyBindings()
    bindings.add(next_key)(focus_next)
    bindings.add(prev_key)(focus_previous)
    return bindings


def global_bindings(next_key="tab", prev_key="s-tab"):
    bindings = _get_bindings(next_key=next_key, prev_key=prev_key)
    bindings.add("c-q", eager=True)(controls.exit_app)
    return bindings


def panel_bindings(next_key="down", prev_key="up"):
    bindings = _get_bindings(next_key=next_key, prev_key=prev_key)
    return bindings


def bottombar_bindings(next_key="right", prev_key="left"):
    bindings = _get_bindings(next_key=next_key, prev_key=prev_key)
    return bindings
