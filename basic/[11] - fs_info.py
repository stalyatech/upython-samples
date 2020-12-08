import os
import sty

# ---------------------------------------------------------------
# Prints the storage information
# ---------------------------------------------------------------
def get_machine_storage(root):
    result = os.statvfs(root)
    f_bsize = result[0]
    f_frsize = result[1]
    f_blocks = result[2]
    f_bfree = result[3]
    block_size = f_frsize
    total_blocks = f_blocks
    free_blocks = f_bfree
    mega = 1000 * 1000
    total_size = total_blocks * block_size / mega
    free_size = free_blocks * block_size / mega
    print('{} : total_size={} free_size={}'.format(root, total_size, free_size))

# ---------------------------------------------------------------
# Get the FAT information
# ---------------------------------------------------------------
get_machine_storage('/flash')

# ---------------------------------------------------------------
# Get the LFS2 information
# ---------------------------------------------------------------

# Has been the partition mounted ?
try:
    os.stat('/data')
except OSError as error:
    print(error)
    os.mount(sty.Flash(start=1024*1024), '/data')
finally:
    get_machine_storage('/data')
