from concurrent import futures
import grpc
import sqlite3 as sql

import auth_history_pb2
import auth_history_pb2_grpc

LIMIT = 10000

#### SIMPLIFY this by exposing one API that will look after insertion and deletion
# Need to redefine the sql parser

counter = 0
db_file = "auth_history.db"
allow_list_threshold = 5
block_list_threshold = 5
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS auth_history (
                                        id integer PRIMARY KEY,
                                        user text NOT NULL,
                                        password text NOT NULL,
                                        ip text,
                                        cookie numeric,
                                        redirect numeric,
                                        os text,
                                        browser text,
                                        date text,
                                        status numeric
                                    ); """

def setup_db():
    conn = None
    try:
        conn = sql.connect(db_file, check_same_thread=False)
        if conn is not None:
            c = conn.cursor()
            c.execute(sql_create_projects_table)
        return conn
    except Exception as e:
        print(e)
    return conn

def generate_where_clause(request):
    if request.parameters is not None:
        where_clause = request.parameters.format(user = request.user, password = request.password, ip = request.ip,
                                                 cookie = request.cookie, redirect = request.redirect, os = request.os,
                                                 browser = request.browser)
        where_clause += " AND ("
        if request.status is not None:
            for status in request.status.split(','):
                where_clause += " status = " + status + " OR"
            return where_clause[:-2] + ')'
    return ""

def generate_sql_query(request):
    if request.parameters is not None:
        sql_query = request.parameters.format(user = request.user, password = request.password, ip = request.ip,
                                                 cookie = request.cookie, redirect = request.redirect, os = request.os,
                                                 browser = request.browser)
        return sql_query
    return ""

def insert_into_db(conn, request):
    global counter
    counter += 1
    if counter == LIMIT:
        counter = 1
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO auth_history(id,user,password,ip,cookie,redirect,os,browser,status,date) VALUES (?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)",
        (counter, request.user, request.password, request.ip, request.cookie, request.redirect, request.os, request.browser,
         int(request.status)))
    conn.commit()

class AuthHistoryServicer(auth_history_pb2_grpc.AuthHistoryServicer):
    def __init__(self):
        setup_db()

    def GetAllowListCount(self, request, context):
        conn = sql.connect(db_file)
        cur = conn.cursor()
        where_clause = generate_where_clause(request)
        cur.execute("SELECT COUNT(*) FROM auth_history WHERE " + where_clause)
        data = cur.fetchone()
        conn.close()
        return auth_history_pb2.AllowListCount(count = int(data[0]))

    def GetBlockListCount(self, request, context):
        conn = sql.connect(db_file)
        cur = conn.cursor()
        where_clause = generate_where_clause(request)
        cur.execute("SELECT COUNT(*) FROM auth_history WHERE " + where_clause)
        data = cur.fetchone()
        conn.close()
        return auth_history_pb2.BlockListCount(count = int(data[0]))

    def GetCustomAllowListCount(self, request, context):
        conn = sql.connect(db_file)
        cur = conn.cursor()
        sql_query = generate_sql_query(request)
        cur.execute(sql_query)
        data = cur.fetchone()
        conn.close()
        return auth_history_pb2.AllowListCount(count = int(data[0]))

    def GetCustomBlockListCount(self, request, context):
        conn = sql.connect(db_file)
        cur = conn.cursor()
        sql_query = generate_sql_query(request)
        cur.execute(sql_query)
        data = cur.fetchone()
        conn.close()
        return auth_history_pb2.BlockListCount(count = int(data[0]))

    def PutAuthEntry(self, request, context):
        conn = sql.connect(db_file)
        insert_into_db(conn, request)
        conn.close()
        return auth_history_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_history_pb2_grpc.add_AuthHistoryServicer_to_server(
        AuthHistoryServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

