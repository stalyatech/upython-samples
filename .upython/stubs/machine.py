"""
Module: 'machine' on pySBC 1.13.0 with FW1.0-171
"""
# MCU: (sysname='pySBC', nodename='pySBC', release='1.13.0 with FW1.0', version='v1.13-171-g7720a5aa6-dirty on 2020-10-20', machine='simpleRTK-SBC with STM32F745')
# Stubber: 1.3.4

class ADC:
    ''
    CORE_TEMP = 268435474
    CORE_VBAT = 18
    CORE_VREF = 17
    VREF = 65535
    def read_u16():
        pass

DEEPSLEEP_RESET = 4
HARD_RESET = 2

class I2C:
    ''
    def init():
        pass

    def readfrom():
        pass

    def readfrom_into():
        pass

    def readfrom_mem():
        pass

    def readfrom_mem_into():
        pass

    def readinto():
        pass

    def scan():
        pass

    def start():
        pass

    def stop():
        pass

    def write():
        pass

    def writeto():
        pass

    def writeto_mem():
        pass

    def writevto():
        pass

PWRON_RESET = 1

class Pin:
    ''
    AF1_TIM1 = 1
    AF1_TIM2 = 1
    AF2_TIM3 = 2
    AF2_TIM4 = 2
    AF2_TIM5 = 2
    AF3_TIM10 = 3
    AF3_TIM11 = 3
    AF3_TIM8 = 3
    AF3_TIM9 = 3
    AF4_I2C3 = 4
    AF7_USART1 = 7
    AF7_USART2 = 7
    AF7_USART3 = 7
    AF8_UART4 = 8
    AF8_UART7 = 8
    AF8_UART8 = 8
    AF8_USART6 = 8
    AF9_CAN1 = 9
    AF9_TIM12 = 9
    AF9_TIM13 = 9
    AF9_TIM14 = 9
    AF_OD = 18
    AF_PP = 2
    ALT = 2
    ALT_OPEN_DRAIN = 18
    ANALOG = 3
    IN = 0
    IRQ_FALLING = 270598144
    IRQ_RISING = 269549568
    OPEN_DRAIN = 17
    OUT = 1
    OUT_OD = 17
    OUT_PP = 1
    PULL_DOWN = 2
    PULL_NONE = 0
    PULL_UP = 1
    def af():
        pass

    def af_list():
        pass

    board = None
    cpu = None
    def debug():
        pass

    def dict():
        pass

    def gpio():
        pass

    def high():
        pass

    def init():
        pass

    def irq():
        pass

    def low():
        pass

    def mapper():
        pass

    def mode():
        pass

    def name():
        pass

    def names():
        pass

    def off():
        pass

    def on():
        pass

    def pin():
        pass

    def port():
        pass

    def pull():
        pass

    def value():
        pass


class RTC:
    ''
    def calibration():
        pass

    def datetime():
        pass

    def info():
        pass

    def init():
        pass

    def wakeup():
        pass

SOFT_RESET = 0

class SPI:
    ''
    LSB = 128
    MSB = 0
    def deinit():
        pass

    def init():
        pass

    def read():
        pass

    def readinto():
        pass

    def write():
        pass

    def write_readinto():
        pass


class Signal:
    ''
    def off():
        pass

    def on():
        pass

    def value():
        pass


class SoftI2C:
    ''
    def init():
        pass

    def readfrom():
        pass

    def readfrom_into():
        pass

    def readfrom_mem():
        pass

    def readfrom_mem_into():
        pass

    def readinto():
        pass

    def scan():
        pass

    def start():
        pass

    def stop():
        pass

    def write():
        pass

    def writeto():
        pass

    def writeto_mem():
        pass

    def writevto():
        pass


class SoftSPI:
    ''
    LSB = 128
    MSB = 0
    def deinit():
        pass

    def init():
        pass

    def read():
        pass

    def readinto():
        pass

    def write():
        pass

    def write_readinto():
        pass


class Timer:
    ''
    ONE_SHOT = 1
    PERIODIC = 2
    def deinit():
        pass

    def init():
        pass


class UART:
    ''
    CTS = 512
    IRQ_RXIDLE = 16
    ParserNMEA = 1
    ParserNONE = 0
    ParserRTCM = 3
    ParserUBX = 2
    RTS = 256
    def any():
        pass

    def callback():
        pass

    def connect():
        pass

    def deinit():
        pass

    def init():
        pass

    def irq():
        pass

    def istxbusy():
        pass

    def parse_nmea():
        pass

    def parse_ubx():
        pass

    def parser():
        pass

    def process():
        pass

    def read():
        pass

    def readchar():
        pass

    def readinto():
        pass

    def readline():
        pass

    def send():
        pass

    def sendbreak():
        pass

    def write():
        pass

    def writechar():
        pass


class WDT:
    ''
    def feed():
        pass

WDT_RESET = 3
def bootloader():
    pass

def deepsleep():
    pass

def disable_irq():
    pass

def enable_irq():
    pass

def freq():
    pass

def idle():
    pass

def info():
    pass

def lightsleep():
    pass

mem16 = None
mem32 = None
mem8 = None
def reset():
    pass

def reset_cause():
    pass

def rng():
    pass

def sleep():
    pass

def soft_reset():
    pass

def time_pulse_us():
    pass

def unique_id():
    pass

