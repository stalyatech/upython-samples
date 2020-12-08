from sty import Pin, Timer

# ---------------------------------------------------------------
# Digital Outputs
# ---------------------------------------------------------------

# QP1 has TIM4 CH1
PWM1 = Pin('QP0')
# QP1 has TIM4 CH2
PWM2 = Pin('QP1')
# QP1 has TIM4 CH3
PWM3 = Pin('QP2')

# PWM Timer
tim = Timer(4, freq=1000)

# PWM Channels
ch1 = tim.channel(1, Timer.PWM, pin=PWM1)
ch2 = tim.channel(2, Timer.PWM, pin=PWM2)
ch3 = tim.channel(3, Timer.PWM, pin=PWM3)
ch4 = tim.channel(4, Timer.PWM, pin=PWM4)

# PWM Duty cycles
ch1.pulse_width_percent(25)
ch2.pulse_width_percent(50)
ch3.pulse_width_percent(75)
ch4.pulse_width_percent(100)
