from sty import Pin
from sty import UART
import sty
import _thread

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

# Power-on the GNSS subsystem
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_PP)
gnss_pwr.high()

# UART configuration of ZEDs with application buffer
zed1_uart = UART('ZED1', 115200, rxbuf=1024)

# Parser configuration
zed1_uart.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg, frcallback=OnParsedMsg)

# Main application process
def app_proc():
    while True:
        # ZED Message processor
        zed1_uart.process(UART.ParserNMEA)

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
