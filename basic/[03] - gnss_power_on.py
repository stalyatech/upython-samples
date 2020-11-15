from sty import Pin

# ---------------------------------------------------------------
# Power-On the GNSS subsystem of RTK board
# ---------------------------------------------------------------
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_OD)
gnss_pwr.high()

# Console info
print('GNSS Power-On')
print('You should see GPS serial ports on your PC ;)')
