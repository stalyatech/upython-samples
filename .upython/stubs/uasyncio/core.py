"""
Module: 'uasyncio.core' on pySBC 1.13.0 with FW1.5.7-225
"""
# MCU: (sysname='pySBC', nodename='pySBC', release='1.13.0 with FW1.5.7', version='v1.13-225-g7d9d01bd1-dirty on 2020-11-15', machine='simpleRTK-SBC with STM32F745')
# Stubber: 1.3.4

class CancelledError:
    ''

class IOQueue:
    ''
    def _dequeue():
        pass

    def _enqueue():
        pass

    def queue_read():
        pass

    def queue_write():
        pass

    def remove():
        pass

    def wait_io_event():
        pass


class Loop:
    ''
    _exc_handler = None
    def call_exception_handler():
        pass

    def close():
        pass

    def create_task():
        pass

    def default_exception_handler():
        pass

    def get_exception_handler():
        pass

    def run_forever():
        pass

    def run_until_complete():
        pass

    def set_exception_handler():
        pass

    def stop():
        pass


class SingletonGenerator:
    ''

class Task:
    ''

class TaskQueue:
    ''
    def peek():
        pass

    def pop_head():
        pass

    def push_head():
        pass

    def push_sorted():
        pass

    def remove():
        pass


class TimeoutError:
    ''
_exc_context = None
_io_queue = None
def _promote_to_task():
    pass

_stop_task = None
_stopper = None
_task_queue = None
def create_task():
    pass

def get_event_loop():
    pass

def new_event_loop():
    pass

def run():
    pass

def run_until_complete():
    pass

select = None
def sleep():
    pass

def sleep_ms():
    pass

sys = None
def ticks():
    pass

def ticks_add():
    pass

def ticks_diff():
    pass

