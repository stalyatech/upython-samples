import usocket
import uasyncio
import network

# ---------------------------------------------------------------
# Ethernet based socket interface
# ---------------------------------------------------------------

# Configure the network interface card (Ethernet)
nic = network.LAN()

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():

    # Print info
    print('\r\nWaiting for link-up')

    # Activate the interface
    nic.active(True)

    # Wait for ethernet link up
    while nic.status() == 0:
        await uasyncio.sleep(1)

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
    print('\r\nSocket closed')

    # Deactivate the interface
    nic.active(False)

    # Info
    print('\r\nThis is simple socket application based on Ethernet NIC')

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
