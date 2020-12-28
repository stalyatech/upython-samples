import machine
import uasyncio
from sty import UART
from sty import Queue
from sty import Parser

# Initialize the static message queue
msgq = Queue(count=10, size=256)

# ---------------------------------------------------------------
# UBX message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnUbloxMsg(message):
    try:
        msgq.append(message)
    except IndexError:
        pass

# ---------------------------------------------------------------
# UBX message decoded callback
# ---------------------------------------------------------------
def OnUbloxDecoded(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# Configure the UBX parser
ubx = Parser(Parser.UBX, rxbuf=256, rxcall=OnUbloxMsg, decall=OnUbloxDecoded)

# UART configuration of ZED1 without application buffer and UBX parser
zed1 = UART('ZED1', 460800, dma=True, parser=ubx)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Decode the UBX messages
        try:
            ubx.decode(msgq.popleft())
        except IndexError:
            pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
