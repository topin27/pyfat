#!/usr/bin/env python

import unittest
from pyfat import mbr


class MBR12Test(unittest.TestCase):

    def setUp(self):
        self.mbr12_fd = open('./tests/2M.vol', 'r')
        self.mbr16_fd = open('./tests/20M.vol', 'r')
        self.mbr32_fd = open('./tests/1G.vol', 'r')

    def testInit(self):
        mbr12 = mbr.MBR12(self.mbr12_fd.read(mbr.MBR_SIZE))
        print mbr12
        self.assertEquals(mbr12.bpb['fs_type'], 'FAT12')
        self.assertEquals(mbr12.bpb['sector_bytes'], 512)

        mbr16 = mbr.MBR16(self.mbr16_fd.read(mbr.MBR_SIZE))
        print mbr16
        self.assertEqual(mbr16.bpb['fs_type'], 'FAT16')
        self.assertEqual(mbr16.bpb['sector_bytes'], 512)

        mbr32 = mbr.MBR32(self.mbr32_fd.read(mbr.MBR_SIZE))
        print mbr32

        fsinfo32 = mbr.FSInfo(self.mbr32_fd.read(mbr.FSINFO_SIZE))
        print fsinfo32

    def tearDown(self):
        self.mbr12_fd.close()
        self.mbr16_fd.close()
        self.mbr32_fd.close()


if __name__ == '__main__':
    unittest.main()
