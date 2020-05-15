import random
import json
import csv

# Main resource which needs to be obtained as is the source for all other files -> U
LEAKED_DATA = "../../Resources/msn.csv"

# This file contains only those users whose leaked password is less than 10 ->  PASSOWRD_LENGTH_FILTER
PREPROCESSED_DATA = "../../Resources/msn_pp.csv"

# Here, we are voluntarily duplicating a password for 40 percent of users -> PASSWORD_DUPLICATION_USERS_PERCENTAGE
DUPLICATE_PASSWORD_DATA = "../../Resources/msn_pp1.csv"

# The list of legitimate user, password pairs -> NUMBER_OF_LEGITIMATE_USERS
LEGITIMATE_USER_DATA = "../../Resources/user.csv"

# This is the username password, where some of them are taken in as legitimate username, password pairs.
# Out of the legitimate username, some of them are retained back giving as 'leaked info' -> Percentage of total users leaked
LEAKED_DATA_UPDATED = "../../Resources/updated_msn_pp.csv"

# List of leaked users
LEAKED_LEGITIMATE_USERS = "../../Resources/leaked.csv"

# List of leaked passwords
LEAKED_LEGITIMATE_PASSWORDS = "../../Resources/leaked_password.txt"

PASSOWRD_LENGTH_FILTER = 10
NUMBER_OF_LEGITIMATE_USERS = 1000
PERCENTAGE_LEAKED = 10
PASSWORD_DUPLICATION_USERS_PERCENTAGE = 40


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

def duplicatePasswords():
    file_counter = getCountOfFile(PREPROCESSED_DATA)
    length = (int)(PASSWORD_DUPLICATION_USERS_PERCENTAGE * file_counter)/100
    duplicateList = getRandomList(int(length), file_counter)
    with open(DUPLICATE_PASSWORD_DATA, "w") as pre_csv_file:
        writer = csv.writer(pre_csv_file)
        with open(PREPROCESSED_DATA) as csv_file:
            line_count = 0
            for row in csv.reader(csv_file):
                line_count += 1
                user = row[0]
                temp = json.loads(row[1])
                if line_count in duplicateList:
                    passwordIndex = random.randint(0, len(temp) - 1)
                    password = temp[passwordIndex]
                    temp.append(password)
                newList = []
                newList.append(user)
                newList.append(json.dumps(temp))
                writer.writerow(newList)


def populateLegitimateUserWithLeaks():
    legitimateList = []
    updatedLeakedDataList = []
    leakedUserList = []
    leakedPasswordList = []
    file_counter = getCountOfFile(PREPROCESSED_DATA)
    list = getRandomList(NUMBER_OF_LEGITIMATE_USERS,file_counter)
    legitimate_user_data_count = len(list)
    leaked_user_count = int((legitimate_user_data_count * PERCENTAGE_LEAKED) / 100)
    tempList = list
    random.shuffle(tempList)
    pick_leaked_data = tempList[0:leaked_user_count]

    with open(DUPLICATE_PASSWORD_DATA) as csv_file:
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
                    leakedUserList.append(str(user) + "\n")
                    for passw in temp:
                        leakedPasswordList.append(passw + "\n")
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
        for element in leakedUserList:
            out_file.write(element)

    # Write it to a leaked csv file
    with open(LEAKED_LEGITIMATE_PASSWORDS, "w") as out_file:
        for element in leakedPasswordList:
            out_file.write(element)

if __name__ == '__main__':
    filterMoreFrequentPasswords()
    duplicatePasswords()
    populateLegitimateUserWithLeaks()


