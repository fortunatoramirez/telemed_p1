from socketIO_client import SocketIO
import serial
import time

# Conectando al socket del Servidor
print("Conectando al Servidor...")
socketIO = SocketIO('localhost',5001)
print("Conectado al Servidor.")

# Conectando por serial a Arduino
print("Conectando al Arduino...")
arduino = serial.Serial('COM6', 9600, timeout = 3.0)
arduino.isOpen()
print("Conectado al Arduino.")


def rutina(*args):
	print(args[0])
	arduino.write(args[0].encode())
	#arduino.write(args[0])

	
socketIO.on('desde_servidor', rutina)
socketIO.wait()