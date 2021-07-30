from cryptography.fernet import Fernet
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import HorizontalLine, Label

from grand_geckos.database.DBWorker import DatabaseWorker
from grand_geckos.ui import controls
from grand_geckos.ui.widgets import (
    ButtonView,
    ControlBarView,
    HorizontalSpacer,
    PanelView,
    TitleView,
    VerticalSpacer,
)


def handle_button(password, id):
    def handle_button_inside():
        PyperclipClipboard().set_text(password)
        title.content = FormattedTextControl(
            [("class:title bold", f"🔥SECRET CRATE OF GRAND GECKOS(Password Copied![{id}]) ✅ 🔥")]
        )
        return

    return handle_button_inside


title = TitleView(text="🔥 SECRET CRATE OF GRAND GECKOS 🔥")


def generate_root(worker: DatabaseWorker, vault_key: Fernet):
    credentials = worker.user.credentials

    root = HSplit(
        [
            HorizontalSpacer(),
            title,
            HorizontalLine(),
            HorizontalLine(),
            HorizontalSpacer(),
            VSplit(
                [
                    VerticalSpacer(),
                    PanelView(
                        title="Platform",
                        data=[
                            Label(
                                vault_key.decrypt(cred.platform.encode("utf-8")).decode("utf-8"),
                            )
                            for cred in credentials
                        ],
                    ),
                    VerticalSpacer(),
                    PanelView(
                        title="Name:Username",
                        data=[
                            Label(
                                vault_key.decrypt(cred.credential_name.encode("utf-8")).decode("utf-8")
                                + ":"
                                + vault_key.decrypt(cred.credential_username.encode("utf-8")).decode("utf-8"),
                            )
                            for cred in credentials
                        ],
                    ),
                    VerticalSpacer(),
                    PanelView(
                        title="Password",
                        data=[
                            ButtonView(
                                style="bold italic",
                                text="COPY PASSWORD💢",
                                action=handle_button(
                                    id=cred.id,
                                    password=vault_key.decrypt(cred.credential_password.encode("utf-8")).decode(
                                        "utf-8"
                                    ),
                                ),
                            )
                            for cred in credentials
                        ],
                    ),
                    VerticalSpacer(),
                ],
                style="fg: ansiblack",
            ),
            HorizontalSpacer(),
            ControlBarView(
                controls=[
                    ButtonView(text="Back to Menu: Ctrl+Q", action=controls.exit_app, width=32),
                ],
                style="fg: ansiblack",
            ),
            HorizontalSpacer(),
        ],
        style="bg:#ffa500 fg: ansiblack",
    )
    return root
