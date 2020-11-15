from sty import Pin
import utime

# ---------------------------------------------------------------
# Digital Inputs
# ---------------------------------------------------------------
IP1 = Pin('DIN1')
IP2 = Pin('DIN2')
IP3 = Pin('DIN3')
IP1.init(Pin.IN, Pin.PULL_NONE)
IP2.init(Pin.IN, Pin.PULL_NONE)
IP3.init(Pin.IN, Pin.PULL_NONE)

# ---------------------------------------------------------------
# Digital Outputs
# ---------------------------------------------------------------
QP1 = Pin('QP1', Pin.OUT_PP)
QP2 = Pin('QP2', Pin.OUT_PP)
QP3 = Pin('QP3', Pin.OUT_PP)
QP4 = Pin('QP4', Pin.OUT_PP)
QP5 = Pin('QP5', Pin.OUT_PP)
QP6 = Pin('QP6', Pin.OUT_PP)

# ---------------------------------------------------------------
# Toogle the outputs
# ---------------------------------------------------------------
print('Outputs are toggling...')
stat = 0
for i in range(10):
    if stat == 1:
        QP1.high()
        QP2.high()
        QP3.high()
        QP4.high()
        QP5.high()
        QP6.high()
        stat = 0
    else:
        QP1.low()
        QP2.low()
        QP3.low()
        QP4.low()
        QP5.low()
        QP6.low()
        stat = 1
    utime.sleep_ms(500)

# ---------------------------------------------------------------
# Read the inputs
# ---------------------------------------------------------------
print('Read the inputs...')
for i in range(10):
    print(IP1.value(), IP2.value(), IP3.value())
    utime.sleep_ms(200)
