#!/usr/bin/env python2

import struct
import datetime
from . import error


class RootEntry(object):

    ENTRY_SIZE = 32

    class AttrFlag(object):

        READ_ONLY = 0x01
        HIDDEN = 0x02
        SYSTEM_FILE = 0x04
        VOLUME_LABEL = 0x08
        LONG_FILE_NAME = 0x0f
        DIRECTORY = 0x10
        ARCHIVE = 0x20


    # Caller to ensure the `buf` is the valid root entry
    def __init__(self, buf):
        self.name = buf[:11]
        self.attr = buf[11]
        time_val = struct.unpack('<H', buf[22:24])[0]
        date_val = struct.unpack('<H', buf[24:26])[0]
        print('time: {0}:{1}:{2}'.format(time_val>>11,
                                  (time_val>>5)&0x003f,
                                  time_val&0x001f))
        print('date: {0}-{1}-{2}'.format(date_val>>9,
                                         (date_val>>5)&0x000f,
                                         date_val&0x001f))
        # self.ctime
        # self.cdate
        # self.addr
        # self.filesize
        

class RootDirs(object):

    def __init__(self, path, begin, max_entries):
        self._fd = open(path, 'rw+')
        self._fd.seek(begin)
        self._begin = begin
        self._max = max_entries
        self._entries = []

    def __del__(self):
        if not self._fd:
            self._fd.close()

    def build_entries(self):
        raise NotImplementedError


class RootDirs12(RootDirs):

    def __init__(self, path, begin, max_entries):
        super(RootDirs12, self).__init__(path, begin, max_entries)

    def build_entries(self):
        self._entries[:] = []
        self._fd.seek(self._begin + 32)
        buf = self._fd.read(RootEntry.ENTRY_SIZE)
        self._entries.append(RootEntry(buf))


class RootDirs16(RootDirs):

    def __init__(self, path, begin, max_entries):
        super(RootDirs16, self).__init__(path, begin, max_entries)


class RootDirs32(RootDirs):

    def __init__(self, path, begin, max_entries):
        super(RootDirs32, self).__init__(path, begin, max_entries)
