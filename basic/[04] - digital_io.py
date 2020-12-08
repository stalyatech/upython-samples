import utime
from sty import Pin

# ---------------------------------------------------------------
# Digital Inputs
# ---------------------------------------------------------------
IP0 = Pin('IP0', Pin.IN, Pin.PULL_NONE)
IP1 = Pin('IP1', Pin.IN, Pin.PULL_NONE)
IP2 = Pin('IP2', Pin.IN, Pin.PULL_NONE)
IP3 = Pin('IP3', Pin.IN, Pin.PULL_NONE)
IP4 = Pin('IP4', Pin.IN, Pin.PULL_NONE)
IP5 = Pin('IP5', Pin.IN, Pin.PULL_NONE)
IP6 = Pin('IP6', Pin.IN, Pin.PULL_NONE)
IP7 = Pin('IP7', Pin.IN, Pin.PULL_NONE)
IP8 = Pin('IP8', Pin.IN, Pin.PULL_NONE)

# ---------------------------------------------------------------
# Digital Outputs
# ---------------------------------------------------------------
QP0 = Pin('QP0', Pin.OUT_PP)
QP1 = Pin('QP1', Pin.OUT_PP)
QP2 = Pin('QP2', Pin.OUT_PP)
QP3 = Pin('QP3', Pin.OUT_PP)
QP4 = Pin('QP4', Pin.OUT_PP)
QP5 = Pin('QP5', Pin.OUT_PP)

# ---------------------------------------------------------------
# Toogle the outputs
# ---------------------------------------------------------------
print('Outputs are toggling...')
stat = 0
for i in range(10):
    if stat == 1:
        QP0.high()
        QP1.high()
        QP2.high()
        QP3.high()
        QP4.high()
        QP5.high()
        stat = 0
    else:
        QP0.low()
        QP1.low()
        QP2.low()
        QP3.low()
        QP4.low()
        QP5.low()
        stat = 1
    utime.sleep_ms(500)

# ---------------------------------------------------------------
# Read the inputs
# ---------------------------------------------------------------
print('Read the inputs...')
for i in range(20):
    print(IP0.value(), IP1.value(), IP2.value(), IP3.value(), IP4.value(), IP5.value(), IP6.value(), IP7.value(), IP8.value())
    utime.sleep_ms(200)
