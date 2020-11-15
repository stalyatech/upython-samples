import utime
import network
import _thread
from sty import Pin
from sty import UART

# SMS received callback
def OnSmsReceived(smsMsg):
    print(smsMsg)

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
sms = nic.SMS(OnSmsReceived)

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

    # Wait till SMS idle
    while sms.isbusy():
        utime.sleep_ms(10)

    # SMS send
    sms.send('05551234567', 'Message from ardusimple.com')

    # Wait till SMS send
    while sms.isbusy():
        utime.sleep_ms(10)

    # Status info
    if sms.iserror():
        print('SMS send error!\r\n')
    else:
        print('SMS has been sent\r\n')
    print('Now we are waiting for any message...\r\n')

    # Sleep for a while
    utime.sleep(600)

    # Disconnect from the gsm network
    nic.disconnect()

    print('This is simple SMS application based on GSM NIC with CMUX support\r\n')

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
