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
# File system usage
# ---------------------------------------------------------------

# Create the test file
fp = open('nmea_log.txt', 'w')

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED without application buffer and NMEA parser
zed1 = UART('ZED1', 115200, dma=True, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsg))

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Get the queued message
        try:
            msg = msgq.popleft().decode('utf-8')
            fp.write(msg + '\n')
            print(msg)
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
