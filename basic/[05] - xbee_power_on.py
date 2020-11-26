import machine

# ---------------------------------------------------------------
# Power-On the XBEE subsystem
# ---------------------------------------------------------------
pwr = machine.Power()
pwr.on(machine.POWER_XBEE)

# Console info
print('XBEE Power-On')
print('You should see XBee serial ports on your PC ;)')
