import machine
import uasyncio
from sty import LED
from sty import UART

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = LED(1)
led2 = LED(2)
led3 = LED(3)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-On the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED1
zed1 = UART('ZED1', 460800, dma=False)

# ---------------------------------------------------------------
# Service Port
# ---------------------------------------------------------------

# UART configuration of service port
srv = UART('SRV', 460800, dma=True)

# ---------------------------------------------------------------
# Port Forwarding
# ---------------------------------------------------------------

# Hardware connection of ports
# (zed1 -> serv)
zed1.connect(srv)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Heart-beat
        led3.toggle()

        # Yield the other process
        await uasyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
