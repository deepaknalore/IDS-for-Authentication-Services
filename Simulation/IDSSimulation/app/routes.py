from app import app, redis_client
from datetime import datetime
import sqlite3 as sql
from haveibeenpwnd import check_email,check_password
from flask import request, render_template, jsonify, make_response, abort
import json

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

@app.route('/attack', methods = ['POST'])
def attack():
    if not request.json or not 'user' in request.json or not 'password' in request.json or not 'metadata' in request.json:
        abort(400)
    try:
        metadata = request.json['metadata']
        ip = metadata['IP']
        if(redis_client.exists(ip)):
            data = redis_client.get(ip)
            ip_stats = json.loads(data)
            td = datetime.now() - datetime.strptime(ip_stats['last_time'], '%Y-%m-%d %H:%M:%S.%f')
            if (int(td.total_seconds()) >= 1):
                ip_stats['last_time'] = datetime.now()
                ip_stats['count'] = 0
            if(ip_stats['count'] <= 5):
                ip_stats['count'] = ip_stats['count'] + 1
            if(ip_stats['count'] > 5 and int(td.total_seconds()) < 1):
                return jsonify({"Authentication": "Blocked"}), 201
            rval = json.dumps(ip_stats, default=myconverter)
            redis_client.set(ip, rval)
        else:
            ip_stats = {}
            ip_stats['count'] = 1
            ip_stats['last_time'] = datetime.now()
            rval = json.dumps(ip_stats, default = myconverter)
            redis_client.set(ip, rval)
        with sql.connect("database.db") as con:
            cur = con.cursor()
            user = request.json['user']
            password = request.json['password']
            cur.execute("SELECT rowid from USER where name = ? and password = ?", (user, password))
            data = cur.fetchone()
            if data is not None:
                return jsonify({"Authentication": True}), 200
    except Exception as e:
        print(e)
    return jsonify({"Authentication": False}), 200

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

