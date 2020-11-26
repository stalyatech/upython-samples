import machine

# ---------------------------------------------------------------
# Power-Off the Modem subsystem
# ---------------------------------------------------------------
pwr = machine.Power()
pwr.off(machine.POWER_GSM)

# Console info
print('Modem Power-Off')
