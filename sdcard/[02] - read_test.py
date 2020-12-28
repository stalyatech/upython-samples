import uasyncio

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    # Open the test file
    with open('nmea_log.txt', 'r') as fp:
        # Read the first line of file
        line = fp.readline()
        # Read the file line by line
        while line:
            print(line[:-2])
            line = fp.readline()
    print('End of file')

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
