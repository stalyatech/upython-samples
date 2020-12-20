import machine
import uasyncio
import sty
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# NMEA message received callback of ZED1
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnNmeaMsgZED1(params):
    s = 'ZED1: ' + params[1].decode('utf-8')
    fp1.write(s + '\n')
    print(s)

# ---------------------------------------------------------------
# NMEA message received callback of ZED2
# params[0] : Parser object
# params[1] : Message object
# ---------------------------------------------------------------
def OnNmeaMsgZED2(params):
    s = 'ZED2: ' + params[1].decode('utf-8')
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
zed1 = UART('ZED1', 115200, dma=True, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsgZED1))
zed2 = UART('ZED2', 115200, dma=True, parser=Parser(Parser.NMEA, rxbuf=256, rxcall=OnNmeaMsgZED2))

# ---------------------------------------------------------------
# Thread #1 process
# ---------------------------------------------------------------
async def thread1_proc():
    global fext1, fext2
    global fp1, fp2

    while True:
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
    uasyncio.create_task(thread1_proc())
    uasyncio.create_task(thread2_proc())
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
