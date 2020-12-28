import machine
import uasyncio
from sty import LED
from sty import UART

# ---------------------------------------------------------------
# ZED message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnDataRecvFromZED(message):
    # Use non-blocking call
    xbee_lp.send(message)
    xbee_hp.send(message)
    led1.toggle()

# ---------------------------------------------------------------
# XBEE LP message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnDataRecvFromXBeeLP(message):
    pass

# ---------------------------------------------------------------
# XBEE HP message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnDataRecvFromXBeeHP(message):
    pass

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = LED(1)
led2 = LED(2)
led3 = LED(3)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# UART configuration of ZED
zed1 = UART('ZED1', 460800, dma=True)

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
async def app_proc():
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
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
