import time
import ssl
import socket
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
# Main application process
# ---------------------------------------------------------------
def app_proc():

    # Start up delay to allow REPL message
    time.sleep_ms(1000)

    # Print info
    print('GSM connection started...\r\n')

    # Configure the GSM parameters
    nic.config(user='gprs', pwd='gprs', apn='internet', pin='1234')

    # Connect to the gsm network
    nic.connect()

    # Wait till connection
    while not nic.isconnected():
        time.sleep_ms(10)

    # Status info
    ifconfig = nic.ifconfig()
    print('GSM connection done: %s' % ifconfig[0])

    # GSM info
    print('IMEI Number: %s' % nic.imei())
    print('IMSI Number: %s' % nic.imsi())
    qos = nic.qos()
    print('Signal Quality: %d,%d' % (qos[0], qos[1]))

    # Get the IP address of host
    addr = socket.getaddrinfo('google.com', 443)[0][-1]
    print('Host: %s:%d' % (addr[0], addr[1]))

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the host
    sock.connect(addr)
    print('Socket connected\r\n')

    # Wrap the socket with SSL
    sock = ssl.wrap_socket(sock)
    print(sock)

    # Both CPython and MicroPython SSLSocket objects support read() and write() methods.

    # Send data to the host
    sock.write(b'GET / HTTP/1.0\r\n\r\n')
    print('Packet sent\r\n')

    # Get data from the host
    print(sock.read(1000))

    # Close the socket
    sock.close()
    print('Socket closed\r\n')

    # Disconnect from the gsm network
    nic.disconnect()

    print('This is simple SSL socket application based on GSM NIC with CMUX support\r\n')

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
