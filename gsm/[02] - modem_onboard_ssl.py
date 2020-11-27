import utime
import ussl
import usocket
import network
import _thread
from sty import Pin
from sty import UART

# ---------------------------------------------------------------
# GSM Module Communication based socket interface
# ---------------------------------------------------------------

# Configure the network interface card (GSM)
pwr = Pin('PWR_GSM', Pin.OUT_OD)
mon = Pin('GSM_MON', Pin.IN, Pin.PULL_DOWN)
nic = network.GSM(UART('GSM', 115200, flow=UART.RTS|UART.CTS, rxbuf=1024, dma=False), pwr_pin=pwr, mon_pin=mon, info=True)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():

    # Start up delay to allow REPL message
    utime.sleep_ms(1000)

    # Print info
    print('GSM connection started...\r\n')

    # Configure the GSM parameters
    nic.config(user='gprs', pwd='gprs', apn='internet', pin='1234')

    # Connect to the gsm network
    nic.connect()

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
    print('Signal Quality: %d,%d' % (qos[0], qos[1]))

    # Get the IP address of host
    addr = usocket.getaddrinfo('google.com', 443)[0][-1]
    print('Host: %s:%d' % (addr[0], addr[1]))

    # Create the socket
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)

    # Connect to the host
    sock.connect(addr)
    print('Socket connected\r\n')

    # Wrap the socket with SSL
    sock = ussl.wrap_socket(sock)
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

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())