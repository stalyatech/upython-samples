import _thread
from sty import Pin
from sty import UART

# ---------------------------------------------------------------
# GNSS NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg(uart, nmeaMsg):
    s = nmeaMsg.decode('utf-8')
    print(s)
    f.write(s + '\n')

# ---------------------------------------------------------------
# GNSS NMEA message parsed callback
# ---------------------------------------------------------------
def OnParsedMsg(msgType, msgItems):
    pass

# ---------------------------------------------------------------
# File system usage
# ---------------------------------------------------------------

# Create the test file
f = open('nmea_log.txt', 'w')

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

# ---------------------------------------------------------------
# Main application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        # Call the NMEA framer processor
        zed1_uart.process(UART.ParserNMEA)
        # Flush the file buffer
        f.flush()

# Start the application process
if __name__ == "__main__":
    _thread.start_new_thread(app_proc, ())
