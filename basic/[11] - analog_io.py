import array
import uasyncio
import sty

# ---------------------------------------------------------------
# Analog Inputs
# ---------------------------------------------------------------
adc0 = sty.ADC(sty.Pin.board.VAIN1)
adc1 = sty.ADC(sty.Pin.board.VAIN2)

# Create timer
tim = sty.Timer(8, freq=100)

# ADC buffers of 100 words
rx0 = array.array('H', (0 for i in range(100)))
rx1 = array.array('H', (0 for i in range(100)))

# ---------------------------------------------------------------
# Application process
# ---------------------------------------------------------------
async def app_proc():
    while True:
        # read analog values into buffers at 100Hz (takes one second)
        sty.ADC.read_timed_multi((adc0, adc1), (rx0, rx1), tim)
        for n in range(len(rx0)):
            print(rx0[n], rx1[n])

# ---------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        uasyncio.run(app_proc())
    except KeyboardInterrupt:
        print('Interrupted')
