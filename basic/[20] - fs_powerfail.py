from collections import deque
import utime
import uasyncio
import machine
import sty
from sty import UART
from sty import Parser

# Initializing the message queues
msgq_zed1 = deque((), 10)
msgq_zed2 = deque((), 10)

# ---------------------------------------------------------------
# NMEA message received callback of ZED1
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsgZED1(message):
    msgq_zed1.append(message)

# ---------------------------------------------------------------
# NMEA message received callback of ZED2
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsgZED2(message):
    msgq_zed2.append(message)

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
zed1 = UART('ZED1', 115200, dma=True, dmabuf=1024, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsgZED1))
zed2 = UART('ZED2', 115200, dma=True, dmabuf=1024, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsgZED2))

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
        # Write the ZED1 NMEA messages
        try:
            msg = msgq_zed1.popleft().decode('utf-8')
            s = 'ZED1: ' + msg
            fp1.write(s + '\n')
            print(s)
        except Exception:
            pass

        # Write the ZED2 NMEA messages
        try:
            msg = msgq_zed2.popleft().decode('utf-8')
            s = 'ZED2: ' + msg
            fp2.write(s + '\n')
            print(s)
        except Exception:
            pass

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
    task1 = uasyncio.create_task(thread1_proc())
    task2 = uasyncio.create_task(thread2_proc(start, reset))
    task3 = uasyncio.create_task(thread3_proc())
    await (task1, task2, task3)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
