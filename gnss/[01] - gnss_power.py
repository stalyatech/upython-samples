from sty import Pin
import _thread

# ---------------------------------------------------------------
# GNSS Modules
# ---------------------------------------------------------------

# Power-on the GNSS subsystem
gnss_pwr = Pin('PWR_GNSS', Pin.OUT_OD)
gnss_pwr.high()

# Main application process
def app_proc():
    while True:
        pass

if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
