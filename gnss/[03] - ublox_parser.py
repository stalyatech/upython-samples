from collections import deque
import machine
import uasyncio
from sty import UART
from sty import Parser

# Initializing the message queue
msgq = deque((), 10)

# ---------------------------------------------------------------
# UBX message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnUbloxMsg(message):
    msgq.append(message)

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
ubx = Parser(Parser.UBX, rxbuf=1024, rxcall=OnUbloxMsg, decall=OnUbloxDecoded)

# UART configuration of ZED1 without application buffer and UBX parser
zed1 = UART('ZED1', 115200, dma=True, parser=ubx)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Decode the UBX messages
        try:
            ubx.decode(msgq.popleft())
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
