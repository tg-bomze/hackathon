from api import create_token, translate
from datetime import datetime, timedelta
#from io import BytesIO
#from PIL import Image
import threading
import requests
import sqlite3
import base64
import socket
import math
import time
import json

global data
global conn_db
global cursor
with open('data.json') as f:
	data = json.load(f)

HEADER = 256
PORT = 65433
SERVER = "127.0.0.1" 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
RADIUS = 1000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def distance(x1, y1, x2, y2):
    return math.sqrt(((float(x1)-float(x2))**2) + ((float(y1)-float(y2))**2))

def setPosition(ID, coord, RADIUS, data):
	global cursor
	cursor.execute("UPDATE Persons SET Coord = '{}' WHERE ID = {}".format(str(coord), str(ID)))
	conn_db.commit()
	coord = coord[1:-1].split(", ")
	cursor.execute("SELECT * FROM Persons WHERE ID = {}".format(int(ID)))
	table_row = cursor.fetchall()
	cursor.execute("SELECT * FROM Persons")
	rows = cursor.fetchall()
	dots = []
	for i in range(len(rows)):
		if int(rows[i][0]) != ID:
			another_ccord = rows[i][3][1:-1].split(", ")
			if RADIUS >= distance(coord[0], coord[1], another_ccord[0], another_ccord[1]): # если точка внутри окружности
				mes = rows[i][5]
				if rows[i][5] != '': # если не пустое поле текст
					if table_row[0][4] != rows[i][4]: # если языки разные
						end_time = datetime.strptime(data["end_time"],'%Y-%m-%dT%H:%M:%S.%fZ')
						if datetime.now() > end_time: # если временные лимиты кончились
							data["access_token"], data["end_time"] = create_token(data["oauth_token"])
							langs = list_lang(data["access_token"], data["folderId"])
							with open('data.json', 'w') as f: json.dump(data, f, sort_keys=True, indent=4)
							print("Токен успешно сгенерирован и действует до {}\n".format(data["end_time"]))
						end_time = datetime.strptime(data["end_time"],'%Y-%m-%dT%H:%M:%S.%fZ')
						if datetime.now() <= end_time: # если временные лимиты кончились
							trans = translate(data["access_token"], rows[i][4], table_row[0][4], rows[i][5], data["folderId"])
							for j in range(len(trans)):
								mes = "{} ({})".format(trans[j], rows[i][4])
							print(mes)
				response = '{"id":'+str(rows[i][0])+', "name":"'+rows[i][1]+'", "status":'+str(rows[i][2])+', "coord": "'+str(rows[i][3])+'", "text_orig":"'+rows[i][5]+'", "text_trans":"'+mes+'", "photo":'+rows[i][6]+'}'
				dots.append(response)
				cursor.execute("UPDATE Persons SET Text = '' WHERE ID = {}".format(str(rows[i][0])))
	conn_db.commit()
	return dots

def sendMessage(ID, STATUS, TEXT):
	global cursor
	cursor.execute("UPDATE Persons SET Status = '{}' WHERE ID = {}".format(str(STATUS), str(ID)))
	conn_db.commit()
	cursor.execute("UPDATE Persons SET Text = '{}' WHERE ID = {}".format(TEXT, str(ID)))
	conn_db.commit()
	cursor.execute("SELECT * FROM Persons WHERE ID = {}".format(int(ID)))
	conn_db.commit()
	return cursor.fetchall()

def auth():
	global cursor
	cursor.execute("SELECT * FROM Persons WHERE Status = 0")
	table_row = cursor.fetchall()
	if len(table_row) != 0: auth_response = '{"result":true, "value":{"id":'+str(table_row[0][0])+', "name":"'+table_row[0][1]+'", "status":1, "coord": "'+str(table_row[0][3])+'", "photo":"'+table_row[0][6]+'"}}'
	else: auth_response = '{"result":false}'
	try: 
		cursor.execute("UPDATE Persons SET Status = 1 WHERE ID = {}".format(str(table_row[0][0])))
		conn_db.commit()
	except: pass
	return table_row, auth_response

def handle_client(conn, addr):
	global data
	global conn_db
	global cursor
	print(f"[NEW CONNECTION] {addr} connected.")
	connected = True
	conn_db = sqlite3.connect("database.db")
	cursor = conn_db.cursor()
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if len(msg) > 0:
				# {"type":"sendMessage","id":1,"value":{"status":1,"text":"Hi"}}
				# {"type":"auth"}
				# {"type":"setPosition","id":1,"value":"[1, 1]"}
				req = json.loads(msg)
				if req["type"] == "auth":
					table_row, auth_response = auth()
					print("Количество символов при отправке ответа на запрос об аутентификации: " + str(len(auth_response)))
					print(table_row[0][:-1])
					conn.send(str(auth_response).encode(FORMAT))
				elif req["type"] == "sendMessage":
					new_text = sendMessage(req["id"], req["value"]["status"], req["value"]["text"])
					print(new_text[0][:-1])
				elif req["type"] == "setPosition":
					new_coord = setPosition(req["id"], req["value"], RADIUS, data)
					print("Количество точек в окружности: " + str(len(new_coord)))
					for i in range(len(new_coord)):
						if new_coord[i] != '':
							print(1)
							conn.send(str(new_coord[i]).encode(FORMAT))
						else: pass
	conn.close()
	server.close()

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()
