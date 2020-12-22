import machine

# ---------------------------------------------------------------
# Power-On the USB Hub
# ---------------------------------------------------------------
pwr = machine.Power()
pwr.on(machine.POWER_HUB)

# Console info
print('USB Hub has been enabled!')
print('You can see all serial ports now!')
print('Ctrl+B helps to get command prompt ;)')
