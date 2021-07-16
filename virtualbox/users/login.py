from copy import copy

from virtualbox.exceptions import InvalidLoginOrPassword
from virtualbox.functions.blessed_functions import echo, request


def login(Users, term):
    while True:
        login = request("login: ", term)
        password = request("password: ", term)

        if login in Users and Users[login].checkPassword(password):
            return copy(Users[login])
        echo(InvalidLoginOrPassword().args[0], term)
