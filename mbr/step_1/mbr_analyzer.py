import sys
import struct


f = open(sys.argv[1], "rb")
bootsect = f.read(512)

if bootsect[510] != 0x55 or bootsect[511] != 0xAA:
    print(f"[Error] Invalid BootSector {sys.argv[1]}")
    sys.exit(-1)

mbr = bootsect[446:510]

for i in range(4):
    entry_raw = mbr[i*16:(i+1)*16]
    boot_flag = int(entry_raw[0])
    part_type = int(entry_raw[4])

    #(start_sector, partition_size) = struct.unpack("@II", entry_raw[8:16]) 
    start_sector = struct.unpack("@I", entry_raw[8:12])[0]
    partition_size = struct.unpack("@I", entry_raw[12:16])[0]

    entry = {
        "boot_flag": boot_flag,
        "part_type": part_type,
        "start_sector": start_sector,
        "partition_size": partition_size,
    }

    print(entry)
