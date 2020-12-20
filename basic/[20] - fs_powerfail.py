import utime
import uasyncio
import machine
import sty
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# NMEA message received callback of ZED1
# ---------------------------------------------------------------
def OnNmeaMsgZED1(parser, nmeaMsg):
    s = 'ZED1: ' + nmeaMsg.decode('utf-8')
    fp1.write(s + '\n')
    print(s)

# ---------------------------------------------------------------
# NMEA message received callback of ZED2
# ---------------------------------------------------------------
def OnNmeaMsgZED2(uart, nmeaMsg):
    s = 'ZED2: ' + nmeaMsg.decode('utf-8')
    fp2.write(s + '\n')
    print(s)

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
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZEDs without application buffer and NMEA parser
zed1 = UART('ZED1', 115200, rxbuf=0, dma=True, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsgZED1))
zed2 = UART('ZED2', 115200, rxbuf=0, dma=True, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsgZED2))

# ---------------------------------------------------------------
# FAT power failure test
# ---------------------------------------------------------------
reset = ((sty.rng() % 20) + 10) * 1000
start = utime.ticks_ms()

# ---------------------------------------------------------------
# Thread #1 process
# ---------------------------------------------------------------
async def thread1_proc():
    while True:
        # Yield to the other tasks
        await uasyncio.sleep_ms(10)

# ---------------------------------------------------------------
# Thread #2 process
# ---------------------------------------------------------------
async def thread2_proc(start_tick, reset_tick):
    while True:
        if utime.ticks_diff(utime.ticks_ms(), start_tick) > reset_tick:
            machine.reset()
        led2.toggle()
        await uasyncio.sleep_ms(10)

# ---------------------------------------------------------------
# Thread #3 process
# ---------------------------------------------------------------
async def thread3_proc():
    while True:
        led3.toggle()
        await uasyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Main process
# ---------------------------------------------------------------
async def main():
    uasyncio.create_task(thread1_proc())
    uasyncio.create_task(thread2_proc(start, reset))
    uasyncio.create_task(thread3_proc())
    loop = uasyncio.get_event_loop()
    loop.run_forever()

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        uasyncio.new_event_loop()
