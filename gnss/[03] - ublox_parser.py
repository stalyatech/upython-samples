from sty import Pin
from sty import UART
import _thread

# ---------------------------------------------------------------
# GNSS UBX message received callback
# ---------------------------------------------------------------
def OnUbloxMsg(uart, ubxMsg):
    uart.parse_ubx(ubxMsg)

# ---------------------------------------------------------------
# GNSS UBX message parsed callback
# ---------------------------------------------------------------
def OnUbloxParsed(msgType, msgItems):
    print(msgType)
    print(msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_OD)
gnss_pwr.high()

# UART configuration of ZED with application buffer
zed1_uart = UART('ZED1', 115200, rxbuf=0, dma=False)

# Parser configurations
zed1_uart.parser(UART.ParserUBX, rxbuf=2048, rxcallback=OnUbloxMsg, frcallback=OnUbloxParsed)

# Main application process
def app_proc():
    while True:
        # Call the UBX framer processor
        zed1_uart.process(UART.ParserUBX)

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
