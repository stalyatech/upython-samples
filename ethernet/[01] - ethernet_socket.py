import utime
import usocket
import network
import _thread

# ---------------------------------------------------------------
# Link status change callback
# ---------------------------------------------------------------
def LinkStatusCB(link):
    if link:
        print('Link is up')
    else:
        print('Link is down')

# ---------------------------------------------------------------
# Ethernet based socket interface
# ---------------------------------------------------------------

# Configure the network interface card (Ethernet)
nic = network.LAN(LinkStatusCB)

# ---------------------------------------------------------------
# Main application process
# ---------------------------------------------------------------
def app_proc():

    # Start up delay to allow REPL message
    utime.sleep_ms(1000)

    # Activate the interface
    nic.active(True)

    # Wait for ethernet link up
    while nic.status() == 0:
        utime.sleep_ms(100)

    # DHCP config
    nic.ifconfig(mode='dhcp')
    ipaddr = nic.ifconfig('ipaddr')
    print('DHCP done: %s' % ipaddr)

    # Get the IP address of host
    addr = usocket.getaddrinfo('google.com', 80)[0][-1]
    print('Host: %s:%d' % (addr[0], addr[1]))

    # Create the socket
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)

    # Connect to the host
    sock.connect(addr)
    print('Socket connected\r\n')

    # Send data to the host
    sock.send(b'GET / HTTP/1.0\r\n\r\n')
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

    # Info
    print('This is simple socket application based on Ethernet NIC\r\n')

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
