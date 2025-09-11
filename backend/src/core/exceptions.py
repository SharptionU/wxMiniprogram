class UserNotExist(Exception):
    """User does not exist"""
    pass


class UserAlreadyExist(Exception):
    """User already exist"""
    pass


class UserNotAuthorized(Exception):
    """User is not authorized"""
    pass


class UserNotVerified(Exception):
    """User is not verified"""
    pass


class UserAlreadyVerified(Exception):
    """User is already verified"""
    pass


class UserAlreadyRegistered(Exception):
    """User is already registered"""
    pass


class UserNotRegistered(Exception):
    """User is not registered"""
    pass


class UserAlreadyLoggedIn(Exception):
    """User is already logged in"""
    pass


