import sqlite3
import json

global pics
with open('pics.json') as f:
    pics = json.load(f)

conn = sqlite3.connect("database.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Persons
                (ID              INTEGER PRIMARY KEY,
                 Username        TEXT    NOT NULL,
                 Status          INTEGER NOT NULL,
                 Coord           TEXT    NOT NULL,
                 Lang            TEXT    NOT NULL,
				 Text            TEXT,
                 Photo           TEXT)""")
try:
    Persons = [(1, 'coder', 0, '[223, 332]', 'ru', '', pics["pic1"]),
	(2, 'designer', 0, '[233, 342]', 'en', '', pics["pic2"]),
	(3, 'investor', 0, '[223, 342]', 'ru', '', pics["pic3"]),
	(4, 'startuper', 0, '[233, 332]', 'ru', '', pics["pic4"]),
	(5, 'manager', 0, '[213, 322]', 'fr', '', pics["pic5"])]
    cursor.executemany("INSERT INTO Persons VALUES (?,?,?,?,?,?,?)", Persons)
    conn.commit()
except: pass

'''cursor.execute("""CREATE TABLE IF NOT EXISTS Rooms
                (ID              INTEGER PRIMARY KEY,
                 Room_type       TEXT    NOT NULL,
                 Room_name       TEXT    NOT NULL)""")
try:
    Rooms = [(1, 'Startup', 'Fase Recognation'),
          (2, 'Design', 'Design'),
          (3, 'Web', 'Web'),
          (4, 'ML', 'ML')]
    cursor.executemany("INSERT INTO Rooms VALUES (?,?,?)", Rooms)
    conn.commit()
except: pass


cursor.execute("""CREATE TABLE IF NOT EXISTS Startups
                (ID              INTEGER PRIMARY KEY,
                 Name            TEXT    NOT NULL,
                 Room_id         INTEGER NOT NULL,
                 Idea            TEXT    NOT NULL,
                 Target          TEXT    NOT NULL,
                 Time_interval   INTEGER,
                 Cost            INTEGER,
                 Vacancies       TEXT,
                 Raiting         TEXT    NOT NULL,
                 Description     TEXT    NOT NULL,
                 FOREIGN KEY (Room_id) REFERENCES Rooms (ID))""")
try:
    Startups = [(1, 'Fase Recognation', 2, 'Fase Recognation', 'Fase Recognation', 40, 1000, 'Prog', 5, 'About')]
    cursor.executemany("INSERT INTO Startups VALUES (?,?,?,?,?,?,?,?,?,?)", Startups)
    conn.commit()
except: pass


cursor.execute("""CREATE TABLE IF NOT EXISTS Cards
                (ID              INTEGER PRIMARY KEY,
                 First_name      TEXT    NOT NULL,
                 Second_name     TEXT    NOT NULL,
                 Company         TEXT,
                 Photo           TEXT,
                 Important       INTEGER,
                 Phone           TEXT,
                 Email           TEXT,
                 Whatsapp        TEXT,
                 Telegram        TEXT,
                 About           TEXT)""")
try:
    Cards = [(1, 'Grisha', 'Pupkin', 'Pupkin Inc', 'base64', 1, '+79609606060', 'pupkin@mail.ru', '+79609606060', 'pupkin', 'Im proger'),
         (2, 'Pasha', 'Lapin', 'Lapin Ind', 'base64', 1, '+79609606061', 'lapin@mail.ru', '+79609606061', 'lapin', 'Im investor')]
    cursor.executemany("INSERT INTO Cards VALUES (?,?,?,?,?,?,?,?,?,?,?)", Cards)
    conn.commit()
except: pass

cursor.execute("""CREATE TABLE IF NOT EXISTS Persons
                (ID              INTEGER PRIMARY KEY,
                 Username        TEXT    NOT NULL,
                 Status          INTEGER NOT NULL,
                 Room_id         INTEGER,
                 Coord           TEXT,
                 My_card_id      INTEGER,
                 Startups_id     INTEGER,
                 Cards_id        TEXT,
                 Lang            TEXT    NOT NULL,
                 Photo           TEXT,
                 FOREIGN KEY (Room_id) REFERENCES Rooms (ID),
                 FOREIGN KEY (Startups_id) REFERENCES Startups (ID),
                 FOREIGN KEY (My_card_id) REFERENCES Cards (ID))""")
try:
    Persons = [(1, 'asabist', 1, 1, '{"x":223, "y":332}', 1, 1, '[2]', 'ru', 'base64')]
    cursor.executemany("INSERT INTO Persons VALUES (?,?,?,?,?,?,?,?,?,?)", Persons)
    conn.commit()
except: pass
'''