import network
from sty import Pin
from sty import UART
import uasyncio as asyncio

# ---------------------------------------------------------------
# GSM Module Communication based socket interface (on XBEE-HP)
# ---------------------------------------------------------------

# Configure the network interface card (GSM)
pwr = Pin('PWR_XBEE_HP', Pin.OUT_OD)
nic = network.GSM(UART('XBEE_HP', 115200, rxbuf=1024, dma=False), pwr_pin=pwr, info=True)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc(url, port):
    # Print info
    print('GSM connection started...\r\n')

    # Configure the GSM parameters
    nic.config(user='gprs', pwd='gprs', apn='internet', pin='1234')

    # Connect to the gsm network
    nic.connect()

    # Wait till connection
    while not nic.isconnected():
        await asyncio.sleep_ms(100)

    # Status info
    ipaddr = nic.ifconfig('ipaddr')
    print('GSM connection done: %s' % ipaddr)

    # GSM info
    print('IMEI Number: %s' % nic.imei())
    print('IMSI Number: %s' % nic.imsi())
    qos = nic.qos()
    print('Signal Quality: %d,%d' % (qos[0], qos[1]))

    # Get the stream reader/writer while connwcto to the host
    reader, writer = await asyncio.open_connection(url, port)

    # Send header data to the host
    print('Write GET')
    writer.write(b'GET / HTTP/1.0\r\n\r\n')
    await writer.drain()

    # Get the data
    while True:
        line = await reader.readline()
        line = line.strip()
        if not line:
            break
        if (line.find(b"Date") == -1 and line.find(b"Modified") == -1 and line.find(b"Server") == -1):
            print(line)

    # Close the stream
    print("Close")
    writer.close()
    await writer.wait_closed()

    # Disconnect from the gsm network
    nic.disconnect()
    print('This is simple socket application based on GSM NIC with CMUX support\r\n')

# ---------------------------------------------------------------
# Start the application process
# ---------------------------------------------------------------
asyncio.run(app_proc('google.com', 80))
