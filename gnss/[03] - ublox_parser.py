import machine
import _thread
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# UBX message received callback
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnUbloxMsg(params):
    parser = params[0]
    parser.decode(params[1])

# ---------------------------------------------------------------
# UBX message decoded callback
# ---------------------------------------------------------------
def OnUbloxDecoded(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED1 without application buffer and UBX parser
zed1 = UART('ZED1', 115200, dma=True, parser=Parser(Parser.UBX, rxbuf=1024, rxcall=OnUbloxMsg, decall=OnUbloxDecoded))

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
