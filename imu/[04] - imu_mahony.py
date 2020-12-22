import uasyncio
import sty

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
ahrs = imu.Mahony(kp=1.5, ki=0.01)

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # Wait for sensor ready
        while not imu.ready():
            pass
        # Update the filtered values (Mahony algorithm)
        printQuaternions(ahrs.update(imu.read()))

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
