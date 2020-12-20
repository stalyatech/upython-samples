import machine
import _thread
import sty
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# NMEA message received callback
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnNmeaMsg(params):
    print(params[1].decode('utf-8'))
    led2.toggle()

# ---------------------------------------------------------------
# NMEA message parsed callback
# ---------------------------------------------------------------
def OnDecodedMsg(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-On the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED with application buffer and NMEA parser
zed1 = UART('ZED1', 115200, rxbuf=1024, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsg, decall=OnDecodedMsg))

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
