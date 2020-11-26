from sty import Pin
from sty import UART
import _thread

# ---------------------------------------------------------------
# RTCM message received callback
# ---------------------------------------------------------------
def OnRtcmMsg(uart, rtcmMsg):
    zed1.send(rtcmMsg)

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
zed1 = UART('ZED1', 115200, rxbuf=0, dma=True)

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-on the XBEE LP subsystem
xlp_pwr = Pin('PWR_XBEE_LP', Pin.OUT_PP)
xlp_pwr.high()

# Re-direct the XBEE LP subsystem to the MCU
xlp_dir = Pin('XBEE_LP_DIR', Pin.OUT_PP)
xlp_dir.high()

# XBEE LP UART configuration
xhp_uart = UART('XBEE_HP', 115200, rxbuf=0, dma=True)

# Parser configuration
xhp_uart.parser(UART.ParserUBX, rxbuf=2048, rxcallback=OnUbloxMsg, frcallback=OnUbloxParsed)
xhp_uart.parser(UART.ParserRTCM, rxbuf=2048, rxcallback=OnRtcmMsg)

# Main application process
def app_proc():
    while True:
        # Call the RTCM framer function
        xhp_uart.process(UART.ParserRTCM)
        # Call the UBX framer function
        xhp_uart.process(UART.ParserUBX)

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
