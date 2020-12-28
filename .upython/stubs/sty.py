"""
Module: 'sty' on none
"""
# MCU: {'ver': '1.13.0 with FW2.0.3-388', 'port': 'pySBC', 'arch': 'armv7emdp', 'sysname': 'pySBC', 'release': '1.13.0 with FW2.0.3', 'name': 'micropython', 'mpy': 8709, 'version': '1.13.0', 'machine': 'simpleRTK-SBC-R02 with STM32H743', 'build': '388', 'nodename': 'pySBC', 'platform': 'pySBC', 'family': 'micropython'}
# Stubber: 1.3.9

class ADC:
    ''
    def read():
        pass

    def read_timed():
        pass

    def read_timed_multi():
        pass


class ADCAll:
    ''
    def read_channel():
        pass

    def read_core_temp():
        pass

    def read_core_vbat():
        pass

    def read_core_vref():
        pass

    def read_vref():
        pass


class CAN:
    ''
    BUS_OFF = 4
    DUAL = 1
    ERROR_ACTIVE = 1
    ERROR_PASSIVE = 3
    ERROR_WARNING = 2
    LOOPBACK = 4
    MASK = 2
    NORMAL = 0
    RANGE = 0
    SILENT = 2
    SILENT_LOOPBACK = 3
    STOPPED = 0
    def any():
        pass

    def clearfilter():
        pass

    def deinit():
        pass

    def info():
        pass

    def init():
        pass

    def initfilterbanks():
        pass

    def recv():
        pass

    def restart():
        pass

    def rxcallback():
        pass

    def send():
        pass

    def setfilter():
        pass

    def state():
        pass


class ExtInt:
    ''
    EVT_FALLING = 287440896
    EVT_RISING = 286392320
    EVT_RISING_FALLING = 288489472
    IRQ_FALLING = 287375360
    IRQ_RISING = 286326784
    IRQ_RISING_FALLING = 288423936
    def disable():
        pass

    def enable():
        pass

    def line():
        pass

    def regs():
        pass

    def swint():
        pass


class Flash:
    ''
    def ioctl():
        pass

    def readblocks():
        pass

    def writeblocks():
        pass


class Hub:
    ''
    USB_HUB_F9H1_PORT = 2
    USB_HUB_F9H2_PORT = 6
    USB_HUB_F9P_PORT = 1
    USB_HUB_GSM_PORT = 4
    USB_HUB_XBEE_PORT = 5
    def portconfig():
        pass


class I2C:
    ''
    MASTER = 0
    SLAVE = 1
    def deinit():
        pass

    def init():
        pass

    def is_ready():
        pass

    def mem_read():
        pass

    def mem_write():
        pass

    def recv():
        pass

    def scan():
        pass

    def send():
        pass

class Imu:
    ''
    ACCEL_X = 0
    ACCEL_Y = 1
    ACCEL_Z = 2
    GYRO_X = 3
    GYRO_Y = 4
    GYRO_Z = 5
    DT = 6

    class Madgwick:
        ''
        def update(self, data):
            pass

    class Mahony:
        ''
        def update(self, data):
            pass

    class DCM:
        ''
        def update(self, data, yaw):
            pass

    def ax():
        pass

    def ay():
        pass

    def az():
        pass

    def gx():
        pass

    def gy():
        pass

    def gz():
        pass

    def read():
        pass

    def read_accel():
        pass

    def read_gyro():
        pass

    def ready():
        pass

    def stat():
        pass

    def temp():
        pass

    def write_accel():
        pass

    def write_gyro():
        pass

    def wx():
        pass

    def wy():
        pass

    def wz():
        pass


class LED:
    ''
    def intensity():
        pass

    def off():
        pass

    def on():
        pass

    def toggle():
        pass


class Parser:
    ''
    NMEA = 1
    NONE = 0
    RTCM = 3
    UBX = 2
    def config():
        pass

    def decode():
        pass

    def deinit():
        pass

    def init():
        pass

    def popleft():
        pass

    def process():
        pass


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


class Queue:
    ''
    def append():
        pass

    def deinit():
        pass

    def popleft():
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

SD = None

class SDCard:
    ''
    def info():
        pass

    def ioctl():
        pass

    def power():
        pass

    def present():
        pass

    def read():
        pass

    def readblocks():
        pass

    def write():
        pass

    def writeblocks():
        pass


class SPI:
    ''
    LSB = 8388608
    MASTER = 4194304
    MSB = 0
    SLAVE = 0
    def deinit():
        pass

    def init():
        pass

    def read():
        pass

    def readinto():
        pass

    def recv():
        pass

    def send():
        pass

    def send_recv():
        pass

    def write():
        pass

    def write_readinto():
        pass


class Timer:
    ''
    BOTH = 10
    BRK_HIGH = 2
    BRK_LOW = 1
    BRK_OFF = 0
    CENTER = 32
    DOWN = 16
    ENC_A = 9
    ENC_AB = 11
    ENC_B = 10
    FALLING = 2
    HIGH = 0
    IC = 8
    LOW = 2
    OC_ACTIVE = 3
    OC_FORCED_ACTIVE = 6
    OC_FORCED_INACTIVE = 7
    OC_INACTIVE = 4
    OC_TIMING = 2
    OC_TOGGLE = 5
    PWM = 0
    PWM_INVERTED = 1
    RISING = 0
    UP = 0
    def callback():
        pass

    def channel():
        pass

    def counter():
        pass

    def deinit():
        pass

    def freq():
        pass

    def init():
        pass

    def period():
        pass

    def prescaler():
        pass

    def source_freq():
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


class USB_HID:
    ''
    def recv():
        pass

    def send():
        pass


class USB_VCP:
    ''
    CTS = 2
    RTS = 1
    def any():
        pass

    def close():
        pass

    def init():
        pass

    def isconnected():
        pass

    def read():
        pass

    def readinto():
        pass

    def readline():
        pass

    def readlines():
        pass

    def recv():
        pass

    def send():
        pass

    def setinterrupt():
        pass

    def write():
        pass

def bootloader():
    pass

def country():
    pass

def delay():
    pass

def dht_readinto():
    pass

def disable_irq():
    pass

def elapsed_micros():
    pass

def elapsed_millis():
    pass

def enable_irq():
    pass

def fault_debug():
    pass

def freq():
    pass

def hard_reset():
    pass

def have_cdc():
    pass

def hid():
    pass

hid_keyboard = None
hid_mouse = None
def info():
    pass

def main():
    pass

def micros():
    pass

def millis():
    pass

def mount():
    pass

def repl_info():
    pass

def repl_uart():
    pass

def rng():
    pass

def standby():
    pass

def stop():
    pass

def sync():
    pass

def udelay():
    pass

def unique_id():
    pass

def usb_mode():
    pass

def wfi():
    pass

