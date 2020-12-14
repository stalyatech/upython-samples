import gc
import binascii
import network
import machine
import uasyncio
import sty
from sty import UART

# ---------------------------------------------------------------
#                 RTCM Message Parser Definitions
# ---------------------------------------------------------------
RTCM3_PREAMBLE = 0xD3
RTCM3_DATAOFFS = 3
RTCM3_MINSIZE  = 6

# ---------------------------------------------------------------
#                      CRC24 LOOKUP TABLE
# ---------------------------------------------------------------
crc24table = (
    0x000000, 0x864CFB, 0x8AD50D, 0x0C99F6, 0x93E6E1, 0x15AA1A,
    0x1933EC, 0x9F7F17, 0xA18139, 0x27CDC2, 0x2B5434, 0xAD18CF,
    0x3267D8, 0xB42B23, 0xB8B2D5, 0x3EFE2E, 0xC54E89, 0x430272,
    0x4F9B84, 0xC9D77F, 0x56A868, 0xD0E493, 0xDC7D65, 0x5A319E,
    0x64CFB0, 0xE2834B, 0xEE1ABD, 0x685646, 0xF72951, 0x7165AA,
    0x7DFC5C, 0xFBB0A7, 0x0CD1E9, 0x8A9D12, 0x8604E4, 0x00481F,
    0x9F3708, 0x197BF3, 0x15E205, 0x93AEFE, 0xAD50D0, 0x2B1C2B,
    0x2785DD, 0xA1C926, 0x3EB631, 0xB8FACA, 0xB4633C, 0x322FC7,
    0xC99F60, 0x4FD39B, 0x434A6D, 0xC50696, 0x5A7981, 0xDC357A,
    0xD0AC8C, 0x56E077, 0x681E59, 0xEE52A2, 0xE2CB54, 0x6487AF,
    0xFBF8B8, 0x7DB443, 0x712DB5, 0xF7614E, 0x19A3D2, 0x9FEF29,
    0x9376DF, 0x153A24, 0x8A4533, 0x0C09C8, 0x00903E, 0x86DCC5,
    0xB822EB, 0x3E6E10, 0x32F7E6, 0xB4BB1D, 0x2BC40A, 0xAD88F1,
    0xA11107, 0x275DFC, 0xDCED5B, 0x5AA1A0, 0x563856, 0xD074AD,
    0x4F0BBA, 0xC94741, 0xC5DEB7, 0x43924C, 0x7D6C62, 0xFB2099,
    0xF7B96F, 0x71F594, 0xEE8A83, 0x68C678, 0x645F8E, 0xE21375,
    0x15723B, 0x933EC0, 0x9FA736, 0x19EBCD, 0x8694DA, 0x00D821,
    0x0C41D7, 0x8A0D2C, 0xB4F302, 0x32BFF9, 0x3E260F, 0xB86AF4,
    0x2715E3, 0xA15918, 0xADC0EE, 0x2B8C15, 0xD03CB2, 0x567049,
    0x5AE9BF, 0xDCA544, 0x43DA53, 0xC596A8, 0xC90F5E, 0x4F43A5,
    0x71BD8B, 0xF7F170, 0xFB6886, 0x7D247D, 0xE25B6A, 0x641791,
    0x688E67, 0xEEC29C, 0x3347A4, 0xB50B5F, 0xB992A9, 0x3FDE52,
    0xA0A145, 0x26EDBE, 0x2A7448, 0xAC38B3, 0x92C69D, 0x148A66,
    0x181390, 0x9E5F6B, 0x01207C, 0x876C87, 0x8BF571, 0x0DB98A,
    0xF6092D, 0x7045D6, 0x7CDC20, 0xFA90DB, 0x65EFCC, 0xE3A337,
    0xEF3AC1, 0x69763A, 0x578814, 0xD1C4EF, 0xDD5D19, 0x5B11E2,
    0xC46EF5, 0x42220E, 0x4EBBF8, 0xC8F703, 0x3F964D, 0xB9DAB6,
    0xB54340, 0x330FBB, 0xAC70AC, 0x2A3C57, 0x26A5A1, 0xA0E95A,
    0x9E1774, 0x185B8F, 0x14C279, 0x928E82, 0x0DF195, 0x8BBD6E,
    0x872498, 0x016863, 0xFAD8C4, 0x7C943F, 0x700DC9, 0xF64132,
    0x693E25, 0xEF72DE, 0xE3EB28, 0x65A7D3, 0x5B59FD, 0xDD1506,
    0xD18CF0, 0x57C00B, 0xC8BF1C, 0x4EF3E7, 0x426A11, 0xC426EA,
    0x2AE476, 0xACA88D, 0xA0317B, 0x267D80, 0xB90297, 0x3F4E6C,
    0x33D79A, 0xB59B61, 0x8B654F, 0x0D29B4, 0x01B042, 0x87FCB9,
    0x1883AE, 0x9ECF55, 0x9256A3, 0x141A58, 0xEFAAFF, 0x69E604,
    0x657FF2, 0xE33309, 0x7C4C1E, 0xFA00E5, 0xF69913, 0x70D5E8,
    0x4E2BC6, 0xC8673D, 0xC4FECB, 0x42B230, 0xDDCD27, 0x5B81DC,
    0x57182A, 0xD154D1, 0x26359F, 0xA07964, 0xACE092, 0x2AAC69,
    0xB5D37E, 0x339F85, 0x3F0673, 0xB94A88, 0x87B4A6, 0x01F85D,
    0x0D61AB, 0x8B2D50, 0x145247, 0x921EBC, 0x9E874A, 0x18CBB1,
    0xE37B16, 0x6537ED, 0x69AE1B, 0xEFE2E0, 0x709DF7, 0xF6D10C,
    0xFA48FA, 0x7C0401, 0x42FA2F, 0xC4B6D4, 0xC82F22, 0x4E63D9,
    0xD11CCE, 0x575035, 0x5BC9C3, 0xDD8538)

# ---------------------------------------------------------------
# Compute the CRC24 checksum using a lookup table method.
# ---------------------------------------------------------------
def rtcm_crc24q(buff):
    crc = 0

    for b in buff:
        crc = crc24table[((crc >> 16) ^ b) & 0xFF] ^ (crc << 8)

    return crc & 0xFFFFFF

# ---------------------------------------------------------------
# Extract unsigned/signed bits from byte data.
# ---------------------------------------------------------------
def rtcm_getbitu(buff, pos, size):
    bits = 0

    for i in range(pos, pos + size):
        bits = ((bits << 1) + ((buff[i >> 3] >> (7 - (i & 7))) & 1))

    return bits

# ---------------------------------------------------------------
# RTCM Message Parser Class
# ---------------------------------------------------------------
class RTCM3:
    def __init__(self):
        self.undecoded = bytearray("")
        self.buffer = bytearray("")
        self.packet = bytearray("")
        self.pack_id = None
        self.pack_len = None

    def add(self, data):
        self.buffer += data

    def proc(self):

        # check the length
        if len(self.buffer) < RTCM3_MINSIZE:
            return None

        # trim until first start
        if self.buffer[0] != RTCM3_PREAMBLE:
            for i in range(1, len(self.buffer)):
                if self.buffer[i] == RTCM3_PREAMBLE:
                    self.buffer = self.buffer[i:]
                    break
                self.undecoded.append(self.buffer[i])
            return None

        # get the payload length + preample + length (16-bit)
        self.pack_len = rtcm_getbitu(self.buffer, 14, 10) + 3

        # wait for packet end
        if len(self.buffer) < (self.pack_len + 3):
            return None

        # computed CRC
        comp_crc = rtcm_crc24q(self.buffer[0:self.pack_len])

		# received CRC
        pack_crc = rtcm_getbitu(self.buffer, self.pack_len * 8, 24)

        # check the CRC
        if comp_crc == pack_crc:
            self.pack_id = self.buffer[RTCM3_DATAOFFS]
            self.pack_id = self.pack_id << 4
            self.pack_id = self.pack_id | ((self.buffer[RTCM3_DATAOFFS + 1] >> 4) & 0x0F)
            print("Packet ID: {}".format(self.pack_id))

            # get the raw packet including CRC
            self.packet = self.buffer[0:self.pack_len + 3]

            # trim the buffer
            self.buffer = self.buffer[self.pack_len + 3:]

            # clear the undecoded buffer
            self.undecoded = bytearray("")

            # return with the packet
            return self.packet

        # trim to first start
        trim = False
        for i in range(1, len(self.buffer)):
            if self.buffer[i] == RTCM3_PREAMBLE:
                self.buffer = self.buffer[i:]
                trim = True
                break
            self.undecoded.append(self.buffer[i])
        if not trim:
            self.buffer = bytearray("")

        print("Checksum Error!: {}".format(len(self.buffer)))
        return ValueError

    def get(self):
        # Add all valid RTCM messages to the list
        msglist = []
        msg = self.proc()
        while msg not in (None, ValueError):
            msglist.append(msg)
            msg = self.proc()

        # if there is an error so clear the message list to keep
        # all correction message count same!
        if (msg == ValueError) and len(msglist) > 0:
            msglist.clear()

        return msglist

    def empty(self):
        if len(self.buffer) == 0:
            return True
        return False

# ---------------------------------------------------------------
# GNSS UBX message received callback
# ---------------------------------------------------------------
def OnUbloxMsg(uart, ubxMsg):
    uart.parse_ubx(ubxMsg)

# ---------------------------------------------------------------
# GNSS UBX message parsed callback for ZED1
# ---------------------------------------------------------------
def OnUbloxParsedZED1(msgType, msgItems):
    print(msgType, msgItems)

# ---------------------------------------------------------------
# GNSS UBX message parsed callback for ZED2
# ---------------------------------------------------------------
def OnUbloxParsedZED2(msgType, msgItems):
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
username = 'stalya'
password = '1234'
mountpoint = 'STYIST0'
authkey = b64encode("{}:{}".format(username, password)).decode('utf-8')
header =\
"GET /{} HTTP/1.0\r\n".format(mountpoint) +\
"User-Agent: NTRIP simpleRTK-SBC\r\n" +\
"Accept: */*\r\n" +\
"Authorization: Basic {}\r\n".format(authkey) +\
"Connection: close\r\n\r\n"

# ---------------------------------------------------------------
# RTCM message parser
# ---------------------------------------------------------------

rtcm = RTCM3()

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
pwr = machine.Power()
pwr.on(machine.POWER_GNSS)

# UART configuration of ZEDs without application buffer
zed1 = UART('ZED1', 115200, rxbuf=0, dma=True)
zed2 = UART('ZED2', 115200, rxbuf=0, dma=True)

# Parser configurations
zed1.parser(UART.ParserUBX, rxbuf=2048, rxcallback=OnUbloxMsg, frcallback=OnUbloxParsedZED1)
zed2.parser(UART.ParserUBX, rxbuf=2048, rxcallback=OnUbloxMsg, frcallback=OnUbloxParsedZED2)

# ---------------------------------------------------------------
# Ethernet based socket interface
# ---------------------------------------------------------------

# Configure the network interface card (Ethernet)
nic = network.LAN()

# Enable the automatic garbage collection
gc.enable()

# ---------------------------------------------------------------
# NTRIP client processor
# ---------------------------------------------------------------
async def ntrip_proc():
    global header
    global server
    global port

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

    # Get the stream reader/writer while connect to the host
    reader, writer = await uasyncio.open_connection(server, port)

    # Send header data to the host
    writer.write(header)
    await writer.drain()

    # Get data from the host
    try:
        # Wait data
        data = await reader.read(256)

        # Parse the response
        response = data.decode('utf-8').strip()
        if response.startswith('HTTP/1.1'):
            response_code = response[9:12]
            if response_code == "200":
                print("Successfully connected to mountpoint")
            else:
                print("Error connecting to mountpoint:")
                print(response[9:])
        elif response in ('OK', 'ICY 200 OK'):
            print("Successfully connected to mountpoint")
            print(response)
        else:
            print("Error connecting to mountpoint:")
            print(response)
    except Exception:
        print('Not response from server!\r\n')

    try:
        while True:

            # Heart-beat
            led3.toggle()

            # There are some length bytes at the head here but it actually
            # seems more robust to simply let the higher level RTCMv3 parser
            # frame everything itself and bin the garbage as required.

            # Get the RTCM data from NTRIP caster
            data = await reader.read(1024)

            # Add data to the parser
            rtcm.add(data)

            # Get all valid RTCM messages
            msglist = rtcm.get()

            # Send all messages without blocking
            if len(msglist) > 0:
                cnt = zed1.send(msglist)
                if cnt != len(msglist):
                    print("Unsent Messages!: {}".format(len(msglist) - cnt))

                # Clear the list
                msglist.clear()

            # Suspend for a while
            if rtcm.empty():
                await uasyncio.sleep_ms(1000)

    except Exception as e:
        print(e)
    finally:

        # Close the stream
        writer.close()
        await writer.wait_closed()

        # Deactivate the interface
        nic.active(False)

# ---------------------------------------------------------------
# Message processor
# ---------------------------------------------------------------
async def msg_proc():
    while True:
        # Call the UBX framer function
        zed1.process(UART.ParserUBX)
        # Yield to the other tasks
        await uasyncio.sleep_ms(100)

# ---------------------------------------------------------------
# Main process
# ---------------------------------------------------------------
async def main():
    uasyncio.create_task(msg_proc())
    while True:
        task = uasyncio.create_task(ntrip_proc())
        await uasyncio.wait_for(task, 3600)

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
