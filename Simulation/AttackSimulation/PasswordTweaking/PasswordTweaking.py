import json
import time
import requests
import csv

tweaked_password_list = "../../Resources/tweaked_password.txt"
local_database = "../../Resources/user.csv"
LEAKED_DATA = "../../Resources/msn.csv"

tweaked_password_dict = {}

# Open the database and create a dict of user and his tweaked passwords
local_users = [] # store them in the format of user,password
with open(local_database) as fd:
    lines = fd.readlines()
    for line in lines:
        user_password = line.strip().split(",")
        local_users.append(user_password)

# Open the tweaked password and update the changed passw
with open(tweaked_password_list) as fd:
    lines = fd.readlines()
    for line in lines:
        row = line.split("\t")
        temp = json.loads(row[1])
        for local_user in local_users:
            if temp[0] == local_user[1]:
                tweaked_password_dict[local_user[0]] = temp[1:]

tweaked_success = {}
tweaked_success_count = 0
with open(LEAKED_DATA) as csv_file:
    line_count = 0
    for row in csv.reader(csv_file):
        if len(row) < 2:
            continue
        user = row[0]
        if user in tweaked_password_dict:
            temp = json.loads(row[1])
            tweaked_list = [i[0] for i in tweaked_password_dict[user]]
            if(len(set(json.loads(row[1])).intersection(set(tweaked_list))) > 0):
                tweaked_success[user] = set(json.loads(row[1])).intersection(set(tweaked_list))
                tweaked_success_count += 1

print(tweaked_success)

start_time = time.time()

payload = {'user':'', 'password': '', 'metadata' : ''}
metadata = {'IP': '', 'Cookie': 0, 'Redirect' : 0, 'UserAgent' : '', 'Attack' : True}
userAgent = {'OS': 'MacOSX','Browser': 'Chrm'}
metadata['UserAgent'] = userAgent
payload['metadata'] = metadata

url = "http://127.0.0.1:5000/attack"
headers = {
  'Content-Type': 'application/json'
}

failedAuth = 0
sucessfulBreach = 0
blocked = 0

for user in tweaked_password_dict:
    payload['user'] = user
    for password in tweaked_password_dict[user]:
        payload['password'] = password
        payload['metadata']['IP'] = '1.1.2.1'
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        data = response.json()
        if (data['Authentication'] == True):
            sucessfulBreach += 1
        elif (data['Authentication'] == False):
            failedAuth += 1
        elif (data['Authentication'] == 'Blocked'):
            blocked += 1

print('Number of blocked IPs: ' + str(blocked))
print('Number of successful breaches: ' + str(sucessfulBreach))
print('Number of failed auths: ' + str(failedAuth))

print('Number of blocked %: ' + str(blocked/14940 * 100))
print('Number of successful breaches: ' + str(sucessfulBreach/14940 * 100))
print('Number of failed auths: ' + str(failedAuth/14940 * 100))

print("Total time : %s seconds"  %(time.time() - start_time ))