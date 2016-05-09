#!/usr/bin/env python

import struct
from . import error

class FAT(object):

    def __init__(self, path, begin, media_desc, sector_bytes, fat_sectors):
        self._fd = open(path, 'rw+')
        self._fd.seek(begin * sector_bytes)
        if media_desc != ord(self._fd.read(1)[0]):
            self._fd.close()	# FIXME: Is it need close()?
            raise error.FormatError("Incorrect FAT signature!")
        self._begin = begin
        self._sector_bytes = sector_bytes
        self._fat_sectors = fat_sectors

    def __del__(self):
        if not self._fd:
            self._fd.close()

class FAT12(FAT):

    ENTRY_SIZE = 1.5

    class ClusterFlag(object):
        BAD = (0x0ff7,)
        RESERVED = (0x0ff0+x for x in range(7))
        LAST = (0x0ff8+x for x in range(8))

    def __init__(self, path, begin, media_desc, sector_bytes, fat_sectors):
        super(FAT12, self).__init__(path, begin, media_desc, sector_bytes, fat_sectors)

    def file_clusters(self, start_cluster):
        if (start_cluster < 0x0002 or start_cluster in FAT12.ClusterFlag.BAD or 
            start_cluster in FAT12.ClusterFlag.RESERVED):
            return []
        end_cluster = start_cluster
        clusters = [end_cluster, ]
        while end_cluster not in FAT12.ClusterFlag.LAST:
            end_cluster = self._fetch_entry(end_cluster)
            clusters.append(end_cluster)
        return clusters

    def _fetch_entry(self, cluster_number):
        self._fd.seek(self._begin*self._sector_bytes + cluster_number*FAT12.ENTRY_SIZE)
        entry, = struct.unpack('<L', self._fd.read(4))
        entry = entry & 0xfff0
        return entry

class FAT16(FAT):

    ENTRY_SIZE = 16

    def __init__(self, path, begin, sector_bytes, fat_sectors):
        super(FAT16, self).__init__(path, begin, sector_bytes, fat_sectors)

class FAT32(FAT):

    ENTRY_SIZE = 32

    def __init__(self, path, begin, sector_bytes, fat_sectors):
        super(FAT32, self).__init__(path, begin, sector_bytes, fat_sectors)
