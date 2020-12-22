import uasyncio
import sty

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
async def app_proc():
    while True:

        # Wait for sensor ready
        while not imu.ready():
            pass

        # Read all values
        try:
            printValues(imu.read(), imu.temp())
        except RuntimeError as e:
            print(e)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
