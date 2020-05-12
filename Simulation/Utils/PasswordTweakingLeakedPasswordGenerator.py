import random
import json
import csv

LEAKED_LEGITIMATE_USERS = "../Resources/leaked.csv"
LEAKED_DATA_UPDATED = "../Resources/updated_msn_pp.csv"
Leaked_Password_List = "../Resources/leaked_password.txt"

def getLeakedUsers():
    leaked_users_list = []
    with open(LEAKED_LEGITIMATE_USERS) as leaked:
        leaked_users = leaked.readlines()
        for user in leaked_users:
            leaked_users_list.append(user.rstrip())

def getAllLeakedPasswords(user_list):
    with open(LEAKED_DATA_UPDATED) as csv_file:
        for row in csv.reader(csv_file):
            print("Discontinued")

