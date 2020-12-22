import sty
import machine
import uasyncio
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
# ---------------------------------------------------------------
def OnDataRecvFromZED1(message):
    pass

# ---------------------------------------------------------------
# ZED2 message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnDataRecvFromZED2(message):
    pass

# ---------------------------------------------------------------
# ZED3 message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnDataRecvFromZED3(message):
    pass

# ---------------------------------------------------------------
# XBEE_LP message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# params[0] : UART object
# params[1] : Message object
# ---------------------------------------------------------------
def OnDataRecvFromXBeeLP(message):
    zed1.send(message)
    zed2.send(message)
    zed3.send(message)
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
async def app_proc():
    # Set the GNSS ISR callbacks
    zed1.callback(OnDataRecvFromZED1)
    zed2.callback(OnDataRecvFromZED2)
    zed3.callback(OnDataRecvFromZED3)

    # Set the XBEE_LP ISR callback
    xbee_lp.callback(OnDataRecvFromXBeeLP)

    # Wait infinetely
    while True:
        pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
