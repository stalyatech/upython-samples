from sty import Pin
from sty import UART
import uasyncio as asyncio
import sty
import utime
import machine

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# File system usage
# ---------------------------------------------------------------

# Create the test files
fp1 = open('nmea_log1.txt', 'a+')
fp2 = open('nmea_log2.txt', 'a+')

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_OD)
gnss_pwr.high()

# UART configuration of ZEDs without application buffer
zed1_uart = UART('ZED1', 115200, rxbuf=0, dma=False)
zed2_uart = UART('ZED2', 115200, rxbuf=0, dma=False)

# ---------------------------------------------------------------
# ZED1 GNSS NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg1(uart, nmeaMsg):
    s = 'ZED1: ' + nmeaMsg.decode('utf-8')
    fp1.write(s + '\n')
    print(s)

# ---------------------------------------------------------------
# ZED2 GNSS NMEA message received callback
# ---------------------------------------------------------------
def OnNmeaMsg2(uart, nmeaMsg):
    s = 'ZED2: ' + nmeaMsg.decode('utf-8')
    fp2.write(s + '\n')
    print(s)

# Parser configuration
zed1_uart.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg1)
zed2_uart.parser(UART.ParserNMEA, rxbuf=256, rxcallback=OnNmeaMsg2)

# ---------------------------------------------------------------
# FAT power failure test
# ---------------------------------------------------------------
reset = ((sty.rng() % 20) + 10) * 1000
start = utime.ticks_ms()

# ---------------------------------------------------------------
# Thread #1 process
# ---------------------------------------------------------------
async def thread1_proc():
    global fp1, fp2
    while True:
        # ZED1 NMEA framer processor
        zed1_uart.process(UART.ParserNMEA)

        # ZED2 NMEA framer processor
        zed2_uart.process(UART.ParserNMEA)

        # Yield to the other tasks
        await asyncio.sleep_ms(10)

# ---------------------------------------------------------------
# Thread #2 process
# ---------------------------------------------------------------
async def thread2_proc():
    global start, reset
    while True:
        if utime.ticks_diff(utime.ticks_ms(), start) > reset:
            machine.reset()
        led2.toggle()
        await asyncio.sleep_ms(10)

# ---------------------------------------------------------------
# Thread #3 process
# ---------------------------------------------------------------
async def thread3_proc():
    while True:
        led3.toggle()
        await asyncio.sleep_ms(100)

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
