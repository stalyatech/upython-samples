import machine

# ---------------------------------------------------------------
# Power-On the Modem subsystem
# ---------------------------------------------------------------
pwr = machine.Power()
pwr.on(machine.POWER_GSM)

# Console info
print('Modem Power-On')
print('You should see modem serial ports on your PC ;)')
