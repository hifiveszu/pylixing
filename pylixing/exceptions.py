# -*- coding: utf-8 -*-
from .util import utf8


class LixingException(Exception):
    """Base exception class"""


class ConnectionError(LixingException):
    """ConnectionError raised by requests"""


class LixingAPIError(LixingException):
    """Exception class used when an API request failure happens."""

    def __init__(self, code, message):
        self.code = utf8(code)
        self.message = utf8(message)
        super(LixingAPIError, self).__init__(message)

    def __str__(self):
        return '<LixingAPIError ("%s", "%s")>' % (self.code, self.message)
