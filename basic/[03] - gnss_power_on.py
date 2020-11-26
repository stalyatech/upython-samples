import machine

# ---------------------------------------------------------------
# Power-On the GNSS subsystem
# ---------------------------------------------------------------
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# Console info
print('GNSS Power-On')
print('You should see GPS serial ports on your PC ;)')
