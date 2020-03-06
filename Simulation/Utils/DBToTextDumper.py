import sqlite3 as sql
import csv

with sql.connect("../Resources/database.db") as con:
    cur = con.cursor()
    c = cur.execute("SELECT * from USER")
    with open('../Resources/user.csv', 'w', newline='') as file:
        for i in c:
            csv.writer(file).writerow(i)
