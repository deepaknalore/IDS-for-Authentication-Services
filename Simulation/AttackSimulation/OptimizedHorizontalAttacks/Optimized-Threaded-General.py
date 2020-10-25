import requests
import csv
import json
import time
import threading
import queue
from copy import deepcopy

start_time = time.time()

LEGITIMATE_USER_DATA = '../Resources/user.csv'

# Threading related information
q = queue.Queue()
n_thread = 10

payload = {'user':'', 'password': '', 'metadata' : ''}
metadata = {'IP': '', 'Cookie': 0, 'Redirect' : 0, 'UserAgent' : '', 'Attack' : 1}
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

class ThreadClass(threading.Thread):
    count = 0
    def __init__(self, q, ip):
        threading.Thread.__init__(self)
        self.q = q
        self.ip = "1.1.1." + str(ip)

    def run(self):
        global sucessfulBreach
        global failedAuth
        global blocked
        while True:
            payload = self.q.get()
            self.count += 1
            if self.count == 6:
                time.sleep(1)
                self.count = 1
            payload["metadata"]['IP'] = self.ip
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            data = response.json()
            if (data['Authentication'] == True):
                sucessfulBreach += 1
            elif (data['Authentication'] == False):
                failedAuth += 1
            elif (data['Authentication'] == 'Blocked'):
                blocked += 1
            self.q.task_done()


# Start all the threads
for i in range(n_thread):
    t = ThreadClass(q,i)
    t.setDaemon(True)
    #Start thread
    t.start()

commonPasswordList = ['123456', '123456789', 'qwerty', 'password', '1234567', '12345678', '12345', 'iloveyou', '111111', '123123']

for password in commonPasswordList:
    csvfile = open(LEGITIMATE_USER_DATA)
    readCSV = csv.reader(csvfile, delimiter=',')
    total_users = 0
    for row in readCSV:
        payload['user'] = row[0]
        payload['password'] = password
        payload['metadata']['IP'] = '1.1.1.1'
        payload['metadata']['Attack'] = 1
        q.put(deepcopy(payload))
        total_users += 1
    q.join()

print('Number of blocked IPs: ' + str(blocked))
print('Number of successful breaches: ' + str(sucessfulBreach))
print('Number of failed auths: ' + str(failedAuth))

print('Number of blocked %: ' + str(blocked/(total_users*len(commonPasswordList)) * 100))
print('Number of successful breaches: ' + str(sucessfulBreach/(total_users*len(commonPasswordList)) * 100))
print('Number of failed auths: ' + str(failedAuth/(total_users*len(commonPasswordList)) * 100))

print("Total time : %s seconds"  %(time.time() - start_time ))