import sty
import machine
import uasyncio
from sty import UART

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-On the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZEDs
zed1 = UART('ZED1', 115200, dma=True)
zed2 = UART('ZED2', 115200, dma=True)
zed3 = UART('ZED3', 115200, dma=True)

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-On the XBEE subsystem
pwr.on(machine.POWER_XBEE)

# XBEE LP UART configuration
xbee_lp = UART('XBEE_LP', 115200, dma=False)

# Hardware connection of ports
# (xbee_lp -> zed1)
# (xbee_lp -> zed2)
# (xbee_lp -> zed3)
xbee_lp.connect([zed1, zed2, zed3])

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
