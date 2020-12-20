"""
Module: 'network' on pySBC 1.13.0 with FW2.0.1-363
"""
# MCU: (sysname='pySBC', nodename='pySBC', release='1.13.0 with FW2.0.1', version='v1.13-363-g1fdf4f6ee-dirty on 2020-12-16', machine='simpleRTK-SBC-R02 with STM32H743')
# Stubber: 1.3.4
	
class SMS:
	''
	def callback():
		pass

	def send():
		pass

	def isbusy():
		pass

	def iserror():
		pass

class GSM:
    ''
    AUTHTYPE_CHAP = 2
    AUTHTYPE_EAP = 5
    AUTHTYPE_MSCHAP = 3
    AUTHTYPE_MSCHAP_V2 = 4
    AUTHTYPE_NONE = 0
    AUTHTYPE_PAP = 1
    SMS = None
    def active():
        pass

    def config():
        pass

    def connect():
        pass

    def disconnect():
        pass

    def ifconfig():
        pass

    def imei():
        pass

    def imsi():
        pass

    def isconnected():
        pass

    def qos():
        pass

    def status():
        pass

class LAN:
    ''
    def active():
        pass

    def config():
        pass

    def ifconfig():
        pass

    def isconnected():
        pass

    def status():
        pass

def route():
    pass

