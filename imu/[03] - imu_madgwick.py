import sty
import _thread

# ---------------------------------------------------------------
# Prints quaternions
# ---------------------------------------------------------------
def printQuaternions(q):
    print(q[0], q[1], q[2], q[3])

# ---------------------------------------------------------------
# IMU sensor
# ---------------------------------------------------------------

# Create the IMU sensor class
# it takes some times to configure it
imu = sty.Imu()
print('IMU sensor configured')

# Create the filter class
ahrs = imu.Madgwick(beta=0.2)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        # Update the filtered values (Madgwick algorithm)
        printQuaternions(ahrs.update(imu.read()))

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
