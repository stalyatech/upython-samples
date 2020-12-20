import sty
import machine
import _thread
from sty import UART

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# ZED1 message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# params[0] : UART object
# params[1] : Message object
# ---------------------------------------------------------------
def OnDataRecvFromZED1(params):
    pass

# ---------------------------------------------------------------
# ZED2 message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# params[0] : UART object
# params[1] : Message object
# ---------------------------------------------------------------
def OnDataRecvFromZED2(params):
    pass

# ---------------------------------------------------------------
# ZED3 message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# params[0] : UART object
# params[1] : Message object
# ---------------------------------------------------------------
def OnDataRecvFromZED3(params):
    pass

# ---------------------------------------------------------------
# XBEE_LP message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# params[0] : UART object
# params[1] : Message object
# ---------------------------------------------------------------
def OnDataRecvFromXBeeLP(params):
    msg = params[1]
    zed1.send(msg)
    zed2.send(msg)
    zed3.send(msg)
    led1.toggle()

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-On the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZEDs
zed1 = UART('ZED1', 115200)
zed2 = UART('ZED2', 115200)
zed3 = UART('ZED3', 115200)

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-On the XBEE subsystem
pwr.on(machine.POWER_XBEE)

# XBEE LP UART configuration
xbee_lp = UART('XBEE_LP', 115200)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    # Set the GNSS ISR callbacks
    zed1.callback(OnDataRecvFromZED1)
    zed2.callback(OnDataRecvFromZED2)
    zed3.callback(OnDataRecvFromZED3)

    # Set the XBEE_LP ISR callback
    xbee_lp.callback(OnDataRecvFromXBeeLP)

    while True:
        pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
