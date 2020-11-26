import os
import sty
import time
import machine

# 1st FAT partition (1MB)
p1 = sty.Flash(start=0, len=1024*1024)

# 2nd LittleFS partition (15MB)
p2 = sty.Flash(start=1024*1024)

# Make the FAT partition
os.VfsFat.mkfs(p1)
print('FAT partition has been created')

# Make the LittleFS partition
os.VfsLfs2.mkfs(p2)
print('LFS2 partition has been created')

# Wait a little bit
print('All partitions done')
time.sleep(1)

# Reset the machine to inform host OS for new partitions
machine.reset()
