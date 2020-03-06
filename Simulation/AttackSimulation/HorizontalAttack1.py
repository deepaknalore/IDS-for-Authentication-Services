import requests
import csv
import json

payload = {'user':'', 'password': '', 'metadata' : ''}
metadata = {'IP': '', 'Cookie': 0, 'Redirect' : 0, 'UserAgent' : ''}
userAgent = {'OS': 'MacOSX','Browser': 'Chrm'}
metadata['UserAgent'] = userAgent
payload['metadata'] = metadata

local_database = "../Resources/user.csv"

csvfile = open(local_database)
readCSV = csv.reader(csvfile, delimiter=',')

url = "http://127.0.0.1:5000/attack"
headers = {
  'Content-Type': 'application/json'
}

failedAuth = 0
sucessfulBreach = 0
blocked = 0

commonPasswordList = ['123456', '123456789', 'qwerty', 'password', '111111', '12345678', 'abc123', '1234567', 'password1', '12345']
for password in commonPasswordList:
  csvfile = open('user.csv')
  readCSV = csv.reader(csvfile, delimiter=',')
  for row in readCSV:
    for i in range(10):
      payload['user'] = row[0]
      payload['password'] = password
      payload['metadata']['IP'] = '1.2.1.' + str(i+1)
      response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
      data = response.json()
      if(data['Authentication'] == True):
        sucessfulBreach += 1
      elif(data['Authentication'] == False):
        failedAuth += 1
      elif(data['Authentication'] == 'Blocked'):
        blocked += 1

print('Number of blocked IPs: ' + str(blocked/149400))
print('Number of successful breaches: ' + str(sucessfulBreach/149400))
print('Number of failed auths: ' + str(failedAuth/149400))