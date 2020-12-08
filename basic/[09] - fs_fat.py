import os
import time
import machine
import sty

# FAT partition for all flash
p = sty.Flash(start=0)

# Make the FAT partition
os.VfsFat.mkfs(p)

# Wait a little bit
print('FAT partition has been created')
time.sleep(1)

# Reset the machine to inform host OS for new partitions
machine.reset()
