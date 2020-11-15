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

# ZED1 message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
def OnDataRecvFromZED1(uart, msg):
    pass

# ZED2 message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
def OnDataRecvFromZED2(uart, msg):
    pass

# ZED3 message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
def OnDataRecvFromZED3(uart, msg):
    pass

# XBEE_LP message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
def OnDataRecvFromXBeeLP(uart, msg):
    zed1_uart.send(msg)
    zed2_uart.send(msg)
    zed3_uart.send(msg)
    led1.toggle()

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_PP)
gnss_pwr.high()

# UART configuration of ZEDs
zed1_uart = UART('ZED1', 115200, rxbuf=0)
zed2_uart = UART('ZED2', 115200, rxbuf=0)
zed3_uart = UART('ZED3', 115200, rxbuf=0)

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
xlp_uart = UART('XBEE_LP', 115200, rxbuf=0)

# Main application process
def app_proc():
    # Set the GNSS ISR callbacks
    zed1_uart.callback(OnDataRecvFromZED1)
    zed2_uart.callback(OnDataRecvFromZED2)
    zed3_uart.callback(OnDataRecvFromZED3)

    # Set the XBEE_LP ISR callback
    xlp_uart.callback(OnDataRecvFromXBeeLP)

    while True:
        pass

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
