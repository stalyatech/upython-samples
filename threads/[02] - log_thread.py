from sty import Pin
from sty import UART
import uasyncio as asyncio
import sty

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# File system usage
# ---------------------------------------------------------------
fext1 = 0
fext2 = 0

# Create the test files
fp1 = open('nmea_log1.000', 'w')
fp2 = open('nmea_log2.000', 'w')

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_PP)
gnss_pwr.high()

# UART configuration of ZEDs without application buffer
zed1_uart = UART('ZED1', 115200, rxbuf=0, dma=True)
zed2_uart = UART('ZED2', 115200, rxbuf=0, dma=True)

# ---------------------------------------------------------------
# ZED1 GNSS NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg1(uart, nmeaMsg):
    s = 'ZED1: ' + nmeaMsg.decode('utf-8')
    print(s)
    fp1.write(s + '\n')

# ---------------------------------------------------------------
# ZED1 GNSS NMEA message parsed callback
# ---------------------------------------------------------------
def OnParsedMsg1(msgType, msgItems):
    pass

# ---------------------------------------------------------------
# ZED2 GNSS NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg2(uart, nmeaMsg):
    s = 'ZED2: ' + nmeaMsg.decode('utf-8')
    print(s)
    fp2.write(s + '\n')

# ---------------------------------------------------------------
# ZED2 GNSS NMEA message parsed callback
# ---------------------------------------------------------------
def OnParsedMsg2(msgType, msgItems):
    pass

# Parser configuration
zed1_uart.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg1, frcallback=OnParsedMsg1)
zed2_uart.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg2, frcallback=OnParsedMsg2)

# ---------------------------------------------------------------
# Thread #1 process
# ---------------------------------------------------------------
async def thread1_proc():
    global fext1, fext2
    global fp1, fp2

    while True:
        # ZED1 NMEA framer processor
        zed1_uart.process(UART.ParserNMEA)
        fp1.flush()

        # ZED2 NMEA framer processor
        zed2_uart.process(UART.ParserNMEA)
        fp2.flush()

        # Check the size of files
        if fp1.tell() > 1000000:
            print('ZED1 file bigger than 1MB')
            fp1.close()
            fext1 += 1
            s = 'nmea_log1.{:03d}'.format(fext1)
            print('ZED1 file name: ' + s)
            fp1 = open(s, 'w')
        if fp2.tell() > 1000000:
            print('ZED2 file bigger than 1MB')
            fp2.close()
            fext2 += 1
            s = 'nmea_log2.{:03d}'.format(fext2)
            print('ZED2 file name: ' + s)
            fp2 = open(s, 'w')

        # Yield to the other tasks
        await asyncio.sleep_ms(10)

# ---------------------------------------------------------------
# Thread #2 process
# ---------------------------------------------------------------
async def thread2_proc():
    while True:
        led2.toggle()
        await asyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Thread #3 process
# ---------------------------------------------------------------
async def thread3_proc():
    while True:
        led3.toggle()
        await asyncio.sleep_ms(500)

# ---------------------------------------------------------------
# Main process
# ---------------------------------------------------------------
async def main():
    asyncio.create_task(thread1_proc())
    asyncio.create_task(thread2_proc())
    asyncio.create_task(thread3_proc())
    loop = asyncio.get_event_loop()
    loop.run_forever()

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()
