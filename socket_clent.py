import socket
import time

HEADER = 256
PORT = 65433
SERVER = "127.0.0.1" 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

try:
	cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cs.connect(ADDR)

	while True:
		msg = input("Write: ")
		if msg == "end": break
		message = msg.encode(FORMAT)
		msg_length = len(message)
		send_length = str(msg_length).encode(FORMAT)
		send_length += b' ' * (HEADER - len(send_length))
		cs.send(send_length)
		cs.send(message)
	cs.close()
except ConnectionRefusedError:
	print("Start the server first!")
