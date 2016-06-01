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


class RootDir12(RootDir):

    def __init__(self, path, begin, sector_bytes):
        super(RootDir12, self).__init__(path, begin, sector_bytes)


class RootDir16(RootDir):

    def __init__(self, path, begin, sector_bytes):
        super(RootDir16, self).__init__(path, begin, sector_bytes)


class RootDir32(RootDir):

    def __init__(self, path, begin, sector_bytes):
        super(RootDir32, self).__init__(path, begin, sector_bytes)
