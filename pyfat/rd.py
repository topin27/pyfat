#!/usr/bin/env python2

import struct
from . import error


class RootDir(object):

    def __init__(self, path, begin, sector_bytes):
        self._fd = open(path, 'rw+')
        self._fd.seek(begin * sector_bytes)
        self._begin = begin
        self._sector_bytes = sector_bytes

    def __del__(self):
        if not self._fd:
            self._fd.close()
