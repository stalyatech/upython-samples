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

# UART configuration of ZED
zed1_uart = UART('ZED1', 115200, rxbuf=0)

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-on the XBEE LP subsystem
xlp_pwr = Pin('PWR_XBEE_LP', Pin.OUT_PP)
xlp_pwr.high()

# Power-on the XBEE HP subsystem
xhp_pwr = Pin('PWR_XBEE_HP', Pin.OUT_PP)
xhp_pwr.high()

# XBEE LP UART configuration
xlp_uart = UART('XBEE_LP', 115200, rxbuf=0)

# XBEE HP UART configuration
xhp_uart = UART('XBEE_HP', 115200, rxbuf=0)

# Main application process
def app_proc():

    # ZED message received callback
    # It is called from ISR!!!
    # Don't waste the CPU processing time.
    def OnDataRecvFromZED(uart, msg):
        # Use non-blocking call
        xlp_uart.send(msg)
        xhp_uart.send(msg)
        led1.toggle()

    # XBEE LP message received callback
    # It is called from ISR!!!
    # Don't waste the CPU processing time.
    def OnDataRecvFromXBeeLP(uart, msg):
        pass

    # XBEE HP message received callback
    # It is called from ISR!!!
    # Don't waste the CPU processing time.
    def OnDataRecvFromXBeeHP(uart, msg):
        pass

    # Set the GNSS ISR callbacks
    zed1_uart.callback(OnDataRecvFromZED)

    # Set the XBEE LP ISR callbacks
    xlp_uart.callback(OnDataRecvFromXBeeLP)

    # Set the XBEE HP ISR callback
    xhp_uart.callback(OnDataRecvFromXBeeHP)

    while True:
        pass

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
