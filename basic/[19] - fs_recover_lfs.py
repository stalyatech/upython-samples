import sty
import uos
import utime
import uerrno
import machine

# ---------------------------------------------------------------
# Wipe the LittFS partition to test it
# ---------------------------------------------------------------
def WipeLFS2():
    print('LittFS wipe started')
    # Get the flash partion
    flash = sty.Flash(start=1024*1024)
    # Random number array
    values = uos.urandom(2048)
    # Damage the filesystem
    for block in range(512):
        flash.writeblocks(block, values)
    print('LittFS wiped!')

# ---------------------------------------------------------------
# Try to mount the LFS2 partition
# ---------------------------------------------------------------
def MountLFS2(reset):
    try:
        # Check the status
        uos.stat('/data')
        print('LittleFS is healty;)')
    except OSError as exc:
        if exc.args[0] == uerrno.ENODEV:
            # There is no device!
            # First try to mount it
            try:
                uos.mount(sty.Flash(start=1024*1024), '/data')
                print('LittleFS mounted')
            except OSError as err:
                # Something is wrong!!!
                if err.args[0] == uerrno.ENODEV:
                    # Recreate the LFS2 partion
                    uos.VfsLfs2.mkfs(sty.Flash(start=1024*1024))
                    print('LittleFS created')
                    uos.mount(sty.Flash(start=1024*1024), '/data')
                    print('LittleFS mounted')
                    # if requested, reset the system
                    if reset:
                        utime.sleep(2)
                        machine.reset()


# Damage the filesystem to test it
#WipeLFS2()

# Mount the LittleFS
MountLFS2(True)
