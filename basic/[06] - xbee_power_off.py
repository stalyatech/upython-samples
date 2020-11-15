from sty import Pin

# ---------------------------------------------------------------
# Power-Off the XBEE-LP subsystem of RTK board
# ---------------------------------------------------------------

# XBEE Low Power Socket
xbee_lp_pwr = Pin('PWR_XBEE_LP', Pin.OUT_OD)
xbee_lp_pwr.low()

# XBEE High Power Socket
xbee_hp_pwr = Pin('PWR_XBEE_HP', Pin.OUT_OD)
xbee_hp_pwr.low()

# Console info
print('XBEE Power-Off')
