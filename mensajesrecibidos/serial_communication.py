from serial.tools import list_ports
import serial

COMPORT = ''

def available_ports(port):
	global COMPORT
	for i in list_ports.comports():
		if port == i.device:
			COMPORT = serial.Serial(port, timeout=1)
			return True
	return False


# from serial.tools import list_ports
# import serial


# def available_ports(port,baud):
# 	global COMPORT
# 	for i in list_ports.comports():
# 		if port == i.device:
# 			print("CONECTADO CON EXITO")
# 			COMPORT = serial.Serial(port, baudrate=baud)
# 			return True
# 	return False

