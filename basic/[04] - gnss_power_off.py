import machine

# ---------------------------------------------------------------
# Power-Off the GNSS subsystem
# ---------------------------------------------------------------
pwr = machine.Power()
pwr.off(machine.POWER_GNSS)

# Console info
print('GNSS Power-Off')
