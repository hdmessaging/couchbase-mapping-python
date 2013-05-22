"""
Customize exception class that will display some
useful information.
"""
MEMCACHED_STATUS_INVALID_ARGUMENTS = 4


class Error(Exception):
    def __init__(self, msg="", parent=None):
        self.parent_error = parent
        self.msg = msg

    def __str__(self):
        return self.msg


class NotFoundError(Error):
    pass


class InvalidArgumentError(Error):
    pass
