import _thread

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    # Open the test file
    with open('nmea_log.txt', 'r') as fp:
        # Read the first line of file
        line = fp.readline()
        # Read the file line by line
        while line:
            print(line)
            line = fp.readline()
        # Close the test file
        fp.close()
    print('End of file')

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
