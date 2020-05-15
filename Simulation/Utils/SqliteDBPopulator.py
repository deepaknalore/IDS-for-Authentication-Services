import sqlite3
import random
import csv
import json

LEGITIMATE_USER_DATA = "../Resources/user.csv"
DATABASE = "../Resources/database.db"
INSERTION_QUERY = "INSERT INTO USER (name,password) VALUES(?,?)"
NUMBER_OF_ENTRIES = 10000

def process(row,cursor):
    user = row[0]
    password = row[1]
    cursor.execute(INSERTION_QUERY, (user, password))

conn = sqlite3.connect(DATABASE)
c = conn.cursor()
with open(LEGITIMATE_USER_DATA) as csv_file:
    for r in csv.reader(csv_file):
        if len(r) < 2:
            continue
        process(r,c)
conn.commit()
conn.close()
