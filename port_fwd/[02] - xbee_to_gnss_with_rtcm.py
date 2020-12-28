import machine
import uasyncio
from sty import LED
from sty import UART
from sty import Queue
from sty import Parser

# Initialize the static message queues
msgq = Queue(count=8, size=1024)

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

# UART configuration of ZEDs
zed1 = UART('ZED1', 460800, dma=True)
zed2 = UART('ZED2', 460800, dma=True)
zed3 = UART('ZED3', 460800, dma=True)

# ---------------------------------------------------------------
# RTCM message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnRtcmMsg(message):
    try:
        msgq.append(message)
    except IndexError:
        pass

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-On the XBEE subsystem
pwr.on(machine.POWER_XBEE)

# UART configuration of XBEE LP without application buffer and RTCM parser
xbee_lp = UART('XBEE_LP', 115200, dma=True, parser=Parser(Parser.RTCM, rxbuf=1024, rxcall=OnRtcmMsg))

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Forward the RTCM messages
        try:
            msg = msgq.popleft()
            zed1.send(msg)
            zed2.send(msg)
            zed3.send(msg)
        except IndexError:
            pass

        await uasyncio.sleep_ms(50)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
