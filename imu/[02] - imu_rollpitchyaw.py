import math
import uasyncio
import sty

# ---------------------------------------------------------------
# Calculates roll, pitch, yaw angles from quaternions
# ---------------------------------------------------------------
def calcRollPitchYaw(q, dt):
    gx = 2 * (q[1]*q[3] - q[0]*q[2])
    gy = 2 * (q[0]*q[1] + q[2]*q[3])
    gz = q[0]*q[0] - q[1]*q[1] - q[2]*q[2] + q[3]*q[3]
    roll = math.atan(gy / math.sqrt(gx*gx + gz*gz)) * 57.29577951
    pitch = math.atan(gx / math.sqrt(gy*gy + gz*gz)) * 57.29577951
    print("DEL:%6.3f #RPY:%2.0f,%2.0f,%2.0f" % (dt, roll, pitch, 0))

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
        # Read the unfiltered values
        # ax, ay, az, gx, gy, gz, dt
        vals = imu.read()
        # Update the AHRS filter
        calcRollPitchYaw(ahrs.update(vals), vals[sty.Imu.DT])

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
