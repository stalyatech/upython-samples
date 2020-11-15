from sty import Pin, ExtInt

# External interrupt callback
def OnExtInt(line):
    print('line=', line)

# Configure the external interrupt
extint = ExtInt(Pin('DIN1'), ExtInt.IRQ_FALLING, Pin.PULL_NONE, OnExtInt)
