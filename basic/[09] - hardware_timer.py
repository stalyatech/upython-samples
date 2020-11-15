import math
import sty
import micropython
micropython.alloc_emergency_exception_buf(100)

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# Something calculation functions
# ---------------------------------------------------------------
def CalculateSomething1(timer):
    led1.toggle()
    print(math.fmod(1, 5))

def CalculateSomething2(timer):
    led2.toggle()
    print(math.fmod(2, 5))

def CalculateSomething3(timer):
    led3.toggle()
    print(math.fmod(3, 5))

# ---------------------------------------------------------------
# Create the timer
# ---------------------------------------------------------------

# Timer #1 trigger callback
def OnTimer1(timer):
    micropython.schedule(CalculateSomething1, timer)

# Timer #2 trigger callback
def OnTimer2(timer):
    micropython.schedule(CalculateSomething2, timer)

# Timer #3 trigger callback
def OnTimer3(timer):
    micropython.schedule(CalculateSomething3, timer)

# Create a timer objects
tim1 = sty.Timer(1, freq=1)
tim2 = sty.Timer(2, freq=10)
tim3 = sty.Timer(4, freq=20)

# Configure the callbacks
tim1.callback(OnTimer1)
tim2.callback(OnTimer2)
tim3.callback(OnTimer3)
