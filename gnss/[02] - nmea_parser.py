from sty import Pin
from sty import UART
import _thread

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
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_OD)
gnss_pwr.high()

# UART configuration of ZEDs without application buffer
zed1_uart = UART('ZED1', 115200, rxbuf=0, dma=True)

# Parser configuration
zed1_uart.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg, frcallback=OnParsedMsg)

# Main application process
def app_proc():
    while True:
        # Call the NMEA framer processor
        zed1_uart.process(UART.ParserNMEA)

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
