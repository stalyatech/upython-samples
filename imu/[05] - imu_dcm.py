import sty
import _thread

# ---------------------------------------------------------------
# Prints roll, pitch, yaw
# ---------------------------------------------------------------
def printRollPitchYaw(rpy, dt):
    roll = rpy[0] * 57.29577951
    pitch = rpy[1] * 57.29577951
    yaw = rpy[2] * 57.29577951
    print("DEL:%6.3f #RPY:%2.0f,%2.0f,%2.0f" % (dt, roll, pitch, yaw))

# ---------------------------------------------------------------
# IMU sensor
# ---------------------------------------------------------------

# Create the IMU sensor class
# it takes some times to configure it
imu = sty.Imu()
print('IMU sensor configured')

# Create the filter class
ahrs = imu.DCM(yawfix=True, kp_rollpitch=0.2, ki_rollpitch=0.00005, kp_yaw=1.2, ki_yaw=0.00005)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    while True:
        # Read the unfiltered values
        # ax, ay, az, gx, gy, gz, dt
        vals = imu.read()
        # Update the filtered values (DCM algorithm)
        printRollPitchYaw(ahrs.update(vals, 0), vals[sty.Imu.DT])

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
