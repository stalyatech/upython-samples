import sty
import _thread
from sty import UART

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# GNSS NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg(uart, nmeaMsg):
    print(nmeaMsg.decode('utf-8'))
    led2.toggle()

# ---------------------------------------------------------------
# GNSS NMEA message parsed callback
# ---------------------------------------------------------------
def OnParsedMsg(msgType, msgItems):
    pass

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# UART configuration of ZEDs with application buffer
zed1 = UART('ZED1', 115200, rxbuf=1024)

# Parser configuration
zed1.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg, frcallback=OnParsedMsg)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        # ZED Message processor
        zed1.process(UART.ParserNMEA)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
