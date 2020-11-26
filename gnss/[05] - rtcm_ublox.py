import machine
import _thread
from sty import UART

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
    print(msgType, msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED with application buffer
zed1 = UART('ZED1', 115200, rxbuf=0, dma=True)

# ---------------------------------------------------------------
# XBEE Expansions
# ---------------------------------------------------------------

# Power-on the XBEE subsystem
pwr.on(machine.POWER_XBEE)

# XBEE HP UART configuration
xbee_hp = UART('XBEE_HP', 115200, rxbuf=0, dma=True)

# Parser configuration
xbee_hp.parser(UART.ParserUBX, rxbuf=2048, rxcallback=OnUbloxMsg, frcallback=OnUbloxParsed)
xbee_hp.parser(UART.ParserRTCM, rxbuf=2048, rxcallback=OnRtcmMsg)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        # Call the RTCM framer processor
        xbee_hp.process(UART.ParserRTCM)
        # Call the UBX framer processor
        xbee_hp.process(UART.ParserUBX)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
