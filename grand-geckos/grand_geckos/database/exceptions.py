from sqlalchemy.exc import ArgumentError


class UserAlreadyExistsError(ArgumentError):
    pass


class AuthenticationError(ArgumentError):
    pass
