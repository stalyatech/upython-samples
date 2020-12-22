import uasyncio
import network
from sty import Pin
from sty import UART

# ---------------------------------------------------------------
# SMS received callback
# ---------------------------------------------------------------
def OnSmsReceived(smsMsg):
    print(smsMsg)

# ---------------------------------------------------------------
# GSM Module Communication based socket interface (on XBEE-HP)
# ---------------------------------------------------------------

# Configure the network interface card (GSM)
pwr = Pin('PWR_XBEE', Pin.OUT_OD)
nic = network.GSM(UART('XBEE_HP', 115200, rxbuf=1024, dma=False), pwr_pin=pwr, info=True)
sms = nic.SMS(OnSmsReceived)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():

    # Print info
    print('\r\nWaiting for link-up')

    # Configure the GSM parameters
    nic.config(user='gprs', pwd='gprs', apn='internet', pin='1234')

    # Connect to the gsm network
    nic.connect()

    # Wait for connection
    while not nic.isconnected():
        await uasyncio.sleep_ms(100)

    # Status info
    ipaddr = nic.ifconfig('ipaddr')
    print('GSM connection done: %s' % ipaddr)

    # GSM info
    print('IMEI Number: %s' % nic.imei())
    print('IMSI Number: %s' % nic.imsi())
    qos = nic.qos()
    print('Signal Quality: %d,%d' % (qos[0], qos[1]))

    # Wait till SMS idle
    while sms.isbusy():
        await uasyncio.sleep_ms(100)

    # SMS send
    sms.send('05335115360', 'Message from stalya.com')

    # Wait till SMS send
    while sms.isbusy():
        await uasyncio.sleep_ms(100)

    # Status info
    if sms.iserror():
        print('SMS send error!\r\n')
    else:
        print('SMS has been sent\r\n')
    print('Now we are waiting for any message...\r\n')

    # Sleep for a while
    await uasyncio.sleep(600)

    # Disconnect from the gsm network
    nic.disconnect()
    print('This is simple SMS application based on GSM NIC with CMUX support\r\n')

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
        nic.disconnect()
