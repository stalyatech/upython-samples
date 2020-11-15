from sty import Pin

# ---------------------------------------------------------------
# Power-Off the GNSS subsystem of RTK board
# ---------------------------------------------------------------
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_OD)
gnss_pwr.low()

# Console info
print('GNSS Power-Off')
