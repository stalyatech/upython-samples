import machine
import uasyncio
from sty import UART
from sty import Queue
from sty import Parser

# Initialize the static message queues
msgq_nmea = Queue(count=10, size=128)
msgq_ublx = Queue(count=10, size=256)

# ---------------------------------------------------------------
# NMEA message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsg(message):
    try:
        msgq_nmea.append(message)
    except IndexError:
        pass

# ---------------------------------------------------------------
# NMEA message decoded callback
# ---------------------------------------------------------------
def OnNmeaDecoded(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# UBX message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnUbloxMsg(message):
    try:
        msgq_ublx.append(message)
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

# Parser configurations
nmea = Parser(Parser.NMEA, rxbuf=128, rxcall=OnNmeaMsg, decall=OnNmeaDecoded)
ublx = Parser(Parser.UBX, rxbuf=256, rxcall=OnUbloxMsg, decall=OnUbloxDecoded)

# UART configuration of ZED1 without application buffer and multiple parsers!
zed1 = UART('ZED1', 460800, dma=True, parser=[nmea, ublx])

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Decode the NMEA messages
        try:
            nmea.decode(msgq_nmea.popleft())
        except IndexError:
            pass

        # Decode the UBX messages
        try:
            ublx.decode(msgq_ublx.popleft())
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
