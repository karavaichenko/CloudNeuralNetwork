import psycopg2
import os
import json


class Database:
    def __init__(self):
        entry_data = str(os.path.dirname(os.path.abspath(__file__)))
        entry_data += "/option_for_connect.json"
        entry_data = os.path.normpath(entry_data)

        entry_data = open(entry_data, "r")
        entry_data = json.load(entry_data)

        self.conn = psycopg2.connect(**entry_data)
        self.cursor = self.conn.cursor()

    def take_user(self, login):
        try:
            self.cursor.execute(F"SELECT * FROM users WHERE login='{login}';")
            return list(self.cursor.fetchall())
        except:
            return list("1")

    def put_user(self, login, password, email):
        try:
            self.cursor.execute(f"INSERT INTO users(login, password, email) VALUES ('{login}', '{password}', '{email}');")
            self.conn.commit()
            return list("0")
        except:
            return list("1")

