import re
import gc
import math
import json
import binascii
import network
import machine
import uasyncio
from sty import Imu
from sty import Pin
from sty import UART
from sty import Queue
from sty import Parser

# ---------------------------------------------------------------
# NTRIP Client
# ---------------------------------------------------------------
class NtripClient:

    # -----------------------------------------------------------
    # COPY THE "config.json" FILE TO THE PYTHON DEVICE !!!
    # -----------------------------------------------------------

    # -----------------------------------------------------------
    # Constructor
    # -----------------------------------------------------------
    def __init__(self, conn_timeout=30, read_timeout=10, on_data_recv=None, on_link_stat=None):
        self.__conn_timeout = conn_timeout
        self.__read_timeout = read_timeout
        self.__on_data_recv = on_data_recv
        self.__on_link_stat = on_link_stat
        self.__eth_nic = None
        self.__gsm_nic = None

        # Read from config file
        fd = open('config.json')
        cfg = json.load(fd)
        fd.close()

        # Get the configuration values
        self.__user = cfg['caster']['username']
        self.__pwd  = cfg['caster']['password']
        self.__host = cfg['caster']['host']
        self.__port = cfg['caster']['port']
        self.__mountpnt = cfg['mountpoint']

        # Prepare authorization info
        authkey = self.__b64encode("{}:{}".format(self.__user, self.__pwd)).decode('utf-8')
        self.__header =\
        "GET /{} HTTP/1.0\r\n".format(self.__mountpnt) +\
        "User-Agent: NTRIP simpleRTK-SBC\r\n" +\
        "Accept: */*\r\n" +\
        "Authorization: Basic {}\r\n".format(authkey) +\
        "Connection: close\r\n\r\n"

    # -----------------------------------------------------------
    # Base64 encoding
    # -----------------------------------------------------------
    @staticmethod
    def __b64encode(s):
        return binascii.b2a_base64(s)[:-1]

    # -----------------------------------------------------------
    # Get response from the host
    # -----------------------------------------------------------
    async def __getResponse(self, reader):
        ret = False

        # Get data from the host
        try:
            # Wait data
            data = await uasyncio.wait_for(reader.read(256), timeout=self.__read_timeout)

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
    # Attempt to connect to the host
    # ---------------------------------------------------------------
    async def __connect(self):
        print('Connecting to %s:%d' % (self.__host, self.__port))

        try:
            # Get the stream reader/writer while connect to the host in 30 seconds
            reader, writer = await uasyncio.wait_for(uasyncio.open_connection(self.__host, self.__port), timeout=self.__conn_timeout)

            # Send request data to the host
            writer.write(self.__header)
            await writer.drain()

            # Get response from the server
            if await self.__getResponse(reader):
                # Return with streams
                return reader, writer
        except Exception as Exc:
            raise Exc

    # ---------------------------------------------------------------
    # Background process for ethernet connection
    # ---------------------------------------------------------------
    async def __process_eth(self):
        while True:
            try:
                # Print info
                print('\r\nWaiting for link-up')

                # Activate the interface
                self.__eth_nic.active(True)

                # Wait for ethernet link up
                while self.__eth_nic.status() == 0:
                    await uasyncio.sleep(1)

                # Print info
                print('DHCP started')

                # Configure the DHCP client and get IP address
                self.__eth_nic.ifconfig(mode='dhcp')

                # Status info
                ipaddr = self.__eth_nic.ifconfig('ipaddr')
                print('DHCP done: %s\r\n' % ipaddr)

                try:
                    # Connect to the host
                    reader, writer = await self.__connect()

                    try:
                        # Get the RTCM data from the host and redirect it to the ZEDs
                        while True:

                            # There are some length bytes at the head here but it actually
                            # seems more robust to simply let the higher level RTCMv3 parser
                            # frame everything itself and bin the garbage as required.

                            # Get the RTCM data from NTRIP caster
                            data = await uasyncio.wait_for(reader.read(1024), timeout=self.__read_timeout)

                            # Send the data to the caller
                            if len(data) > 0:
                                if self.__on_data_recv:
                                    self.__on_data_recv(data)
                            else:
                                raise Exception('Data Error!')

                            # Check the link status
                            if self.__eth_nic.status() == 0:
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
                        self.__eth_nic.active(False)

                # Exception while open connection
                except Exception:
                    # De-activate the interface
                    self.__eth_nic.active(False)

            # Exception while Link Up/IP address get
            except Exception as Exc:
                print(Exc)

                # De-activate the interface
                self.__eth_nic.active(False)

    # ---------------------------------------------------------------
    # Background process for gsm connection
    # ---------------------------------------------------------------
    async def __process_gsm(self):
        while True:
            # Print info
            print('\r\nWaiting for link-up')

            # Configure the GSM parameters
            self.__gsm_nic.config(user='gprs', pwd='gprs', apn='internet', pin='1234')

            # Connect to the gsm network
            self.__gsm_nic.connect()

            # Wait till connection
            while not self.__gsm_nic.isconnected():
                await uasyncio.sleep(1)

            # Status info
            ipaddr = self.__gsm_nic.ifconfig('ipaddr')
            print('GSM connection done: %s' % ipaddr)

            # GSM info
            print('IMEI Number: %s' % self.__gsm_nic.imei())
            print('IMSI Number: %s' % self.__gsm_nic.imsi())
            qos = self.__gsm_nic.qos()
            print('Signal Quality: %d,%d' % (qos[0], qos[1]))

            try:
                # Connect to the host
                reader, writer = await self.__connect()

                try:
                    # Get the RTCM data from the host and redirect it to the ZEDs
                    while True:

                        # There are some length bytes at the head here but it actually
                        # seems more robust to simply let the higher level RTCMv3 parser
                        # frame everything itself and bin the garbage as required.

                        # Get the RTCM data from NTRIP caster
                        data = await uasyncio.wait_for(reader.read(1024), timeout=self.__read_timeout)

                        # Send the data to the caller
                        if len(data) > 0:
                            if self.__on_data_recv:
                                self.__on_data_recv(data)
                        else:
                            raise Exception('Data Error!')

                        # Check the link status
                        if not self.__gsm_nic.isconnected():
                            raise Exception('Link Error!')

                        # Suspend for a while
                        await uasyncio.sleep_ms(50)

                # Exception while data read!
                except Exception as Exc:
                    print(Exc)
                finally:

                    # Close the stream
                    writer.close()
                    await writer.wait_closed()
                    print('Stream Closed!')

                    # Disconnect from the network
                    self.__gsm_nic.disconnect()

            # Exception while open connection
            except Exception:
                # Disconnect from the network
                self.__gsm_nic.disconnect()

    # -----------------------------------------------------------
    # Start the background process
    # -----------------------------------------------------------
    def start(self, nic):
        if nic == 'eth':
            # Release the allocated resource for ethernet
            del self.__eth_nic

            # Configure the network interface card (Ethernet)
            self.__eth_nic = network.LAN(self.__on_link_stat)

            # Start the async process
            return uasyncio.create_task(self.__process_eth())

        if nic == 'gsm':
            # Release the allocated resource for gsm
            del self.__gsm_nic

            # Configure the network interface card (GSM)
            self.__gsm_nic = network.GSM(UART('GSM', 115200, flow=UART.RTS|UART.CTS, rxbuf=1024, dma=True), pwr_pin=Pin('PWR_GSM', Pin.OUT_OD), mon_pin=Pin('GSM_MON', Pin.IN, Pin.PULL_DOWN), info=True)

            # Start the async process
            return uasyncio.create_task(self.__process_gsm())

        return None

    # -----------------------------------------------------------
    # Link up/down
    # -----------------------------------------------------------
    def active(self, nic, status):
        if nic == 'eth':
            self.__eth_nic.active(status)

# ---------------------------------------------------------------
# GNSS Based AHRS Fiter
# ---------------------------------------------------------------
class AHRSFilter:

    # -----------------------------------------------------------
    # Constructor
    # -----------------------------------------------------------
    def __init__(self):
        self.__heading = 0
        self.__accuracy = 0
        self.__carrsoln = 0
        self.__bodyNED = (0.0, 0.0, 0.0)
        self.__groundNED = (0.0, 0.0, 0.0)
        self.__yaw = 0
        self.__roll = 0
        self.__pitch = 0
        self.__imu = Imu()
        self.__dcm = self.__imu.DCM(yawfix=True, kp_rollpitch=0.2, ki_rollpitch=0.00005, kp_yaw=2, ki_yaw=0.00005)

    # -----------------------------------------------------------
    # NMEA checksum calculation
    # -----------------------------------------------------------
    @staticmethod
    def __chksm(sentence):
        data = re.sub('(\n|\r\n)', '', sentence[1:sentence.find('*')])
        csum = 0
        for c in data:
            csum ^= ord(c)
        return '{:02X}'.format(csum)

    # -----------------------------------------------------------
    # Set the accuracy, heading and carrsoln
    # -----------------------------------------------------------
    def setValues(self, heading, accuracy, carrsoln):
        self.__accuracy = accuracy
        self.__carrsoln = carrsoln
        if self.__carrsoln == 2:
            self.__heading = -heading * 0.00001

    # -----------------------------------------------------------
    # Get the euler angles
    # -----------------------------------------------------------
    def getAngles(self):
        return (self.__roll, self.__pitch, self.__yaw)

    # -----------------------------------------------------------
    # Update the IMU values and apply the filter
    # -----------------------------------------------------------
    def update(self, relNED):
        # Wait for sensor ready
        while not self.__imu.ready():
            pass

        # Read the unfiltered values
        # ax, ay, az, gx, gy, gz, dt
        vals = self.__imu.read()

        # Update the filtered values (DCM algorithm)
        (self.__roll, self.__pitch, self.__yaw) = self.__dcm.update(vals, self.__heading * 0.017453292)

        # Update the transformation values (DCM algorithm)
        self.__bodyNED = relNED
        self.__groundNED = self.__dcm.transf(relNED)

    # -----------------------------------------------------------
    # Prepare heading NMEA sentence
    # -----------------------------------------------------------
    def getHeading(self):
        hdt = '$GPHDT,{:.3f},T*'.format(self.__yaw * -57.29577951)
        hdt = hdt + self.__chksm(hdt) + '\r\n'
        return hdt

# ---------------------------------------------------------------
# AgOpenGPS Class
# ---------------------------------------------------------------
class AgOpenGps:

    # Initialize the static message queues
    __msgq_nmea = Queue(count=100, size=256)
    __msgq_ublx = Queue(count=100, size=256)

    # AHRS filter
    __ahrs = AHRSFilter()

    # Dual antenna roll
    __rollHp = 0

    # North, East and Down components of relative position vector
    __relNED = (0.0, 0.0, 0.0)

    # -----------------------------------------------------------
    # Constructor
    # -----------------------------------------------------------
    def __init__(self, on_rtcm_msg=None, on_link_stat=None):

        # Parser configurations
        self.__nmea = Parser(Parser.NMEA, rxbuf=256, rxcall=self.__on_nmea_msg, decall=self.__on_nmea_dec)
        self.__ublx = Parser(Parser.UBX, rxbuf=256, rxcall=self.__on_ublx_msg, decall=self.__on_ublx_dec)

        # NTRIP client
        self.__ntrip = NtripClient(on_data_recv=on_rtcm_msg, on_link_stat=on_link_stat)

        # UART configuration of ZED1 without application buffer and NMEA parser
        self.__zed1 = UART('ZED1', 460800, dma=True, parser=self.__nmea)

        # UART configuration of ZED2 without application buffer and UBX parser
        self.__zed2 = UART('ZED2', 460800, dma=True, parser=self.__ublx)

        # UART configuration of service port without application buffer
        self.__srv = UART('SRV', 115200, dma=True)

        # Power-on the GNSS subsystem
        self.__pwr = machine.Power()
        self.__pwr.on(machine.POWER_GNSS)

    # -----------------------------------------------------------
    # Destructor
    # -----------------------------------------------------------
    def __del__(self):

        # Power-off the GNSS subsystem
        self.__pwr.off(machine.POWER_GNSS)

        # Delete all objects
        self.__zed1.deinit()
        self.__zed2.deinit()
        self.__srv.deinit()
        del self.__zed1
        del self.__zed2
        del self.__srv
        del self.__ntrip
        del self.__ublx
        del self.__nmea

    # ---------------------------------------------------------------
    # Background process
    # ---------------------------------------------------------------
    async def __process(self):
        while True:
            # Update the IMU values
            self.__ahrs.update(self.__relNED)

            # Decode the NMEA messages
            try:
                # Send the saved message
                msg = self.__msgq_nmea.popleft().decode('utf-8')
                #self.__srv.send(msg)
                print(msg[:-2])

                # Send the heading information
                msg = self.__ahrs.getHeading()
                #self.__srv.send(msg)
                print(msg[:-2])
            except Exception:
                pass

            # Decode the UBX messages
            try:
                self.__ublx.decode(self.__msgq_ublx.popleft())
            except IndexError:
                pass

            # Yield the next coro
            await uasyncio.sleep_ms(20)

    # -----------------------------------------------------------
    # NMEA message received callback
    # It is called from ISR!!!
    # Don't waste the CPU processing time.
    # -----------------------------------------------------------
    @staticmethod
    def __on_nmea_msg(message):
        try:
            AgOpenGps.__msgq_nmea.append(message)
        except IndexError:
            pass

    # ---------------------------------------------------------------
    # NMEA message decoded callback
    # ---------------------------------------------------------------
    @staticmethod
    def __on_nmea_dec(msgType, msgItems):
        pass

    # ---------------------------------------------------------------
    # UBX message received callback
    # It is called from ISR!!!
    # Don't waste the CPU processing time.
    # ---------------------------------------------------------------
    @staticmethod
    def __on_ublx_msg(message):
        try:
            AgOpenGps.__msgq_ublx.append(message)
        except IndexError:
            pass

    # ---------------------------------------------------------------
    # UBX message decoded callback
    # ---------------------------------------------------------------
    # NAV-RELPOSNED
    # msgItems[0] : North component of relative position vector
    # msgItems[1] : East component of relative position vector
    # msgItems[2] : Down component of relative position vector
    # msgItems[3] : Heading of the relative position vector
    # msgItems[4] : Accuracy of heading of the relative position vector
    # msgItems[5] : Flags
    # ---------------------------------------------------------------
    @staticmethod
    def __on_ublx_dec(msgType, msgItems):
        if msgType == 'NAV_RELPOSNED':
            AgOpenGps.__relNED = (float(msgItems[0]), float(msgItems[1]), float(msgItems[2]))
            N = AgOpenGps.__relNED[0]
            E = AgOpenGps.__relNED[1]
            D = AgOpenGps.__relNED[2]
            try:
                NE2 = math.sqrt(N * N + E * E)
                if NE2 > 0.0000001:
                    AgOpenGps.__rollHp = round(100 * math.atan(D / NE2) * 180 / 3.14159)
                else:
                    AgOpenGps.__rollHp = 90
            except Exception:
                pass
            carrsoln = (msgItems[5] & 0x18) >> 3
            AgOpenGps.__ahrs.setValues(msgItems[3], msgItems[4], carrsoln)

    # -----------------------------------------------------------
    # Start the background process
    # -----------------------------------------------------------
    def start(self, nic):
        task1 = self.__ntrip.start(nic)
        task2 = uasyncio.create_task(self.__process())
        return (task1, task2)

    # -----------------------------------------------------------
    # Send the RTCM message to the ZED1
    # -----------------------------------------------------------
    def correct(self, message):
        self.__zed1.send(message)

    # -----------------------------------------------------------
    # Link up/down
    # -----------------------------------------------------------
    def active(self, nic, status):
        self.__ntrip.active(nic, status)

# ---------------------------------------------------------------
# RTCM message received callback
# ---------------------------------------------------------------
def OnRtcmMsg(message):
    agOpen.correct(message)

# -----------------------------------------------------------
# Network link status callback
# -----------------------------------------------------------
def OnLinkStatus(link):
    if link:
        print('Link Up')
    else:
        print('Link Down!')
        agOpen.active(True)

# Enable the automatic garbage collection
gc.enable()

# ---------------------------------------------------------------
# AgOpenGps class
# ---------------------------------------------------------------
agOpen = AgOpenGps(on_rtcm_msg=OnRtcmMsg, on_link_stat=OnLinkStatus)

# ---------------------------------------------------------------
# Main process
# ---------------------------------------------------------------
async def main():
    await agOpen.start('eth')

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(main())
    except KeyboardInterrupt:
        del agOpen
        print('Interrupted')
