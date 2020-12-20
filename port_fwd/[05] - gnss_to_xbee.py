import sty
import machine
import _thread
from sty import UART

# ---------------------------------------------------------------
# ZED message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# params[0] : UART object
# params[1] : Message object
# ---------------------------------------------------------------
def OnDataRecvFromZED(params):
    msg = params[1]
    # Use non-blocking call
    xbee_lp.send(msg)
    xbee_hp.send(msg)
    led1.toggle()

# ---------------------------------------------------------------
# XBEE LP message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# params[0] : UART object
# params[1] : Message object
# ---------------------------------------------------------------
def OnDataRecvFromXBeeLP(params):
    pass

# ---------------------------------------------------------------
# XBEE HP message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# params[0] : UART object
# params[1] : Message object
# ---------------------------------------------------------------
def OnDataRecvFromXBeeHP(params):
    pass

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# UART configuration of ZED
zed1 = UART('ZED1', 115200)

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-On the XBEE subsystem
pwr = machine.Power()
pwr.on(machine.POWER_XBEE)

# XBEE LP UART configuration
xbee_lp = UART('XBEE_LP', 115200)

# XBEE HP UART configuration
xbee_hp = UART('XBEE_HP', 115200)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    # Set the GNSS ISR callbacks
    zed1.callback(OnDataRecvFromZED)

    # Set the XBEE LP ISR callbacks
    xbee_lp.callback(OnDataRecvFromXBeeLP)

    # Set the XBEE HP ISR callback
    xbee_hp.callback(OnDataRecvFromXBeeHP)

    while True:
        pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
