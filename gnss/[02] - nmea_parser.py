import machine
import _thread
from sty import UART

# ---------------------------------------------------------------
# GNSS NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg(uart, nmeaMsg):
    print(nmeaMsg)
    uart.parse_nmea(nmeaMsg)

# ---------------------------------------------------------------
# GNSS NMEA message parsed callback
# ---------------------------------------------------------------
def OnParsedMsg(msgType, msgItems):
    print(msgType)
    print(msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZEDs without application buffer
zed1 = UART('ZED1', 115200, rxbuf=0, dma=True)

# Parser configuration
zed1.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg, frcallback=OnParsedMsg)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        # Call the NMEA framer processor
        zed1.process(UART.ParserNMEA)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
