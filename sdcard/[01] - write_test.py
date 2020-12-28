import machine
import uasyncio
from sty import UART
from sty import Queue
from sty import Parser

# Initialize the static message queue
msgq = Queue(count=10, size=128)

# ---------------------------------------------------------------
# NMEA message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsg(message):
    try:
        msgq.append(message)
    except IndexError:
        pass

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
zed1 = UART('ZED1', 460800, dma=True, parser=Parser(Parser.NMEA, rxbuf=128, rxcall=OnNmeaMsg))

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Get the queued message
        try:
            msg = msgq.popleft().decode('utf-8')
            fp.write(msg)
            fp.flush()
            print(msg[:-2])
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
