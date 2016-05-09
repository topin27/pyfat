#!/usr/bin/env python

import struct
from . import error

MBR_SIZE = 512

class MBR(object):

    def __init__(self, sector):
        assert len(sector) == MBR_SIZE
        if ord(sector[510]) != 0x55 or ord(sector[511]) != 0xAA:
            raise error.FormatError("Incorrect FAT MBR signature!")
        data = struct.unpack('<3x8sHBHBHHBHHHH',  sector[:30])
        self._info = {}
        self._info['oem'] = data[0]
        self._info['sector_bytes'] = data[1]
        self._info['cluster_sectors'] = data[2]
        self._info['reserved_sectors'] = data[3]    # 1 for FAT12 and FAT16, 32 for FAT32
        self._info['fat_number'] = data[4]
        self._info['rentry_number'] = data[5]
        self._info['total_sectors'] = data[6]
        self._info['media_desc'] = data[7]
        self._info['fat_sectors'] = data[8]
        self._info['track_sectors'] = data[9]
        self._info['heads_number'] = data[10]
        self._info['hidden_sectors'] = data[11]

    @property
    def info(self):
        return self._info

    def __str__(self):
        s = 'OEM name: {}\n'.format(self._info['oem'])
        s += 'Bytes per Sector: {}\n'.format(self._info['sector_bytes'])
        s += 'Sectors per Cluster: {}\n'.format(self._info['cluster_sectors'])
        s += 'Number of Reserved Sectors: {}\n'.format(self._info['reserved_sectors'])
        s += 'Number of FAT copies: {}\n'.format(self._info['fat_number'])
        s += 'Number of root directory entries: {}\n'.format(self._info['rentry_number'])
        s += 'Total number of sectors: {}\n'.format(self._info['total_sectors'])
        s += 'Media descriptor: {}\n'.format(hex(self._info['media_desc']))
        s += 'Sectors per FAT: {}\n'.format(self._info['fat_sectors'])
        s += 'Sectors per track: {}\n'.format(self._info['track_sectors'])
        s += 'Number of heads: {}\n'.format(self._info['heads_number'])
        s += 'Hidden sectors: {}\n'.format(self._info['hidden_sectors'])
        return s

class MBR12(MBR):

    def __init__(self, sector):
        super(MBR12, self).__init__(sector)
        extend_sig = False
        if ord(sector[38]) == 0x29:
            extend_sig = True
        data = struct.unpack('<39xL11s8s', sector[:62])
        self._info['partition_serial'] = data[0] if extend_sig else 0
        self._info['label'] = data[1] if extend_sig else 0
        self._info['type'] = data[2] if extend_sig else 0

    def __str__(self):
        s = super(MBR12, self).__str__()
        s += 'Serial number of partition: {}\n'.format(hex(self._info['partition_serial']))
        s += 'Volume label: {}\n'.format(self._info['label'])
        s += 'Filesystem type: {}\n'.format(self._info['type'])
        return s

class MBR16(MBR):

    def __init__(self, sector):
        super(MBR16, self).__init__(sector)
        extend_sig = False
        if ord(sector[38]) == 0x28 or ord(sector[38]) == 0x29:
            extend_sig = True
        data = struct.unpack('<28xLL3xL11s8s', sector[:62])
        self._info['hidden_sectors'] = data[0]
        self._info['total_sectors'] = data[1]
        self._info['partition_serial'] = data[2] if extend_sig else 0
        self._info['label'] = data[3] if extend_sig else 0
        self._info['type'] = data[4] if extend_sig else 0

    def __str__(self):
        s = super(MBR16, self).__str__()
        s += 'Serial number of partition: {}\n'.format(hex(self._info['partition_serial']))
        s += 'Volume label: {}\n'.format(self._info['label'])
        s += 'Filesystem type: {}\n'.format(self._info['type'])
        return s


class MBR32(MBR):

    def __init__(self, sector):
        super(MBR32, self).__init__(sector)
        extend_sig = False
        if ord(sector[66]) == 0x29:
            extend_sig = True
        data = struct.unpack('<28xLLL2x2xL2x2x12x3xL11s8s', sector[:90])
        self._info['hidden_sectors'] = data[0]
        self._info['total_sectors'] = data[1]
        self._info['fat_sectors'] = data[2]
        self._info['mirror_flags'] = sector[40:42]
        self._info['1st_cluster'] = data[3]     # of root directory
        self._info['partition_serial'] = data[4] if extend_sig else 0
        self._info['label'] = data[5] if extend_sig else 0
        self._info['type'] = data[6] if extend_sig else 0

    def __str__(self):
        s = super(MBR32, self).__str__()
        s += 'First cluster of root directory: {}\n'.format(self._info['1st_cluster'])
        s += 'Serial number of partition: {}\n'.format(hex(self._info['partition_serial']))
        s += 'Volume label: {}\n'.format(self._info['label'])
        s += 'Filesystem type: {}\n'.format(self._info['type'])
        return s
