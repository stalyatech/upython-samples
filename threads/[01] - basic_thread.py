import uasyncio as asyncio
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
        await asyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Thread #2 process
# ---------------------------------------------------------------
async def thread2_proc():
    while True:
        led2.toggle()
        await asyncio.sleep_ms(200)

# ---------------------------------------------------------------
# Thread #3 process
# ---------------------------------------------------------------
async def thread3_proc():
    while True:
        led3.toggle()
        await asyncio.sleep_ms(300)

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
