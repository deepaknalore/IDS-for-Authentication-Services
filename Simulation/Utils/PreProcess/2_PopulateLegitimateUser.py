import random
import csv
import json

LEAKED_DATA = "../../Resources/msn_pp.csv"
LEGITIMATE_USER_DATA = "../../Resources/user.csv"
LEAKED_DATA_UPDATED = "../../Resources/updated_msn_pp.csv"
NUMBER_OF_LEGITIMATE_USERS = 10000

list = []
legitimateList = []
updatedLeakedDataList = []

file_counter = 0
with open(LEAKED_DATA) as fd:
    lines = fd.readlines()
    for line in lines:
        file_counter += 1

for x in range(NUMBER_OF_LEGITIMATE_USERS):
    list.append(random.randint(1, file_counter))

with open(LEAKED_DATA) as csv_file:
    line_count = 0
    for row in csv.reader(csv_file):
        line_count += 1
        if len(row) < 2:
            continue
        user = row[0]
        temp = json.loads(row[1])
        if line_count in list:
            passwordIndex = random.randint(0, len(temp) - 1)
            password = temp[passwordIndex]
            legitimateList.append(user + "," + password + "\n")
            if len(temp) > 1:
                del temp[passwordIndex]
            else:
                continue
        temp = [json.dumps(item) for item in temp]
        updatedLeakedDataList.append(user + "," + "\"" + str(json.dumps(temp)) + "\"" + "\n")


with open(LEGITIMATE_USER_DATA, "w") as fd:
    for user_password in legitimateList:
        fd.write(user_password)

with open(LEAKED_DATA_UPDATED, "w") as fd:
    for user_password in updatedLeakedDataList:
        fd.write(user_password)