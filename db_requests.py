from datetime import datetime, timedelta
from api import create_token, translate
from io import BytesIO
from PIL import Image
import requests
import sqlite3
import base64
import json
import math

global cursor
global data
with open('data.json') as f:
    data = json.load(f)

ID = 1
COORD1 = [1,1]
COORD2 = [4,5]
RADIUS = 1000
STATUS = 22
TEXT = "Привет"

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

def distance(x1, y1, x2, y2):
    return math.sqrt(((float(x1)-float(x2))**2) + ((float(y1)-float(y2))**2))

def setPosition(ID, coord, RADIUS, data):
	cursor.execute("UPDATE Persons SET Coord = '{}' WHERE ID = {}".format(str(coord), str(ID)))
	conn.commit()
	cursor.execute("SELECT * FROM Persons WHERE ID = {}".format(int(ID)))
	table_row = cursor.fetchall()
	cursor.execute("SELECT * FROM Persons")
	rows = cursor.fetchall()
	dots = []
	for i in range(len(rows)):
		if int(rows[i][0]) != ID:
			another_ccord = rows[i][3][1:-1].split(",")
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
				response = '{"id":'+str(rows[i][0])+', "name":'+rows[i][1]+', "status":'+str(rows[i][2])+', "coord": "'+str(rows[i][3])+'", "text_orig":'+rows[i][5]+', "text_trans":'+mes+', "photo":'+rows[i][6]+'}'
				dots.append(response)
				cursor.execute("UPDATE Persons SET Text = '' WHERE ID = {}".format(str(rows[i][0])))
	conn.commit()
	return dots
	
def auth():
	global cursor
	cursor.execute("SELECT * FROM Persons WHERE Status = 0")
	table_row = cursor.fetchall()
	if len(table_row) != 0: auth_response = '{"result":true, "value":{"id":'+str(table_row[0][0])+', "name":'+table_row[0][1]+', "status":1, "coord": "'+str(table_row[0][3])+'", "photo":'+table_row[0][6]+'}}'
	else: auth_response = '{"result":false}'
	try: 
		cursor.execute("UPDATE Persons SET Status = 1 WHERE ID = {}".format(str(table_row[0][0])))
		conn.commit()
	except: pass
	return table_row, auth_response

def sendMessage(ID, STATUS, TEXT):
	cursor.execute("UPDATE Persons SET Status = '{}' WHERE ID = {}".format(str(STATUS), str(ID)))
	conn.commit()
	cursor.execute("UPDATE Persons SET Text = '{}' WHERE ID = {}".format(TEXT, str(ID)))
	conn.commit()
	cursor.execute("SELECT * FROM Persons WHERE ID = {}".format(int(ID)))
	return cursor.fetchall()
	
'''
new_text = sendMessage(ID, STATUS, TEXT)
print(new_text[0][:-1])

print("Расстояние между объектами: " + str(distance(COORD1[0], COORD1[1], COORD2[0], COORD2[1])))

new_coord = setPosition(ID, COORD1, RADIUS, data)
print("Количество точек в окружности: " + str(len(new_coord)))

table_row, auth_response = auth()
print("Количество символов при отправке ответа на запрос об аутентификации: " + str(len(auth_response)))
print(table_row[0][0])
'''
# Вставляем данные в таблицу
'''cursor.execute("INSERT INTO Persons VALUES (1, 'asabist', 1, 1, '{"x":223, "y":332}', 1, 1, '[2]', 'ru', 'base64')")
conn.commit()'''

# Редактируем данные в таблице
'''cursor.execute("UPDATE Persons SET Lang = 'en' WHERE Username = 'asabist'")
conn.commit()'''

# Удаляем данные из таблицы
'''cursor.execute("DELETE FROM Cards WHERE First_name = 'Pasha'")
conn.commit()'''

# Выводим строку из таблицы по одной из ячеек
'''cursor.execute("SELECT * FROM Cards WHERE First_name=?", [("Grisha")])
print(cursor.fetchall()) # или fetchone()
im = Image.open(BytesIO(base64.b64decode(func.json()['Data']['Receipt'])))'''

# Выводим содержимое таблицы, отсортированное по столбцу
'''for row in cursor.execute("SELECT rowid, * FROM Startups ORDER BY Raiting"):
    print(row)'''
