import utime
import usocket
import network
import _thread
from sty import Pin
from sty import UART

# ---------------------------------------------------------------
# Power-on the XBEE subsystem
# ---------------------------------------------------------------

# XBEE Low Power Socket
xbee_lp_pwr = Pin('PWR_XBEE_LP', Pin.OUT_OD)
xbee_lp_pwr.high()

# XBEE Low Power Direction (XBEE_LP <-> MCU)
xbee_lp_dir = Pin('XBEE_LP_DIR', Pin.OUT_PP)
xbee_lp_dir.high()

# XBEE High Power Direction (XBEE_HP <-> MCU)
xbee_hp_dir = Pin('XBEE_HP_DIR', Pin.OUT_PP)
xbee_hp_dir.high()

# ---------------------------------------------------------------
# GSM Module Communication based socket interface (on XBEE-HP)
# ---------------------------------------------------------------

# Configure the network interface card (GSM)
pwr = Pin('PWR_XBEE_HP', Pin.OUT_OD)
nic = network.GSM(UART('XBEE_HP', 115200, rxbuf=1024, dma=False), pwr_pin=pwr, info=True)

# ---------------------------------------------------------------
# GSM connection status callback
# ---------------------------------------------------------------
def OnGsmStatus(status):
    print('Link : {}\r\nQoS  : {}\r\nBER  : {}'.format(status[0], status[1], status[2]))

# ---------------------------------------------------------------
# Main application process
# ---------------------------------------------------------------
def app_proc():

    # Start up delay to allow REPL message
    utime.sleep_ms(1000)

    # Print info
    print('GSM connection started...\r\n')

    # Configure the GSM parameters
    nic.config(user='gprs', pwd='gprs', apn='internet', pin='1234')

    # Connect to the gsm network
    nic.connect(OnGsmStatus)

    # Wait till connection
    while not nic.isconnected():
        utime.sleep_ms(10)

    # Status info
    ifconfig = nic.ifconfig()
    print('GSM connection done: %s' % ifconfig[0])

    # GSM info
    print('IMEI Number: %s' % nic.imei())
    print('IMSI Number: %s' % nic.imsi())
    qos = nic.qos()
    print('Signal Quality: %d,%d' % (qos[0],qos[1]))

    # Get the IP address of host
    addr = usocket.getaddrinfo('ardusimple.com', 80)[0][-1]
    print('Host: %s:%d' % (addr[0], addr[1]))

    # Create the socket
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)

    # Connect to the host
    sock.connect(addr)
    print('Socket connected\r\n')

    # Send data to the host
    sock.send(b'GET / HTTP/1.1\r\nHost: ardusimple.com\r\n\r\n')
    print('Packet sent\r\n')

    # Get data from the host
    sock.settimeout(10.0)
    try:
        data = sock.recv(1000)
        print(data)
    except Exception as e:
        print(e)

    # Close the socket
    sock.close()
    print('Socket closed\r\n')

    # Disconnect from the gsm network
    nic.disconnect()

    print('This is simple socket application based on GSM NIC with CMUX support\r\n')

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
