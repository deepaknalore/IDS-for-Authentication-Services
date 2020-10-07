from app import app, redis_client
from datetime import datetime
import sqlite3 as sql
from haveibeenpwnd import check_email,check_password
from flask import request, render_template, jsonify, make_response, abort
from dbservice import auth_history_pb2,auth_history_pb2_grpc
import json
import editdistance
import grpc
import yaml

# fill this up
weight_dict = {""}
LEGITIMATE_DATABASE = "../Resources/database.db"
AUTHENTICATION_TRACK_COUNT = 1000
authentication_request_count = 0
universal_history = {}
rules = []

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

def rules_initializer():
    global rules
    with open('app/rules.yml') as f:
        rules = yaml.load(f, Loader=yaml.FullLoader)

def user_exists(user):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM USER where name = ?);", (user,))
        data = cur.fetchone()
        if data is not None:
            return 1
        else:
            return 0

def is_typo(user, password):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT password from USER where name = ?;", (user,))
        data = cur.fetchone()
        if data is None:
            return 0
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

# Status - 0 = Allowed, 1 = Failed, 2 = Blocked
def generate_messages(dict,params,status):
    return auth_history_pb2.AuthRequest(
        user = dict['user'],
        password = dict['password'],
        ip = dict['ip'],
        cookie = dict['cookie'],
        redirect = dict['redirect'],
        os = dict['os'],
        browser = dict['browser'],
        parameters = params,
        status = status
    )

def generate_update(dict,result):
    return auth_history_pb2.AuthRequest(
        user=dict['user'],
        password=dict['password'],
        ip=dict['ip'],
        cookie=dict['cookie'],
        redirect=dict['redirect'],
        os=dict['os'],
        browser=dict['browser'],
        status=result
    )

def blacklist(stub, dict, rule):
    responses = stub.GetBlockListCount(generate_messages(dict,rule['params'],rule['status']))
    if responses.count >= rule['threshold']:
        return rule['weight']
    else:
        return 0

def whitelist(stub, dict, rule):
    responses = stub.GetAllowListCount(generate_messages(dict,rule['params'],rule['status']))
    if responses.count >= rule['threshold']:
        return rule['weight']
    else:
        return 0

@app.route('/attack', methods = ['POST'])
def attack():
    global rules
    if len(rules) == 0:
        rules_initializer()
    dict = flatten_request(request)
    try:
        password_match = False
        blocked = False
        wvalue = 0
        bvalue = 0
        with sql.connect(LEGITIMATE_DATABASE) as con:
            cur = con.cursor()
            user = dict['user']
            password = dict['password']
            cur.execute("SELECT rowid from USER where name = ? and password = ?", (user, password))
            data = cur.fetchone()
            if data is not None:
                password_match = True
        channel = grpc.insecure_channel('localhost:50051')
        stub = auth_history_pb2_grpc.AuthHistoryStub(channel)
        for rule in rules:
            if(rule['weight'] > 0):
                wvalue += whitelist(stub, dict, rule)
            else:
                bvalue += blacklist(stub, dict, rule)
            print(bvalue)
            print(wvalue)
        if(bvalue > wvalue):
            result = '2'
            blocked = True
        else:
            if password_match:
                result = '0'
            else:
                result = '1'
        # Set the authentication back to the DB
        stub.PutAuthEntry(generate_update(dict,result))
        channel.close()
        if result == 0:
            return jsonify({"Authentication": True}), 200
        elif blocked == True:
            return jsonify({"Authentication": "Blocked"}), 401
    except Exception as e:
        print(e)
    return jsonify({"Authentication": False}), 401

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

