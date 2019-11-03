import sqlite3
import random
import csv

LEAKED_DATA = "Resources/msn.csv"
DATABASE = "tester.db"
INSERTION_QUERY = "INSERT INTO USER (name,password) VALUES(?,?)"
NUMBER_OF_ENTRIES = 1500

def process(row,cursor):
    user = row[0]
    temp = row[1].replace("[","").replace("]","").replace("\"","").replace("\"","").strip().split(",")
    password = temp[random.randint(0,len(temp)-1)]
    cursor.execute(INSERTION_QUERY, (user, password))

list = []
for x in range(NUMBER_OF_ENTRIES):
    list.append(random.randint(1, 152673))
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
with open(LEAKED_DATA) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    line_count = 0
    for row in csv_reader:
        if line_count in list:
            process(row,c)
        line_count += 1
conn.commit()
conn.close()