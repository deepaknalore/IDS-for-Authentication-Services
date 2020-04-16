import random
import json
import csv

LEAKED_DATA = "../../Resources/msn.csv"
PREPROCESSED_DATA = "../../Resources/msn_pp.csv"
LEGITIMATE_USER_DATA = "../../Resources/user.csv"
LEAKED_DATA_UPDATED = "../../Resources/updated_msn_pp.csv"
LEAKED_LEGITIMATE_USERS = "../../Resources/leaked.csv"

PASSOWRD_LENGTH_FILTER = 10
NUMBER_OF_LEGITIMATE_USERS = 10000
PERCENTAGE_LEAKED = 10


def getCountOfFile(file):
    with open(file) as fd:
        lines = fd.readlines()
        return len(lines)

def getRandomList(length, limit):
    list = []
    for x in range(length):
        list.append(random.randint(1, limit))
    return list

def filterMoreFrequentPasswords():
    with open(PREPROCESSED_DATA, "w") as pre_csv_file:
        writer = csv.writer(pre_csv_file)
        with open(LEAKED_DATA) as csv_file:
            for row in csv.reader(csv_file):
                if len(row) < 2:
                    continue
                user = row[0]
                temp = json.loads(row[1])
                if (len(temp) > PASSOWRD_LENGTH_FILTER):
                    continue
                writer.writerow(row)

def populateLegitimateUserWithLeaks():
    legitimateList = []
    updatedLeakedDataList = []
    leakedList = []
    file_counter = getCountOfFile(PREPROCESSED_DATA)
    list = getRandomList(NUMBER_OF_LEGITIMATE_USERS,file_counter)
    legitimate_user_data_count = len(list)
    leaked_user_count = int((legitimate_user_data_count * PERCENTAGE_LEAKED) / 100)
    tempList = list
    random.shuffle(tempList)
    pick_leaked_data = tempList[0:leaked_user_count]

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
                if line_count not in pick_leaked_data:
                    if len(temp) > 1:
                        del temp[passwordIndex]
                    else:
                        continue
                else:
                    leakedList.append(str(user) + "," + password + "\n")
            # temp = [json.dumps(item) for item in temp]
            newList = []
            newList.append(user)
            newList.append(json.dumps(temp))
            updatedLeakedDataList.append(newList)

    with open(LEGITIMATE_USER_DATA, "w") as fd:
        for user_password in legitimateList:
            fd.write(user_password)

    with open(LEAKED_DATA_UPDATED, "w") as fd:
        writer = csv.writer(fd)
        for user_password in updatedLeakedDataList:
            writer.writerow(user_password)

    # Write it to a leaked csv file
    with open(LEAKED_LEGITIMATE_USERS, "w") as out_file:
        for element in leakedList:
            out_file.write(element)
        out_file.close()

if __name__ == '__main__':
    filterMoreFrequentPasswords()
    populateLegitimateUserWithLeaks()


