"""
Module: 'machine' on pySBC 1.13.0 with FW2.0.1-363
"""
# MCU: (sysname='pySBC', nodename='pySBC', release='1.13.0 with FW2.0.1', version='v1.13-363-g1fdf4f6ee-dirty on 2020-12-16', machine='simpleRTK-SBC-R02 with STM32H743')
# Stubber: 1.3.4

class ADC:
    ''
    CORE_TEMP = -880541696
    CORE_VBAT = -950927360
    CORE_VREF = -810024960
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

POWER_GNSS = 0
POWER_GSM = 4
POWER_HUB = 5
POWER_XBEE = 1
PWRON_RESET = 1

class Pin:
    ''
    AF11_UART7 = 11
    AF1_TIM1 = 1
    AF1_TIM16 = 1
    AF1_TIM17 = 1
    AF1_TIM2 = 1
    AF2_TIM12 = 2
    AF2_TIM3 = 2
    AF2_TIM4 = 2
    AF2_TIM5 = 2
    AF3_TIM8 = 3
    AF4_I2C3 = 4
    AF4_TIM15 = 4
    AF4_USART1 = 4
    AF6_UART4 = 6
    AF7_UART7 = 7
    AF7_USART1 = 7
    AF7_USART2 = 7
    AF7_USART3 = 7
    AF7_USART6 = 7
    AF8_UART4 = 8
    AF8_UART8 = 8
    AF9_CAN1 = 9
    AF9_TIM13 = 9
    AF9_TIM14 = 9
    AF_OD = 18
    AF_PP = 2
    ALT = 2
    ALT_OPEN_DRAIN = 18
    ANALOG = 3
    IN = 0
    IRQ_FALLING = 287375360
    IRQ_RISING = 286326784
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


class Power:
    ''
    def off():
        pass

    def on():
        pass

    def stat():
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
    LSB = 8388608
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
    LSB = 8388608
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
    RTS = 256
    def any():
        pass

    def callback():
        pass

    def connect():
        pass

    def decode():
        pass

    def deinit():
        pass

    def init():
        pass

    def irq():
        pass

    def istxbusy():
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

