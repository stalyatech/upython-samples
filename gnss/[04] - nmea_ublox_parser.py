import machine
import _thread
from sty import UART

# ---------------------------------------------------------------
# GNSS NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg(uart, nmeaMsg):
    print(nmeaMsg)
    uart.parse_nmea(nmeaMsg)

# ---------------------------------------------------------------
# GNSS NMEA message parsed callback
# ---------------------------------------------------------------
def OnNmeaParsed(msgType, msgItems):
    print(msgType)
    print(msgItems)

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
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED with application buffer
zed1 = UART('ZED1', 115200, rxbuf=0, dma=False)

# Parser configurations
zed1.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg, frcallback=OnNmeaParsed)
zed1.parser(UART.ParserUBX, rxbuf=256, rxcallback=OnUbloxMsg, frcallback=OnUbloxParsed)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        # Call the UBX framer processor
        zed1.process(UART.ParserUBX)
        # Call the NMEA framer processor
        zed1.process(UART.ParserNMEA)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
