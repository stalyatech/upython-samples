import machine
import uasyncio
from sty import LED
from sty import UART
from sty import Queue
from sty import Parser

# Initialize the static message queue
msgq = Queue(count=10, size=128)

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = LED(1)
led2 = LED(2)
led3 = LED(3)

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
    led3.toggle()

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
zed1 = UART('ZED1', 460800, dma=True, parser=Parser(Parser.NMEA, rxbuf=128, rxcall=OnNmeaMsg, decall=OnDecodedMsg))

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Print the NMEA messages
        try:
            msg = msgq.popleft().decode('utf-8')
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
