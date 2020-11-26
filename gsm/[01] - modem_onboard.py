import utime
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
