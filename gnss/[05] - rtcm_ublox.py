import machine
import _thread
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# RTCM message received callback
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnRtcmMsg(params):
    print(params[1])

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
def app_proc():
    while True:
        pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
