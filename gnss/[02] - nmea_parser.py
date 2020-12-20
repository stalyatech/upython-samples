import machine
import _thread
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg(parser, nmeaMsg):
    parser.decode(nmeaMsg)

# ---------------------------------------------------------------
# NMEA message decoded callback
# ---------------------------------------------------------------
def OnDecodedMsg(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED1 without application buffer and NMEA parser
zed1 = UART('ZED1', 115200, rxbuf=0, dma=True, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsg, decall=OnDecodedMsg))

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
