"""
Customize exception class that will display some
useful information.
"""


class NotFoundError(Exception):
    def __init__(self, msg="", parent=None):
        self.parent_error = parent
        self.msg = msg

    def __str__(self):
        return self.msg
