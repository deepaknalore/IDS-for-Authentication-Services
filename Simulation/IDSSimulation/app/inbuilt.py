from zxcvbn import zxcvbn
import editdistance
import sqlite3 as sql


LEGITIMATE_DATABASE = "../Resources/database.db"

def password_strength(request):
    results = zxcvbn(request['password'])
    return int(results['score'])

def typo(request):
    with sql.connect(LEGITIMATE_DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT password from USER where name = ?;", (request['user'],))
        data = cur.fetchone()
        if data is None:
            return 0
        return editdistance.eval(data,request['password'])

def invalid_account(request):
    with sql.connect(LEGITIMATE_DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT count(*) from USER where name = ?;", (request['user'],))
        data = cur.fetchone()
        if data is None:
            return 0
        if int(data[0]) > 0:
            return 0
        else:
            return 1

def display():
    print("This works")
    return 0