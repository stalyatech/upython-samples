from sty import Pin

# ---------------------------------------------------------------
# Power-Off the Modem subsystem of RTK board
# ---------------------------------------------------------------
modem_pwr = Pin('PWR_GSM', Pin.OUT_OD)
modem_pwr.low()

# Console info
print('Modem Power-Off')
