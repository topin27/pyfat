#!/usr/bin/env python2

import struct
import datetime
from . import error


class RootEntry(object):

    ENTRY_SIZE = 32

    TYPE_FAT12 = 0
    TYPE_FAT16 = 1
    TYPE_FAT32 = 2

    class AttrFlag(object):

        READ_ONLY = 0x01
        HIDDEN = 0x02
        SYSTEM_FILE = 0x04
        VOLUME_LABEL = 0x08
        LONG_FILE_NAME = 0x0f
        DIRECTORY = 0x10
        ARCHIVE = 0x20


    # Caller to ensure the `buf` is the valid root entry
    def __init__(self, buf, t):
        self.name = buf[:11]
        self.attr = ord(buf[11])
        time_val = struct.unpack('<H', buf[14:16])[0]
        date_val = struct.unpack('<H', buf[16:18])[0]
        self.ctime = datetime.time(
            time_val>>11, (time_val>>5)&0x003f, time_val&0x001f
        )
        self.cdate = datetime.date(
            1980+(date_val>>9), (date_val>>5)&0x000f, date_val&0x001f
        )
        time_val = struct.unpack('<H', buf[22:24])[0]
        date_val = struct.unpack('<H', buf[24:26])[0]
        self.mtime = datetime.time(
            time_val>>11, (time_val>>5)&0x003f, time_val&0x001f
        )
        self.mdate = datetime.date(
            1980+(date_val>>9), (date_val>>5)&0x000f, date_val&0x001f
        )
        if t == RootEntry.TYPE_FAT32:
            self.addr = struct.unpack('<I', buf[20:22]+buf[26:28])[0]
        else:
            self.addr = struct.unpack('<H', buf[26:28])[0]
        self.filesize = struct.unpack('<I', buf[28:32])[0]

    def __str__(self):
        return '{} {}|{} {}|{} {} {} {}'.format(
            hex(self.attr), self.cdate, self.ctime, self.mdate, self.mtime, 
            self.addr, self.filesize, self.name
        )
        

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
        self._entries.append(RootEntry(buf, RootEntry.TYPE_FAT12))

    def __str__(self):
        l = [str(i) for i in self._entries]
        return '\n'.join(l)


class RootDirs16(RootDirs):

    def __init__(self, path, begin, max_entries):
        super(RootDirs16, self).__init__(path, begin, max_entries)


class RootDirs32(RootDirs):

    def __init__(self, path, begin, max_entries):
        super(RootDirs32, self).__init__(path, begin, max_entries)
