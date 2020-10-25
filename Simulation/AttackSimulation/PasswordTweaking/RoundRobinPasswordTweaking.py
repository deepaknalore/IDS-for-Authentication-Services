import json
import time
import requests
import csv

TWEAKED_PASSWORD_LIST = "../../Resources/tweaked_attack.csv"

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
count = 0
attack_count = 0

with open(TWEAKED_PASSWORD_LIST) as csv_file:
    for row in csv.reader(csv_file):
        user = row[0]
        password_list = json.loads(row[1])
        payload['user'] = user
        for password in password_list:
            attack_count += 1
            if attack_count == 6:
                time.sleep(1)
                attack_count = 1
            count += 1
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

print('Number of blocked %: ' + str(blocked/count * 100))
print('Number of successful breaches: ' + str(sucessfulBreach/count * 100))
print('Number of failed auths: ' + str(failedAuth/count * 100))

print("Total time : %s seconds"  %(time.time() - start_time ))