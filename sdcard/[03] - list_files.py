import os
import _thread

# ---------------------------------------------------------------
# Main application process
# ---------------------------------------------------------------
def app_proc():
    print(os.listdir())
    print(os.listdir('sub_directory'))

# Start the application process
if __name__ == "__main__":
    _thread.start_new_thread(app_proc, ())
