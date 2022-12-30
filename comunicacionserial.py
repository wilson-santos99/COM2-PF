from serial.tools import list_ports
import serial

COMPORT = ''

def available_ports(port,baud):
	global COMPORT
	try:
		for i in list_ports.comports():
			if port == i.device:
				COMPORT = serial.Serial(port=str(port), baudrate=str(baud))
				print("CONECTADO")
				return True
		return False
	except:
		print("OCURRIO UN PROBLEMA")
# port="COM1"
# baud="9600"
# available_ports(port,baud)