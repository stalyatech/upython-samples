import sty
import machine
import _thread
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-On the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZEDs
zed1 = UART('ZED1', 115200, dma=True)
zed2 = UART('ZED2', 115200, dma=True)
zed3 = UART('ZED3', 115200, dma=True)

# ---------------------------------------------------------------
# RTCM message received callback
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnRtcmMsg(params):
    rtcmMsg = params[1]
    zed1.send(rtcmMsg)
    zed2.send(rtcmMsg)
    zed3.send(rtcmMsg)
    while zed3.istxbusy():
        pass

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-On the XBEE subsystem
pwr.on(machine.POWER_XBEE)

# UART configuration of XBEE LP without application buffer and RTCM parser
xbee_lp = UART('XBEE_LP', 115200, dma=True, parser=Parser(Parser.RTCM, rxbuf=2048, rxcall=OnRtcmMsg))

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
