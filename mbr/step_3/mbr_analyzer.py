from drive import Drive
import sys
import struct


class PartitionEntry:
    def __init__(self):
        self.boot_flag = 0
        self.partition_type = 0
        self.start_sector = 0
        self.size = 0

    def parse_from_buffer(self, entry_raw):
        self.boot_flag = int(entry_raw[0])
        self.partition_type = int(entry_raw[4])

        (self.start_sector, self.size) = struct.unpack("@II", entry_raw[8:16]) 


class MBRAnalyzer:
    def __init__(self, drive):
        self.drive = drive

    def parse(self):
        partitions = []
        bootsect = vdrive.read(0, 1)
        if bootsect[510] != 0x55 or bootsect[511] != 0xAA:
            raise Exception(f"[Error] Invalid BootSector {sys.argv[1]}")

        mbr = bootsect[446:510]
        for i in range(4):
            entry = PartitionEntry()
            entry.parse_from_buffer(mbr[i*16:(i+1)*16])
            partitions.append(entry)

        return partitions

vdrive = Drive(sys.argv[1], 512, 128*1024*1024)
mbr = MBRAnalyzer(vdrive)

for part in mbr.parse():
    print(part.boot_flag, part.partition_type, part.start_sector, part.size)
