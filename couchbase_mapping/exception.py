"""
Customize exception class that will display some
useful information.
"""


class BasicException(Exception):
    def __init__(self, msg="", parent=None):
        self.parent_error = parent
        self.msg = msg

    def __str__(self):
        return self.msg


class NotFoundError(BasicException):
    pass


class InvalidArgumentError(BasicException):
    pass
