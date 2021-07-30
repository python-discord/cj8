from cryptography.fernet import Fernet
from prompt_toolkit.shortcuts import (
    button_dialog,
    checkboxlist_dialog,
    input_dialog,
    message_dialog,
    yes_no_dialog,
)
from prompt_toolkit.styles import Style

from grand_geckos.database.DBWorker import DatabaseWorker
from grand_geckos.database.exceptions import AuthenticationError, UserAlreadyExistsError
from grand_geckos.database.models import Credential
from grand_geckos.ui.dashboard import get_app as dashboard_app
from grand_geckos.utils.password_checker import check_password
from grand_geckos.utils.password_generator import generate_password

dialog_style = Style.from_dict(
    {
        "dialog": "bg:#ffa500",
        "dialog frame.label": "bg:#000000 #ffff00",
        "dialog.body": "bg:#000000 #ffff00",
        "dialog shadow": "bg:#111111",
        "button.focused": "bg:#ffa500 #ffffcc",
        "text-area": "bg:#111111 #ffffaa",
    }
)
ERROR_DIALOG_TITLE = "Oops, something went wrong❗"
ERROR_DIALOG_MESSAGE_MENU = "Returning to menu..💥"
ERROR_DIALOG_MESSAGE_MAIN_MENU = "Returning to main menu..💥"


def main_menu(worker: DatabaseWorker, vault_key: Fernet, text_pass: str) -> None:
    result = button_dialog(
        style=dialog_style,
        title="Done! 👏",
        text="Access your saved credentials 🔓, Add ➕  a new one or Delete ❌ them.",
        buttons=[("Vault", True), ("Add", False), ("Delete", ...), ("Exit", None)],
    ).run()
    if result is True:
        dashboard_app(worker, vault_key).run()
        main_menu(worker, vault_key, text_pass)
    elif result is None:
        exit()
    elif result is ...:
        results_array = checkboxlist_dialog(
            style=dialog_style,
            title="Delete Credentials",
            text="Choose the credentials you would like to delete",
            values=[
                (cred.id, vault_key.decrypt((cred.credential_name.encode("utf-8"))).decode("utf-8"))
                for cred in worker.user.credentials
            ],
        ).run()
        if not results_array:
            main_menu(worker, vault_key, text_pass)
        else:
            result = worker.delete_credentials(results_array, user=worker.user)
            if not result:
                message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MENU).run()
                main_menu(worker, vault_key, text_pass)
            else:
                message_dialog(style=dialog_style, title="Success! ✅", text="Credential(s) deleted..").run()
                main_menu(worker, vault_key, text_pass)

    elif result is False:
        text_credential_name = input_dialog(
            style=dialog_style,
            title="What would you like to name this credential? (eg. Github Work, Raspberry Pi4, SSH-hobby)",
            text="",
        ).run()
        if not text_credential_name:
            message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MENU).run()
            main_menu(worker, vault_key, text_pass)
        text_credential_username = input_dialog(
            style=dialog_style, title="Username - Credential", text="Please type in the username for the credential"
        ).run()
        if not text_credential_username:
            message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MENU).run()
            main_menu(worker, vault_key, text_pass)
        strong_password = yes_no_dialog(
            style=dialog_style, title="Password", text="Would you like to generate a strong password?"
        ).run()
        if strong_password:
            text_credential_password = generate_password(length=35)
        else:
            text_credential_password = input_dialog(
                style=dialog_style,
                title="Password - Credential",
                text="Please type in the password for the credential",
                password=True,
            ).run()

        if not text_credential_password:
            message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MENU).run()
            main_menu(worker, vault_key, text_pass)
        text_platform = input_dialog(
            style=dialog_style, title="Credential Platform (eg. github.com, mail.google.com, ssh)", text=""
        ).run()
        if not text_platform:
            message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MENU).run()
            main_menu(worker, vault_key, text_pass)
        cred = Credential(
            credential_name=text_credential_name,
            actual_password=text_pass,
            credential_username=text_credential_username,
            platform=text_platform,
            credential_password=text_credential_password,
            user=worker.user,
        )
        worker.append_credential(cred)
        main_menu(worker, vault_key, text_pass)


def run_app_init() -> None:
    """Function that contains dialogs of Auth interactions such as Login,Register"""
    while True:
        result = button_dialog(
            style=dialog_style,
            title="🔥Welcome to the Secret Crate of Grand Geckos!🔥 ",
            text="Please choose an option.",
            buttons=[("Register", True), ("Login", False), ("Exit", None)],
        ).run()
        # Registration Process - Register
        if result is True:
            text_username = input_dialog(
                style=dialog_style, title="Register - Username", text="Please type your username"
            ).run()
            if not text_username:
                message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MENU).run()
                continue
            text_pass = input_dialog(
                style=dialog_style, title="Register - Password", text="Please type your password:", password=True
            ).run()
            if not text_pass:
                message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MENU).run()
                continue
            text_pass_confirm = input_dialog(
                style=dialog_style,
                title="Register - Password-Confirm",
                text="Please type your password again:",
                password=True,
            ).run()
            if not text_pass_confirm:
                message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MENU).run()
                continue
            if text_pass != text_pass_confirm:
                message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text="Passwords must match.").run()
                continue
            check_pass = check_password(text_pass)
            if check_pass:
                check = button_dialog(
                    style=dialog_style,
                    title="Your password is not strong!",
                    text="Do you want to confirm without changing your password?\n - "
                    + "\n -".join([str(issue) for issue in check_pass]),
                    buttons=[
                        ("Yes", True),
                        ("No", False),
                    ],
                ).run()
                if not check:
                    continue

            try:
                worker = DatabaseWorker.create_user(
                    username=text_username, password=text_pass, password_confirm=text_pass_confirm
                )
            except UserAlreadyExistsError as e:
                message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=str(e)).run()
                continue

            vault_key = worker.vault_key(worker.user, text_pass)
            message_dialog(style=dialog_style, title="Successful registration! ✅", text="").run()
            main_menu(worker, vault_key, text_pass)
        # Login Process - Login
        elif result is False:
            text_username = input_dialog(
                style=dialog_style, title="Login - Username", text="Please type your username"
            ).run()
            if not text_username:
                message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MAIN_MENU).run()
                continue
            text_pass = input_dialog(
                style=dialog_style, title="Login - Password", text="Please type your password:", password=True
            ).run()
            if not text_pass:
                message_dialog(style=dialog_style, title=ERROR_DIALOG_TITLE, text=ERROR_DIALOG_MESSAGE_MAIN_MENU).run()
                continue
            try:
                worker = DatabaseWorker.auth_user(username=text_username, password=text_pass)
            except AuthenticationError as e:
                message_dialog(style=dialog_style, title="Error!", text=str(e)).run()
                continue

            vault_key = worker.vault_key(worker.user, text_pass)
            message_dialog(style=dialog_style, title="Successful login! ✅", text="").run()
            main_menu(worker, vault_key, text_pass)
        # Exit
        elif result is None:
            exit()
