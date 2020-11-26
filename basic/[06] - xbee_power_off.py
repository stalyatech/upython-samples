import machine

# ---------------------------------------------------------------
# Power-Off the XBEE subsystem
# ---------------------------------------------------------------
pwr = machine.Power()
pwr.off(machine.POWER_XBEE)

# Console info
print('XBEE Power-Off')
