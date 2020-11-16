import requests
import csv
import json
import time
import threading
import queue
from copy import deepcopy

start_time = time.time()

TWEAKED_PASSWORD_LIST = "../Resources/tweaked_attack.csv"

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
ip_count = 6

class ThreadClass(threading.Thread):
    count = 0
    def __init__(self, q, ip):
        global ip_count
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
            if ip_count > 15:
                ip_count = 6
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

with open(TWEAKED_PASSWORD_LIST) as csv_file:
    total_attacks = 0
    attack_count = 0
    for row in csv.reader(csv_file):
        user = row[0]
        password_list = json.loads(row[1])
        payload['user'] = user
        for password in password_list:
            payload['password'] = password
            payload['metadata']['IP'] = '1.1.1.1'
            payload['metadata']['Attack'] = 1
            q.put(deepcopy(payload))
            total_attacks += 1
    q.join()

print('Number of blocked IPs: ' + str(blocked))
print('Number of successful breaches: ' + str(sucessfulBreach))
print('Number of failed auths: ' + str(failedAuth))

print('Number of blocked %: ' + str(blocked/total_attacks * 100))
print('Number of successful breaches: ' + str(sucessfulBreach/total_attacks * 100))
print('Number of failed auths: ' + str(failedAuth/total_attacks * 100))

print("Total time : %s seconds"  %(time.time() - start_time ))