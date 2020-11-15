import utime
import sty

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# Blink LEDs with different frequency
# ---------------------------------------------------------------
print('LED1 is blinking...')
for i in range(10):
    led1.toggle()
    utime.sleep_ms(100)

print('LED2 is blinking...')
for i in range(10):
    led2.toggle()
    utime.sleep_ms(200)

print('LED3 is blinking...')
for i in range(10):
    led3.toggle()
    utime.sleep_ms(500)

# Console info
print('Did you see them :)')
