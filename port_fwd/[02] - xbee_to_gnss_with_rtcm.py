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
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_PP)
gnss_pwr.high()

# UART configuration of ZEDs
zed1_uart = UART('ZED1', 115200, rxbuf=0, dma=True)
zed2_uart = UART('ZED2', 115200, rxbuf=0, dma=True)
zed3_uart = UART('ZED3', 115200, rxbuf=0, dma=True)

# ---------------------------------------------------------------
# RTCM message received callback
# ---------------------------------------------------------------
def OnRtcmMsg(uart, rtcmMsg):
    zed1_uart.send(rtcmMsg)
    zed2_uart.send(rtcmMsg)
    zed3_uart.send(rtcmMsg)
    while zed3_uart.istxbusy() == True:
        pass

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
xlp_uart = UART('XBEE_LP', 115200, rxbuf=0, dma=True)

# Parser configuration
xlp_uart.parser(UART.ParserRTCM, rxbuf=1030, rxcallback=OnRtcmMsg)

# Main application process
def app_proc():
    while True:
        # Call the RTCM framer processor
        xlp_uart.process(UART.ParserRTCM)

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
