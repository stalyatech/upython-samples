import os
import _thread

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
def app_proc():
    print(os.listdir())
    print(os.listdir('sub_directory'))

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Start the application process
    _thread.start_new_thread(app_proc, ())
