import sys
import struct

from disk import Disk

class FATable:
    def __init__(self, tables, fstype):
        self.tables = tables
        self.fstype = fstype
        self.fatformat = "<l"
        self.fatsize = 4
        if fstype != "FAT32":
            self.fatformat = "<h"
            self.fatsize = 2

    def get(self, cluster):
        arr = [cluster]
        num = cluster
        next_cluster = self.get_info(num)
        while next_cluster != 268435455:
            arr.append(next_cluster)
            next_cluster = self.get_info(next_cluster)

        return arr

    def get_info(self, cluster):
        pos = cluster * self.fatsize
        return struct.unpack(self.fatformat, self.tables[pos : pos+self.fatsize])[0]


class FAT:
    def __init__(self, sector):
        self.fstype = "FAT16"
        self.bytes_per_sector = struct.unpack("<h", sector[11:13])[0]
        self.sectors_per_cluster = struct.unpack("<B", sector[13])[0]
        self.reserved_sector_count = struct.unpack("<h", sector[14:16])[0]
        self.number_of_fats = struct.unpack("<B", sector[16])[0]
        self.root_entry_number = struct.unpack("<h", sector[17:19])[0]
        self.fatsize = 0
        self.backup_boot_sector = 0
        if self.root_entry_number == 0:
            self.fstype = "FAT32"

        if self.fstype == "FAT32":
            self.total_sectors = struct.unpack("<L", sector[32:36])[0]
            self.fatsize = struct.unpack("<L", sector[36:40])[0]
            self.backup_boot_sector = struct.unpack("<h", sector[50:52])[0]
        else:
            self.total_sectors = struct.unpack("<h", sector[19:21])[0]
            self.fatsize = struct.unpack("<h", sector[22:24])[0]

        self.root_dir_sectors = ((self.root_entry_number * 32) + (self.bytes_per_sector - 1)) / self.bytes_per_sector
        self.first_data_sector = self.reserved_sector_count + self.fatsize * self.number_of_fats + self.root_dir_sectors

    def c2s(self, cluster):
        return ((cluster-2) * self.sectors_per_cluster) + self.first_data_sector


def usage():
    print "%s filename sector"%(sys.argv[0])
    sys.exit(0)


def show_part_info(sector):
    return FAT(sector)


def get_fat_table(fat, disk):
    s = fat.reserved_sector_count
    print s
    tables = disk.read(s, fat.fatsize)
    return FATable(tables, fat.fstype)


if __name__ == '__main__':
    filename = sys.argv[1]
    sector = int(sys.argv[2])
    disk = Disk(512, filename)

    raw = disk.read(sector, 512)
    fat = show_part_info(raw)
    print fat.fstype, fat.first_data_sector, fat.reserved_sector_count, fat.fatsize, fat.root_dir_sectors
    fat_table = get_fat_table(fat, disk)
    print fat.c2s(2)
