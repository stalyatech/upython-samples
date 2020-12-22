from collections import deque
import machine
import uasyncio
from sty import UART
from sty import Parser

# Initializing the message queues
msgq_rtcm = deque((), 10)
msgq_ublx = deque((), 10)

# ---------------------------------------------------------------
# RTCM message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnRtcmMsg(message):
    msgq_rtcm.append(message)

# ---------------------------------------------------------------
# UBX message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnUbloxMsg(message):
    msgq_ublx.append(message)

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

# UART configuration of ZED without application buffer and RTCM parser
zed1 = UART('ZED1', 115200, dma=True)

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-on the XBEE subsystem
pwr.on(machine.POWER_XBEE)

# Parser configurations
ublx = Parser(Parser.UBX, rxbuf=256, rxcall=OnUbloxMsg, decall=OnUbloxDecoded)
rtcm = Parser(Parser.RTCM, rxbuf=2048, rxcall=OnRtcmMsg)

# UART configuration of XBEE HP without application buffer and multiple parsers!
xbee_hp = UART('XBEE_HP', 115200, dma=True, parser=[ublx, rtcm])

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Decode the UBX messages
        try:
            ublx.decode(msgq_ublx.popleft())
        except Exception:
            pass

        # Print the RTCM messages
        try:
            print(msgq_rtcm.popleft())
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
