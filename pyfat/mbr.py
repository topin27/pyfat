#!/usr/bin/env python

import struct
from . import error


MBR_SIZE = 512


class MBR(object):

    def __init__(self, sector):
        assert len(sector) == MBR_SIZE

        if ord(sector[510]) != 0x55 or ord(sector[511]) != 0xAA:
            raise error.FormatError("Incorrect FAT MBR signature!")

        self.bpb = {}

    def __str__(self):
        s = ''
        for k, v in self.bpb.items():
            s += '{}: {}\n'.format(k, v)
        return s


def _init_fat12or16_mbr(sector):
    data = struct.unpack('<3x8sHBHBHHBHHHLL3xL11s8s', sector[:62])
    return {
        'oem': data[0].strip(),
        'sector_bytes': data[1],
        'cluster_sectors': data[2],
        'reserved': data[3],
        'fat_count': data[4],
        'rentries': data[5],
        'media_type': data[7],
        'fat_sectors': data[8],
        'track_sectors': data[9],
        'head_count': data[10],
        'hidden_sectors': data[11],
        'serial': data[13],
        'label': data[14],
        'fs_type': data[15].strip(),
    }


class MBR12(MBR):

    def __init__(self, sector):
        super(MBR12, self).__init__(sector)
        self.bpb = _init_fat12or16_mbr(sector)


class MBR16(MBR):

    def __init__(self, sector):
        super(MBR16, self).__init__(sector)
        self.bpb = _init_fat12or16_mbr(sector)


class MBR32(MBR):

    def __init__(self, sector):
        super(MBR32, self).__init__(sector)
        data = struct.unpack('<3x8sHBHB4xB2xHHLLLH2xL19xL11s8s', sector[:90])
        self.bpb = {
            'oem': data[0].strip(),
            'sector_bytes': data[1],
            'cluster_sectors': data[2] if data[2] != 0 else data[9],
            'reserved': data[3],
            'fat_count': data[4],
            'media_type': data[5],
            'track_sectors': data[6],
            'head_count': data[7],
            'hidden_sectors': data[8],
            'fat_sectors': data[10],
            # 'other': data[11],
            'rd_1stcluster': data[12],   # Cluster number of the first cluster of the rd
            'serial': data[13],
            'label': data[14],
            'fs_type': data[15].strip(),
        }


FSINFO_SIZE = 512


class FSInfo(object):

    def __init__(self, sector):
        assert(len(sector) == FSINFO_SIZE)

        def verify_signature(s):
            first_one = [ord(x) for x in s[0:4]]
            if first_one != [0x52, 0x52, 0x61, 0x41]:
                return False

            second_one = [ord(x) for x in s[484:488]]
            if second_one != [0x72, 0x72, 0x41, 0x61]:
                return False

            third_one = [ord(x) for x in s[508:512]]
            if third_one != [0x00, 0x00, 0x55, 0xaa]:
                return False

            return True

        if not verify_signature(sector):
            raise error.FormatError('Incorrect FSInfo signature')

        data = struct.unpack('<488xLL16x', sector)
        self.last_free = data[0]       # Last free cluster on the volume
        self.free_cluster = data[1]    # Indicates where FAT should look for free clusters

    def __str__(self):
        s = 'last_free: {}\n'.format(self.last_free)
        s += 'free_cluster: {}\n'.format(self.free_cluster)
        return s
