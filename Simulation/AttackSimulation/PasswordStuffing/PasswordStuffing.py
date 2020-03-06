import requests
import csv
import json
import time

start_time = time.time()
local_database = "../Resources/credential_stuffing.csv"

payload = {'user':'', 'password': '', 'metadata' : ''}
metadata = {'IP': '', 'Cookie': 0, 'Redirect' : 0, 'UserAgent' : ''}
userAgent = {'OS': 'MacOSX','Browser': 'Chrm'}
metadata['UserAgent'] = userAgent
payload['metadata'] = metadata

url = "http://127.0.0.1:5000/attack"
headers = {
  'Content-Type': 'application/json'
}

password_stuffing_csv = "../../Resources/credential_stuffing.csv"

failedAuth = 0
sucessfulBreach = 0
blocked = 0

with open(password_stuffing_csv) as password_stuffing_f:
    readCSV = csv.reader(password_stuffing_f, delimiter=',')
    for row in readCSV:
        payload['user'] = row[0]
        password_list = json.loads(row[1])
        for password in password_list:
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