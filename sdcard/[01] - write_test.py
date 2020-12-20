import machine
import _thread
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# NMEA message received callback
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnNmeaMsg(params):
    s = params[1].decode('utf-8')
    f.write(s + '\n')
    print(s)

# ---------------------------------------------------------------
# File system usage
# ---------------------------------------------------------------

# Create the test file
f = open('nmea_log.txt', 'w')

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED without application buffer and NMEA parser
zed1 = UART('ZED1', 115200, dma=True, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsg))

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
