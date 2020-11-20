import requests
import csv
import json
import time
import threading
import queue
import random
from copy import deepcopy

start_time = time.time()

LEGITIMATE_USER_DATA = '../Resources/user.csv'

# Threading related information
q = queue.Queue()
n_thread = 10

payload = {'user':'', 'password': '', 'metadata' : ''}
metadata = {'IP': '', 'Cookie': 0, 'Redirect' : 0, 'UserAgent' : '', 'Attack' : -1}
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
ip_count = 1

class ThreadClass(threading.Thread):
    def __init__(self, q, ip):
        threading.Thread.__init__(self)
        self.q = q
        self.ip = "1.1.1." + str(ip)

    def run(self):
        global sucessfulBreach
        global failedAuth
        global blocked
        global ip_count
        while True:
            payload = self.q.get()
            payload["metadata"]['IP'] = "1.1.1." + str(ip_count)
            ip_count += 1
            if(ip_count) > 100:
                ip_count = 1
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

# put all the username, password into a list
legitimate_list = []
csvfile = open(LEGITIMATE_USER_DATA)
readCSV = csv.reader(csvfile, delimiter=',')
for row in readCSV:
    payload = {'user': '', 'password': '', 'metadata': ''}
    metadata = {'IP': '', 'Cookie': 0, 'Redirect': 0, 'UserAgent': ''}
    userAgent = {'OS': 'MacOSX', 'Browser': 'Chrm'}
    metadata['UserAgent'] = userAgent
    payload['metadata'] = metadata
    payload['user'] = row[0]
    payload['password'] = row[1]
    payload['metadata']['IP'] = '1.1.1.1'
    payload['metadata']['Attack'] = -1
    payload['metadata']['Cookie'] = random.choices([0,1],[0.5,0.5])[0]
    legitimate_list.append(payload)

starttime = time.time()
request_count = 0
while True:
    request_count += 1
    payload = random.choice(legitimate_list)
    q.put(deepcopy(payload))
    if(request_count > 12000):
        break
q.join()

print('Number of blocked IPs: ' + str(blocked))
print('Number of successful breaches: ' + str(sucessfulBreach))
print('Number of failed auths: ' + str(failedAuth))

print('Number of blocked %: ' + str(blocked/request_count * 100))
print('Number of successful breaches: ' + str(sucessfulBreach/request_count * 100))
print('Number of failed auths: ' + str(failedAuth/request_count * 100))

print("Total time : %s seconds"  %(time.time() - start_time ))