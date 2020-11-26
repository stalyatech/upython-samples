import sty
import _thread

# ---------------------------------------------------------------
# Prints all values
# ---------------------------------------------------------------
def printValues(vals, temp):
    print("BDY: [%6.2f  %6.2f  %6.2f]  [%6.2f  %6.2f  %6.2f]  [%5.3f]" % (vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], temp))

# ---------------------------------------------------------------
# IMU sensor
# ---------------------------------------------------------------

# Create the IMU sensor class
# it takes some times to configure it
imu = sty.Imu()
print('IMU sensor configured')

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        printValues(imu.read(), imu.temp())

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
