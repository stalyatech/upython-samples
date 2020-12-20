import gc
import json
import binascii
import network
import machine
import uasyncio
import sty
from sty import UART
from sty import Parser

# ---------------------------------------------------------------
# COPY THE "config.json" FILE TO THE PYTHON DEVICE !!!
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# UBX message received callback
# ---------------------------------------------------------------
def OnUbloxMsg(parser, ubxMsg):
    parser.decode(ubxMsg)

# ---------------------------------------------------------------
# UBX message decoded callback for ZED1
# ---------------------------------------------------------------
def OnUbloxDecodedZED1(msgType, msgItems):
    print('ZED1: ', msgType, msgItems)

# ---------------------------------------------------------------
# UBX message decoded callback for ZED2
# ---------------------------------------------------------------
def OnUbloxDecodedZED2(msgType, msgItems):
    print('ZED2: ', msgType, msgItems)

# ---------------------------------------------------------------
# Base64 encoding
# ---------------------------------------------------------------
def b64encode(s):
    return binascii.b2a_base64(s)[:-1]

# ---------------------------------------------------------------
# Ethernet link status callback
# ---------------------------------------------------------------
def OnLinkStatus(link):
    if link:
        print('Link Up')
    else:
        print('Link Down!')
        nic.active(True)

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------
led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# NTRIP Client informations
# ---------------------------------------------------------------
HOST_CONN_TIMEOUT = 30
DATA_READ_TIMEOUT = 5

# Read from config file
config = open('config.json')
c = json.load(config)
config.close()

# Prepare authorization info
authkey = b64encode("{}:{}".format(c['caster']['username'], c['caster']['password'])).decode('utf-8')
header =\
"GET /{} HTTP/1.0\r\n".format(c['mountpoint']) +\
"User-Agent: NTRIP simpleRTK-SBC\r\n" +\
"Accept: */*\r\n" +\
"Authorization: Basic {}\r\n".format(authkey) +\
"Connection: close\r\n\r\n"

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZED1 without application buffer and UBX parser
zed1 = UART('ZED1', 115200, rxbuf=0, dma=True, parser=Parser(Parser.UBX, rxbuf=256, rxcall=OnUbloxMsg, decall=OnUbloxDecodedZED1))

# UART configuration of ZED2 without application buffer and UBX parser
zed2 = UART('ZED2', 115200, rxbuf=0, dma=True, parser=Parser(Parser.UBX, rxbuf=256, rxcall=OnUbloxMsg, decall=OnUbloxDecodedZED2))

# ---------------------------------------------------------------
# Ethernet based socket interface
# ---------------------------------------------------------------

# Configure the network interface card (Ethernet)
nic = network.LAN(OnLinkStatus)

# Enable the automatic garbage collection
gc.enable()

# ---------------------------------------------------------------
# Attempt to connect to the host
# ---------------------------------------------------------------
async def DoConnect(host, port, request):
    print('Connecting to %s:%d' % (host, port))

    try:
        # Get the stream reader/writer while connect to the host in 30 seconds
        reader, writer = await uasyncio.wait_for(uasyncio.open_connection(host, port), timeout=HOST_CONN_TIMEOUT)

        # Send request data to the host
        writer.write(request)
        await writer.drain()

        # Get response from the server
        if await GetResponse(reader):
            # Return with streams
            return reader, writer
    except Exception as Exc:
        raise Exc

# ---------------------------------------------------------------
# Get response from the host
# ---------------------------------------------------------------
async def GetResponse(reader):
    ret = False

    # Get data from the host
    try:
        # Wait data
        data = await uasyncio.wait_for(reader.read(256), timeout=DATA_READ_TIMEOUT)

        # Parse the response
        response = data.decode('utf-8').strip()
        if response.startswith('HTTP/1.1'):
            response_code = response[9:12]
            if response_code == "200":
                print("Successfully connected to mountpoint")
                ret = True
            else:
                print("Error connecting to mountpoint:")
                print(response[9:])
        elif response in ('OK', 'ICY 200 OK'):
            print("Successfully connected to mountpoint")
            print(response)
            ret = True
        else:
            print("Error connecting to mountpoint:")
            print(response)
    except Exception:
        print('Not response from server!\r\n')

    return ret

# ---------------------------------------------------------------
# NTRIP client processor
# ---------------------------------------------------------------
async def ntrip_proc(request):
    while True:
        # Print info
        print('\r\nWaiting for link-up')

        # Activate the interface
        nic.active(True)

        # Wait for ethernet link up
        while nic.status() == 0:
            await uasyncio.sleep_ms(100)

        # Print info
        print('DHCP started')

        # Configure the DHCP client and get IP address
        nic.ifconfig(mode='dhcp')

        # Status info
        ipaddr = nic.ifconfig('ipaddr')
        print('DHCP done: %s\r\n' % ipaddr)

        try:
            # Connect to the host
            reader, writer = await DoConnect(c['caster']['host'], c['caster']['port'], request)

            try:
                # Get the RTCM data from the host and redirect it to the ZEDs
                while True:

                    # Heart-beat for NTRIP task
                    led2.toggle()

                    # There are some length bytes at the head here but it actually
                    # seems more robust to simply let the higher level RTCMv3 parser
                    # frame everything itself and bin the garbage as required.

                    # Get the RTCM data from NTRIP caster
                    data = await uasyncio.wait_for(reader.read(1024), timeout=DATA_READ_TIMEOUT)

                    # Send the data to the ZEDs
                    if len(data) > 0:
                        zed1.send(data)
                        zed2.send(data)
                    else:
                        raise Exception('Data Error!')

                    # Check the link status
                    if nic.status() == 0:
                        raise Exception('Link Error!')

                    # Suspend for a while
                    await uasyncio.sleep_ms(100)

            # Exception while data read!
            except Exception as Exc:
                print(Exc)
            finally:

                # Close the stream
                writer.close()
                await writer.wait_closed()
                print('Stream Closed!')

                # De-activate the interface
                nic.active(False)

        # Exception while open connection
        except Exception:
            # De-activate the interface
            nic.active(False)


# ---------------------------------------------------------------
# Message processor
# ---------------------------------------------------------------
async def msg_proc():
    while True:
        # Heart-beat for message processor task
        led3.toggle()

        # Yield to the other tasks
        await uasyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Main process
# ---------------------------------------------------------------
async def main():
    uasyncio.create_task(msg_proc())
    while True:
        await uasyncio.create_task(ntrip_proc(header))

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        loop = uasyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        uasyncio.new_event_loop()