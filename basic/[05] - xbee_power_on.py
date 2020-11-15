from sty import Pin

# ---------------------------------------------------------------
# Power-on the XBEE-LP subsystem of RTK board
# ---------------------------------------------------------------

# XBEE Low Power Socket
xbee_lp_pwr = Pin('PWR_XBEE_LP', Pin.OUT_OD)
xbee_lp_pwr.high()

# XBEE High Power Socket
xbee_hp_pwr = Pin('PWR_XBEE_HP', Pin.OUT_OD)
xbee_hp_pwr.high()

# XBEE Low Power Direction (XBEE_LP <-> FTDI)
xbee_lp_dir = Pin('XBEE_LP_DIR', Pin.OUT_OD)
xbee_lp_dir.low()

# XBEE High Power Direction (XBEE_HP <-> FTDI)
xbee_hp_dir = Pin('XBEE_HP_DIR', Pin.OUT_OD)
xbee_hp_dir.low()

# Console info
print('XBEE Power-On')
print('You should see XBee serial ports on your PC ;)')
