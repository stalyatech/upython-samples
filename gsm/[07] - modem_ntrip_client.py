import binascii
import network
import machine
import sty
from sty import Pin
from sty import UART
import uasyncio as asyncio

# ---------------------------------------------------------------
# GNSS UBX message received callback
# ---------------------------------------------------------------
def OnUbloxMsg(uart, ubxMsg):
    uart.parse_ubx(ubxMsg)

# ---------------------------------------------------------------
# GNSS UBX message parsed callback
# ---------------------------------------------------------------
def OnUbloxParsed(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# Base64 encoding
# ---------------------------------------------------------------
def b64encode(s):
    return binascii.b2a_base64(s)[:-1]

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------
led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# NTRIP Client informations
# ---------------------------------------------------------------
server = 'ntrip.stalya.com'
port = 2101
username = 'mcastillo@eps-works.com'
password = 'Nhx7tUPnv8eS9euY'
mountpoint = 'STYIST0'
authkey = b64encode("{}:{}".format(username, password)).decode('utf-8')
header =\
"GET /{} HTTP/1.0\r\n".format(mountpoint) +\
"User-Agent: NTRIP simpleRTK-SBC\r\n" +\
"Accept: */*\r\n" +\
"Authorization: Basic {}\r\n".format(authkey) +\
"Connection: close\r\n\r\n"

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# UART configuration of ZEDs with application buffer
zed1 = UART('ZED1', 115200, rxbuf=0, dma=True)

# Parser configurations
zed1.parser(UART.ParserUBX, rxbuf=2048, rxcallback=OnUbloxMsg, frcallback=OnUbloxParsed)

# ---------------------------------------------------------------
# GSM Module Communication based socket interface (on XBEE-HP)
# ---------------------------------------------------------------

# Configure the network interface card (GSM)
pwr = Pin('PWR_XBEE', Pin.OUT_OD)
nic = network.GSM(UART('XBEE_HP', 115200, rxbuf=1024, dma=False), pwr_pin=pwr, info=True)

# ---------------------------------------------------------------
# GSM connection status callback
# ---------------------------------------------------------------
def OnGsmStatus(status):
    print('Link : {}\r\nQoS  : {}\r\nBER  : {}'.format(status[0], status[1], status[2]))

# ---------------------------------------------------------------
# NTRIP client processor
# ---------------------------------------------------------------
async def ntrip_proc():
    global header
    global server
    global port

    # Print info
    print('GSM connection started...\r\n')

    # Configure the GSM parameters
    nic.config(user='gprs', pwd='gprs', apn='internet', pin='1234')

    # Connect to the gsm network
    nic.connect(OnGsmStatus)

    # Wait till connection
    while not nic.isconnected():
        await asyncio.sleep_ms(100)

    # Status info
    ifconfig = nic.ifconfig()
    print('GSM connection done: %s' % ifconfig[0])

    # GSM info
    print('IMEI Number: %s' % nic.imei())
    print('IMSI Number: %s' % nic.imsi())
    qos = nic.qos()
    print('Signal Quality: %d,%d' % (qos[0], qos[1]))

    # Get the stream reader/writer while connwcto to the host
    reader, writer = await asyncio.open_connection(server, port)

    # Send header data to the host
    writer.write(header)
    await writer.drain()

    # Get data from the host
    try:
        data = await reader.read(256)
        print(data)
    except Exception:
        print('Not response from server!\r\n')

    try:
        while True:
            # Suspend for a while
            await asyncio.sleep_ms(1000)

            # There are some length bytes at the head here but it actually
            # seems more robust to simply let the higher level RTCMv3 parser
            # frame everything itself and bin the garbage as required.

            # Get the RTCM data from NTRIP caster
            data = await reader.read(2048)
            print(data)

            # Check the received data length
            if len(data) > 0 and not zed1.istxbusy():
                # Redirect it to the destination
                zed1.send(data)

    except Exception:
        print('Not response from server!\r\n')
    finally:

        # Close the stream
        writer.close()
        await writer.wait_closed()

        # Disconnect from the gsm network
        nic.disconnect()

# ---------------------------------------------------------------
# Message processor
# ---------------------------------------------------------------
async def msg_proc():
    while True:
        # Heart-beat
        led3.toggle()
        # Call the UBX framer function
        zed1.process(UART.ParserUBX)
        # Yield to the other tasks
        await asyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Main process
# ---------------------------------------------------------------
async def main():
    asyncio.create_task(msg_proc())
    while True:
        task = asyncio.create_task(ntrip_proc())
        await asyncio.wait_for(task, 3600)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()
