import serial as ser
import serial.tools.list_ports as prtlst

global COMs
ports= prtlst.comports()

for port in ports:
	print(port)
	
