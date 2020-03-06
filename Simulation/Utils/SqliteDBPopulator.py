import sqlite3
import random
import csv
import json

LEAKED_DATA = "../Resources/msn.csv"
DATABASE = "../Resources/database.db"
INSERTION_QUERY = "INSERT INTO USER (name,password) VALUES(?,?)"
NUMBER_OF_ENTRIES = 10000

def process(row,cursor):
    user = row[0]
    temp = json.loads(row[1])
    password = temp[random.randint(0,len(temp)-1)]
    cursor.execute(INSERTION_QUERY, (user, password))

list = []
for x in range(NUMBER_OF_ENTRIES):
    list.append(random.randint(1, 152673))
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
with open(LEAKED_DATA) as csv_file:
    line_count = 0
    for r in csv.reader(csv_file):
        if len(r) < 2:
            continue
        if line_count in list:
            process(r,c)
    # for row in csv_reader:
    #     if line_count in list:
    #         process(row,c)
        line_count += 1
conn.commit()
conn.close()
