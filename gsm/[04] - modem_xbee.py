import uasyncio
import network
from sty import Pin
from sty import UART

# ---------------------------------------------------------------
# GSM Module Communication based socket interface (on XBEE-HP)
# ---------------------------------------------------------------

# Configure the network interface card (GSM)
pwr = Pin('PWR_XBEE', Pin.OUT_OD)
nic = network.GSM(UART('XBEE_HP', 115200, rxbuf=1024, dma=False), pwr_pin=pwr, info=True)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc(url, port):

    # Print info
    print('\r\nWaiting for link-up')

    # Configure the GSM parameters
    nic.config(user='gprs', pwd='gprs', apn='internet', pin='1234')

    # Connect to the gsm network
    nic.connect()

    # Wait for connection
    while not nic.isconnected():
        await uasyncio.sleep_ms(100)

    # Status info
    ipaddr = nic.ifconfig('ipaddr')
    print('GSM connection done: %s' % ipaddr)

    # GSM info
    print('IMEI Number: %s' % nic.imei())
    print('IMSI Number: %s' % nic.imsi())
    qos = nic.qos()
    print('Signal Quality: %d,%d' % (qos[0], qos[1]))

    # Get the stream reader/writer while connwcto to the host
    reader, writer = await uasyncio.open_connection(url, port)

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
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc('google.com', 80))
    except KeyboardInterrupt:
        print('Interrupted')
        nic.disconnect()
