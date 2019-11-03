import sqlite3

DATABASE = "tester.db"
USER_TABLE = "CREATE TABLE USER ([name] text,[password] text)"
LOGIN_TABLE = "CREATE TABLE AUTHENTICATION ([name] text,[password] text,[ip] text, [cookie] numeric, [redirect] numeric, [os] text, [browser] text, [date] text)"


conn = sqlite3.connect(DATABASE)
c = conn.cursor()
# c.execute(USER_TABLE)
c.execute(LOGIN_TABLE)
conn.commit()

