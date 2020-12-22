import machine

# ---------------------------------------------------------------
# Power-On the USB Hub
# ---------------------------------------------------------------
pwr = machine.Power()
pwr.off(machine.POWER_HUB)

# Console info
print('USB Hub has been disabled!')
print('You don''t not see any serial port except MCU!')
print('Ctrl+B helps to get command prompt ;)')
