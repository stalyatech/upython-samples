from collections import deque
import machine
import uasyncio
import sty
from sty import UART
from sty import Parser

# Initializing the message queue
msgq = deque((), 10)

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# NMEA message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsg(message):
    msgq.append(message)
    led2.toggle()

# ---------------------------------------------------------------
# NMEA message decoded callback
# ---------------------------------------------------------------
def OnDecodedMsg(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-On the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED1 without application buffer and NMEA parser
zed1 = UART('ZED1', 115200, dma=True, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsg, decall=OnDecodedMsg))

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Get the NMEA messages
        try:
            print(msgq.popleft().decode('utf-8'))
        except Exception:
            pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
