import machine
import uasyncio
from sty import LED
from sty import UART
from sty import Queue
from sty import Parser

# Initialize the static message queues
msgq_zed1 = Queue(count=10, size=128)
msgq_zed2 = Queue(count=10, size=128)

# ---------------------------------------------------------------
# NMEA message received callback of ZED1
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsgZED1(message):
    try:
        msgq_zed1.append(message)
    except IndexError:
        pass

# ---------------------------------------------------------------
# NMEA message received callback of ZED2
# It is called from ISR!!!
# Don't waste the CPU processing time.
# ---------------------------------------------------------------
def OnNmeaMsgZED2(message):
    try:
        msgq_zed2.append(message)
    except IndexError:
        pass

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = LED(1)
led2 = LED(2)
led3 = LED(3)

# ---------------------------------------------------------------
# File system usage
# ---------------------------------------------------------------
fext1 = 0
fext2 = 0

# Create the test files
fp1 = open('nmea_log1.000', 'a+')
fp2 = open('nmea_log2.000', 'a+')

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZEDs without application buffer and NMEA parser
zed1 = UART('ZED1', 460800, dma=True, parser=Parser(Parser.NMEA, rxbuf=128, rxcall=OnNmeaMsgZED1))
zed2 = UART('ZED2', 460800, dma=True, parser=Parser(Parser.NMEA, rxbuf=128, rxcall=OnNmeaMsgZED2))

# ---------------------------------------------------------------
# Thread #1 process
# ---------------------------------------------------------------
async def thread1_proc():
    global fext1, fext2
    global fp1, fp2

    while True:
        # Write the ZED1 NMEA messages
        try:
            msg = 'ZED1: ' + msgq_zed1.popleft().decode('utf-8')
            fp1.write(msg)
            fp1.flush()
            print(msg[:-2])
        except Exception:
            pass

        # Write the ZED2 NMEA messages
        try:
            msg = 'ZED2: ' + msgq_zed2.popleft().decode('utf-8')
            fp2.write(msg)
            fp2.flush()
            print(msg[:-2])
        except Exception:
            pass

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
        await uasyncio.sleep_ms(10)

# ---------------------------------------------------------------
# Thread #2 process
# ---------------------------------------------------------------
async def thread2_proc():
    while True:
        led2.toggle()
        await uasyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Thread #3 process
# ---------------------------------------------------------------
async def thread3_proc():
    while True:
        led3.toggle()
        await uasyncio.sleep_ms(500)

# ---------------------------------------------------------------
# Main process
# ---------------------------------------------------------------
async def main():
    task1 = uasyncio.create_task(thread1_proc())
    task2 = uasyncio.create_task(thread2_proc())
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
        led1.off()
        led2.off()
        led3.off()
