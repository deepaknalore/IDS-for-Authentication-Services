import csv
import json
import editdistance
import random
import sys

LEAKED_DATA = "../Resources/updated_wisc_pp.csv"

csv.field_size_limit(sys.maxsize)

dict = {}

multiplePasswords = {}
frequentPasswords = []
topFrequencyLimit = 1000
editDistanceLimit = 2

def multiplePasswordFinder(data):
    global multiplePasswords
    for user in data:
        if len(data[user]) in multiplePasswords:
            multiplePasswords[len(data[user])] += 1
        else:
            multiplePasswords[len(data[user])] = 1

def makeFrequencyDict(data):
    frequencyDict = {}
    for user in data:
        for password in data[user]:
            if password not in frequencyDict:
                frequencyDict[password] = 0
            frequencyDict[password] += 1
    return frequencyDict

def frequentPasswordsFinder(data):
    frequencyDict= makeFrequencyDict(data)
    dd = sorted(frequencyDict.items(), key=lambda x: x[1], reverse=True)
    return dd[:topFrequencyLimit]

# This edit distance compares all the password pairs
def editDistanceFinder(data, distanceLimit):
    totalPairs = 0
    pairsWith2Edits = 0
    for user in data:
        if (len(data[user]) > 1):
            for i in range(len(data[user])):
                for j in range(i+1, len(data[user])):
                    totalPairs += 1
                    if(editdistance.eval(data[user][i], data[user][j]) <= distanceLimit):
                        pairsWith2Edits += 1

    return totalPairs, pairsWith2Edits

# This edit distance compares two random passwords for a user, randomly picking two passwords for a user
def editDistanceFinderNew(data, distanceLimit):
    totalPairs = 0
    pairsWith2Edits = 0
    for user in data:
        if (len(data[user]) > 1):
            totalPairs += 1
            sampled_password = random.sample(data[user], 2)
            sampled_password[0] = sampled_password[0].lower()
            sampled_password[1] = sampled_password[1].lower()
            if (editdistance.eval(sampled_password[0], sampled_password[1]) <= distanceLimit):
                pairsWith2Edits += 1
    return totalPairs, pairsWith2Edits


with open(LEAKED_DATA, "r") as csv_file:
    for row in csv.reader(csv_file):
        if len(row) < 2:
            continue
        user = row[0]
        passwordList = json.loads(row[1])
        # passwordList = []
        # passwordList.append(row[1])
        dict[user] = passwordList
    multiplePasswordFinder(dict)
    frequentPasswords = frequentPasswordsFinder(dict)
    totalPairs, pairsWith1Edits = editDistanceFinder(dict, 1)
    totalPairs, pairsWith2Edits = editDistanceFinder(dict, 2)
    totalPairs, pairsWith3Edits = editDistanceFinder(dict, 3)
    totalPairsNew, pairsWith1EditsNew = editDistanceFinderNew(dict, 1)
    totalPairsNew, pairsWith2EditsNew = editDistanceFinderNew(dict, 2)
    totalPairsNew, pairsWith3EditsNew = editDistanceFinderNew(dict, 3)

for password in frequentPasswords:
    print(password)

print("########### STATS - Multiple passwords ###########")
print("Users with multiple passwords: ")
print(multiplePasswords)
print("\n\n\n\n\n\n\n########### STATS - Password Edit distances - Old info ###########")
print("Total number of password pairs compared: " + str(totalPairs))
if(totalPairs > 0):
    print("Password pairs where the edit distance is less than 1 " + str(pairsWith1Edits))
    print("Percentage of pairs with edit distance less than 1: " + str(pairsWith1Edits*100/totalPairs))
    print("Password pairs where the edit distance is less than 2 " + str(pairsWith2Edits))
    print("Percentage of pairs with edit distance less than 2: " + str(pairsWith2Edits*100/totalPairs))
    print("Password pairs where the edit distance is less than 3 " + str(pairsWith3Edits))
    print("Percentage of pairs with edit distance less than 3: " + str(pairsWith3Edits*100/totalPairs))



print("\n\n\n\n\n\n\n########### STATS - Password Edit distances - New info ###########")
print("Total number of password pairs compared: " + str(totalPairsNew))
if(totalPairs > 0):
    print("Password pairs where the edit distance is less than 1 " + str(pairsWith1EditsNew))
    print("Percentage of pairs with edit distance less than 1: " + str(pairsWith1EditsNew*100/totalPairsNew))
    print("Password pairs where the edit distance is less than 2 " + str(pairsWith2EditsNew))
    print("Percentage of pairs with edit distance less than 2: " + str(pairsWith2EditsNew*100/totalPairsNew))
    print("Password pairs where the edit distance is less than 3 " + str(pairsWith3EditsNew))
    print("Percentage of pairs with edit distance less than 3: " + str(pairsWith3EditsNew*100/totalPairsNew))
