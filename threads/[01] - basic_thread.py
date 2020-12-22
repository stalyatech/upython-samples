import uasyncio
from sty import LED

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = LED(1)
led2 = LED(2)
led3 = LED(3)

# ---------------------------------------------------------------
# Thread #1 process
# ---------------------------------------------------------------
async def thread1_proc():
    while True:
        led1.toggle()
        await uasyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Thread #2 process
# ---------------------------------------------------------------
async def thread2_proc():
    while True:
        led2.toggle()
        await uasyncio.sleep_ms(200)

# ---------------------------------------------------------------
# Thread #3 process
# ---------------------------------------------------------------
async def thread3_proc():
    while True:
        led3.toggle()
        await uasyncio.sleep_ms(300)

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
