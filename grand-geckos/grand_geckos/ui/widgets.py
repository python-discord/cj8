from typing import Callable, List, Optional

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.layout.containers import (
    AnyContainer,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import Box, Button, Frame, SearchToolbar, TextArea

from grand_geckos.ui.bindings import bottombar_bindings, panel_bindings


class VerticalDivider(Window):
    def __init__(self) -> None:
        super().__init__(width=1, char="│", style="class:line")


class HorizontalDivider(Window):
    def __init__(self) -> None:
        super().__init__(height=1, char="─", style="class:line")


class VerticalSpacer(Window):
    def __init__(self, width=1) -> None:
        super().__init__(width=width, char=" ", style="class:line")


class HorizontalSpacer(Window):
    def __init__(self, height=1) -> None:
        super().__init__(height=height, char=" ", style="class:line")


class TitleView(Window):
    def __init__(self, text: str) -> None:
        super().__init__(
            height=2,
            content=FormattedTextControl([("class:title bold", text)]),
            align=WindowAlign.CENTER,
        )


class SearchBarView(TextArea):
    def __init__(self) -> None:
        super().__init__(
            height=1,
            prompt=" Search: ",
            style="class:input-field",
            multiline=False,
            wrap_lines=False,
            search_field=SearchToolbar(),
        )


class PanelView(Frame):
    def __init__(
        self,
        data: List[AnyContainer],
        title: AnyFormattedText,
    ) -> None:
        super().__init__(
            title=title,
            body=Box(body=HSplit(data, padding=1), padding=1, height=D()),
            key_bindings=panel_bindings(),
        )


class ControlBarView(Frame):
    def __init__(self, controls: Optional[List[AnyContainer]] = None, *, style: str = "") -> None:
        super().__init__(
            body=Box(body=VSplit(controls or [], align="CENTER", padding=2), style="class:bottom-bar", height=1),
            style=style,
            key_bindings=bottombar_bindings(),
        )


class ButtonView(Box):
    def __init__(self, text: str, action: Callable[[], None], style: str = "class:button", width: int = 16) -> None:

        super().__init__(
            body=Button(
                text=text,
                handler=action,
                width=width,
                left_symbol="",
                right_symbol="",
            ),
            style=style,
            height=1,
        )
