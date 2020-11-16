from machine import WDT

# Enable the watchdog timer with a timeout of 3s
wdt = WDT(timeout=5000)
wdt.feed()

# Print info
print('Watchdog timer started...')
print('It will cause the system reset!')

# Check it for reset
while True:
    pass
