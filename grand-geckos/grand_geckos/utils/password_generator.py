import secrets
import string

from grand_geckos.static import words


def generate_password(
    length: int,
    *,
    use_letters: bool = True,
    use_numbers: bool = True,
    use_symbols: bool = False,
    custom_letters: str = "",
):
    """
    Password generator.

    Uses word groups like lowercase, number, symbols to verify that each password
    generated has at least one of each type defined.

    You can also use `custom_letters` to create your own group.
    """
    if custom_letters:
        groups = [custom_letters]
    else:
        groups = []

    if use_letters:
        groups.append(string.ascii_lowercase)
        groups.append(string.ascii_uppercase)
    if use_numbers:
        groups.append(string.digits)
    if use_symbols:
        groups.append(string.punctuation)

    # Check that the length is possible to generate with one unique character
    # from each group.
    if not length >= len(groups):
        raise Exception(
            f"Length of {length!r} is too short to generate a password with"
            + " at least one unqiue character each from the currently selected"
            + " groups."
        )
    # Spessific case for if length is zero, as its not catched by the above statement.
    if length <= 0:
        raise Exception(f"Cannot generate a password of length {length!r}.")
    # Also check that we actually have a group to generate passwords from
    if len(groups) < 1:
        raise Exception("No groups to generate a password with!")

    possible_chars = "".join(groups)
    while True:
        password = "".join(secrets.choice(possible_chars) for _ in range(length))

        # Check that there is at least one character from each selected group.
        if all(any(char in password for char in group) for group in groups):
            return password


def generate_passphrase(length: int):
    """
    XKCD-style passphrase

    Generate easy to remember pass-phrases like "correct horse battery staple".
    https://xkcd.com/936/

    Should be at minimum 4 in length.
    """
    if length <= 0:
        raise Exception("Passphrase length cannot be 0 or lower!")

    password = " ".join(secrets.choice(words) for _ in range(length))
    password = password.replace("-", "").lower()
    return password
