#!/usr/bin/python

class Error(Exception):
    pass


class FormatError(Error):
    def __init__(self, message):
        super(FormatError, self).__init__()
        self._message = message

    def __str__(self):
        return 'Error occurred: {}'.format(self._message)
