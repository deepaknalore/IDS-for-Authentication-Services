import pickledb
import json
import csv
from itertools import chain
from collections import OrderedDict


TWEAKED_DB = "../../Resources/tweaked.db"
LEAKED_LEGITIMATE_USERS = "../../Resources/leaked.csv"
LEAKED_DATA_UPDATED = "../../Resources/updated_msn_pp.csv"
TWEAKED_ATTACK_INPUT = "../../Resources/tweaked_attack.csv"

db = pickledb.load(TWEAKED_DB, False)

def getLeakedUsers():
    leaked_users_list = []
    with open(LEAKED_LEGITIMATE_USERS) as leaked:
        leaked_users = leaked.readlines()
        for user in leaked_users:
            leaked_users_list.append(user.rstrip())
    return leaked_users_list

def listOfUsersAndTweakedPasswords(leaked_user_list):
    with open(TWEAKED_ATTACK_INPUT, "w") as pre_csv_file:
        writer = csv.writer(pre_csv_file)
        with open(LEAKED_DATA_UPDATED) as csv_file:
            for row in csv.reader(csv_file):
                if len(row) < 2:
                    continue
                user = row[0]
                if user not in leaked_user_list:
                    continue
                tweakedList = []
                temp = json.loads(row[1])
                for password in temp:
                    if db.get(password) == False:
                        continue
                    tempList = db.get(password)
                    tempList.insert(0, password)
                    tweakedList.append(tempList)
                newList = list(chain.from_iterable(zip(*tweakedList)))
                res = list(OrderedDict.fromkeys(newList))
                newList = []
                newList.append(user)
                newList.append(json.dumps(res))
                writer.writerow(newList)

if __name__ == '__main__':
    leaked_user_list = getLeakedUsers()
    listOfUsersAndTweakedPasswords(leaked_user_list)