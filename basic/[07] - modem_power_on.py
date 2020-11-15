from sty import Pin

# ---------------------------------------------------------------
# Power-On the Modem subsystem of RTK board
# ---------------------------------------------------------------
modem_pwr = Pin('PWR_GSM', Pin.OUT_OD)
modem_pwr.high()

# Console info
print('Modem Power-On')
print('You should see modem serial ports on your PC ;)')
