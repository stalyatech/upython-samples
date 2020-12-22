from collections import deque
import machine
import uasyncio
from sty import UART
from sty import Parser

# Initializing the message queue
msgq = deque((), 10)

# ---------------------------------------------------------------
# NMEA message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsg(message):
    msgq.append(message)

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

# Configure the NMEA parser
nmea = Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsg, decall=OnDecodedMsg)

# UART configuration of ZED1 without application buffer and NMEA parser
zed1 = UART('ZED1', 115200, dma=True, parser=nmea)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Decode the NMEA messages
        try:
            nmea.decode(msgq.popleft())
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
