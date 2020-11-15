import sty
import _thread
from sty import Pin

# ---------------------------------------------------------------
# On-Board LEDs
# ---------------------------------------------------------------

led1 = sty.LED(1)
led2 = sty.LED(2)
led3 = sty.LED(3)

# ---------------------------------------------------------------
# Digital Input for F9P Time Pulse
# ---------------------------------------------------------------
fp9_puls = Pin('F9P_PULS')

# ---------------------------------------------------------------
# Digital Output to reflect the F9P Time Pulse
# ---------------------------------------------------------------
QP1 = Pin('QP1', Pin.OUT_PP)

# ---------------------------------------------------------------
# Timer callback to redirect the time pulse
# ---------------------------------------------------------------
def OnTimer(timer):
    QP1.value(fp9_puls.value())
    led3.toggle()

# ---------------------------------------------------------------
# Create the timer
# ---------------------------------------------------------------

# Create a timer objects
tim1 = sty.Timer(1, freq=10)

# Configure the callbacks
tim1.callback(OnTimer)

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_PP)
gnss_pwr.high()

# Main application process
def app_proc():
    while True:
        pass

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
