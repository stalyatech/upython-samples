import os
import uasyncio

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    try:
        print(os.listdir())
        print(os.listdir('sub_directory'))
    except Exception as e:
        print(e)

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
