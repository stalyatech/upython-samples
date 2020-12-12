import utime
import usocket
import network
import _thread

# ---------------------------------------------------------------
# Ethernet based socket interface
# ---------------------------------------------------------------

# Configure the network interface card (Ethernet)
nic = network.LAN()

# ---------------------------------------------------------------
# Main application process
# ---------------------------------------------------------------
def app_proc():

    # Start up delay to allow REPL message
    utime.sleep_ms(1000)

    # Print info
    print('\r\nWaiting for link-up')

    # Activate the interface
    nic.active(True)

    # Wait for ethernet link up
    while nic.status() == 0:
        utime.sleep(1)

    # Print info
    print('DHCP started')

    # Configure the DHCP client
    nic.ifconfig(mode='dhcp')

    # Status info
    ipaddr = nic.ifconfig('ipaddr')
    print('DHCP done: %s\r\n' % ipaddr)

    # Get the IP address of host
    addr = usocket.getaddrinfo('google.com', 80)[0][-1]
    print('Host: %s:%d' % (addr[0], addr[1]))

    # Create the socket
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)

    # Connect to the host
    sock.connect(addr)
    print('Socket connected')

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
    print('\r\nSocket closed')

    # Deactivate the interface
    nic.active(False)

    # Info
    print('\r\nThis is simple socket application based on Ethernet NIC')

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
