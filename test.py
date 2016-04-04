#!/usr/bin/python

import sys
from pyfat import mbr


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     sys.stderr.write('Wrong usage\n')
    #     sys.exit(1)

    sys.stdout.write('** FAT12 **\n')
    with open('2M.vol', 'rb') as f12:
        mbr_sector = f12.read(mbr.MBR_SIZE)
        mbr12 = mbr.MBR12(mbr_sector)
        print(mbr12)

    sys.stdout.write('** FAT16 **\n')
    with open('100M.vol', 'rb') as f16:
        mbr_sector = f16.read(mbr.MBR_SIZE)
        mbr16 = mbr.MBR16(mbr_sector)
        print(mbr16)

    sys.stdout.write('** FAT32 **\n')
    with open('1G.vol', 'rb') as f32:
        mbr_sector = f32.read(mbr.MBR_SIZE)
        mbr32 = mbr.MBR32(mbr_sector)
        print(mbr32)