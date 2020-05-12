from app import app, redis_client
from datetime import datetime
import sqlite3 as sql
from haveibeenpwnd import check_email,check_password
from flask import request, render_template, jsonify, make_response, abort
import json
import editdistance

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def user_exists(user):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM USER where name = ?)", (user))
        data = cur.fetchone()
        if data is not None:
            return 1
        else:
            return 0

def typo_distance(user, password):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT password from USER where name = ?", (user))
        data = cur.fetchone()
        if editdistance.eval(data,password) > 2:
            return 0
        else:
            return 1

def failed_password(request):
    return 0

def successful_password(request):
    return 1

def flatten_request(request):
    dict = {}
    dict['user'] = request.json['user']
    dict['password'] = request.json['password']
    metadata = request.json['metadata']
    dict['ip'] = metadata['IP']
    dict['cookie'] = metadata['Cookie']
    dict['redirect'] = metadata['Redirect']
    userAgent = metadata['UserAgent']
    dict['os'] = userAgent['OS']
    dict['browser'] = userAgent['Browser']
    return dict

def blacklist(dict):
    blacklistcount = 0
    keys = redis_client.keys("authentication:*")
    failed_count = 0
    for key in  keys:
        info = redis_client.hmget(key,["password","authenticated"])
        if info[0] == dict['password'] and info[1] == False:
            failed_count += 1
    if failed_count > 10 and user_exists(dict['user']) == 0:
        blacklistcount += 1

    if failed_count > 10 and typo_distance(dict['user'],dict['password']) == 0:
        blacklistcount += 1
    return  blacklistcount

def whitelist(dict):
    whitelistcount = 0
    keys = redis_client.keys("authentication:*")
    passwordcount = 0
    ipcount = 0
    for key in keys:
        info = redis_client.hmget(key, ["password", "ip","authenticated"])
        if info[2] == True:
            if info[0] == dict['password']:
                passwordcount += 1
            if info[1] == dict['ip']:
                ipcount += 1

    if passwordcount > 20:
        whitelistcount += 1
    if ipcount > 30:
        whitelistcount += 1

@app.route('/attack', methods = ['POST'])
def attack():
    if not request.json or not 'user' in request.json or not 'password' in request.json or not 'metadata' in request.json:
        abort(400)
    dict = flatten_request(request)
    authentication_request_count = 0
    if authentication_request_count == 1000:
        authentication_request_count = 0
    try:
        password_match = False
        with sql.connect("database.db") as con:
            cur = con.cursor()
            user = request.json['user']
            password = request.json['password']
            cur.execute("SELECT rowid from USER where name = ? and password = ?", (user, password))
            data = cur.fetchone()
            if data is not None:
                password_match = True
        bvalue = blacklist(dict)
        wvalue = whitelist(dict)
        if(bvalue > wvalue):
            dict['authenticated'] = False
        else:
            if password_match:
                dict['authenticated'] = True
            else:
                dict['authenticated'] = False
        redis_client.hmset("authentication:" + str(authentication_request_count), mapping=dict)
        if dict['authenticated'] == True:
            return jsonify({"Authentication": True}), 200
    except Exception as e:
        print(e)
    return jsonify({"Authentication": False}), 401


# @app.route('/attack', methods = ['POST'])
# def attack():
#     if not request.json or not 'user' in request.json or not 'password' in request.json or not 'metadata' in request.json:
#         abort(400)
#     try:
#         metadata = request.json['metadata']
#         ip = metadata['IP']
#         if(redis_client.exists(ip)):
#             data = redis_client.get(ip)
#             ip_stats = json.loads(data)
#             td = datetime.now() - datetime.strptime(ip_stats['last_time'], '%Y-%m-%d %H:%M:%S.%f')
#             if (int(td.total_seconds()) >= 1):
#                 ip_stats['last_time'] = datetime.now()
#                 ip_stats['count'] = 0
#             if(ip_stats['count'] <= 5):
#                 ip_stats['count'] = ip_stats['count'] + 1
#             if(ip_stats['count'] > 5 and int(td.total_seconds()) < 1):
#                 return jsonify({"Authentication": "Blocked"}), 201
#             rval = json.dumps(ip_stats, default=myconverter)
#             redis_client.set(ip, rval)
#         else:
#             ip_stats = {}
#             ip_stats['count'] = 1
#             ip_stats['last_time'] = datetime.now()
#             rval = json.dumps(ip_stats, default = myconverter)
#             redis_client.set(ip, rval)
#         with sql.connect("database.db") as con:
#             cur = con.cursor()
#             user = request.json['user']
#             password = request.json['password']
#             cur.execute("SELECT rowid from USER where name = ? and password = ?", (user, password))
#             data = cur.fetchone()
#             if data is not None:
#                 return jsonify({"Authentication": True}), 200
#     except Exception as e:
#         print(e)
#     return jsonify({"Authentication": False}), 200

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    if not request.json or not 'user' in request.json or not 'password' in request.json or not 'metadata' in request.json:
        abort(400)
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            user = request.json['user']
            password = request.json['password']
            metadata = request.json['metadata']
            ip = metadata['IP']
            cookie = metadata['Cookie']
            redirect = metadata['Redirect']
            userAgent = metadata['UserAgent']
            os = userAgent['OS']
            browser = userAgent['Browser']
            cur.execute("INSERT INTO AUTHENTICATION(name,password,ip,cookie,redirect,os,browser,date) VALUES (?,?,?,?,?,?,?,CURRENT_TIMESTAMP)",(user,password,ip,cookie,redirect,os,browser))
            con.commit()
            msg = "Record successfully added"
            print(msg)
    finally:
        con.close()
        return jsonify({"Authentication": True, "Check-email": check_email(request.json['user']), "Check-password": check_password(request.json['password'])}), 201


@app.route('/test', methods = ['GET'])
def test():
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT count(*) from USER")
        data = cur.fetchone()
        return jsonify({"DatabaseSize": data}), 200

