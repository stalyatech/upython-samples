from sty import Pin, ExtInt

# External interrupt callback
def OnExtInt(line):
    print('line=', line)

# Configure the external interrupt
extint = ExtInt(Pin('IP0'), ExtInt.IRQ_RISING, Pin.PULL_NONE, OnExtInt)
