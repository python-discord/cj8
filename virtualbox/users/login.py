from virtualbox.functions.blessed_functions import echo, request
from virtualbox.exceptions import InvalidLoginOrPassword
from copy import copy


def login(Users, term):
    while True:
        login = request("login: ", term)
        password = request("password: ", term)

        if login in Users and Users[login].checkPassword(password):
            return copy(Users[login])
        echo(InvalidLoginOrPassword().args[0], term)
