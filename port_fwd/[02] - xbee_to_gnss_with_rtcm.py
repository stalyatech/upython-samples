import sty
import machine
import uasyncio
from sty import UART
from sty import Parser

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
# RTCM message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnRtcmMsg(message):
    zed1.send(message)
    zed2.send(message)
    zed3.send(message)
    while zed3.istxbusy():
        pass

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-On the XBEE subsystem
pwr.on(machine.POWER_XBEE)

# UART configuration of XBEE LP without application buffer and RTCM parser
xbee_lp = UART('XBEE_LP', 115200, dma=True, parser=Parser(Parser.RTCM, rxbuf=2048, rxcall=OnRtcmMsg))

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
