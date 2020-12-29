import machine
import uasyncio
from sty import UART
from sty import Queue
from sty import Parser

# Initialize the static message queue
msgq = Queue(count=10, size=128)

# ---------------------------------------------------------------
# NMEA message received callback
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsg(message):
    try:
        msgq.append(message)
    except IndexError:
        pass

# ---------------------------------------------------------------
# NMEA message decoded callback
# ---------------------------------------------------------------
def OnDecodedMsg(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-On the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED1 without application buffer and NMEA parser
zed1 = UART('ZED1', 460800, dma=True, parser=Parser(Parser.NMEA, rxbuf=128, rxcall=OnNmeaMsg, decall=OnDecodedMsg))

# UART configuration of service port without application buffer
srv = UART('SRV', 115200, dma=True)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Print the NMEA messages from service port
        try:
            srv.send(msgq.popleft().decode('utf-8'))
            while srv.istxbusy():
                await uasyncio.sleep_ms(1)
        except Exception:
            pass

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
