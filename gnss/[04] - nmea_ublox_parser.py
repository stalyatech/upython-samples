import machine
import _thread
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# NMEA message received callback
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnNmeaMsg(params):
    parser = params[0]
    parser.decode(params[1])

# ---------------------------------------------------------------
# NMEA message decoded callback
# ---------------------------------------------------------------
def OnNmeaDecoded(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# UBX message received callback
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnUbloxMsg(params):
    parser = params[0]
    parser.decode(params[1])

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
nmea = Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsg, decall=OnNmeaDecoded)
ublx = Parser(Parser.UBX, rxbuf=256, rxcall=OnUbloxMsg, decall=OnUbloxDecoded)

# UART configuration of ZED1 without application buffer and multiple parsers!
zed1 = UART('ZED1', 115200, dma=True, parser=[nmea, ublx])

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
