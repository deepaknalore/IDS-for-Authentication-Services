import csv
import json
import editdistance

LEAKED_DATA = "../Resources/msn.csv"

dict = {}

multiplePasswords = 0
frequentPasswords = []
topFrequencyLimit = 1000
editDistanceLimit = 2

def multiplePasswordFinder(data):
    global multiplePasswords
    for user in data:
        if(len(data[user]) > 1):
            multiplePasswords += 1

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

def editDistanceFinder(data):
    totalPairs = 0
    pairsWith2Edits = 0
    for user in data:
        if (len(data[user]) > 1):
            for i in range(len(data[user])):
                for j in range(i+1, len(data[user])):
                    totalPairs += 1
                    if(editdistance.eval(data[user][i], data[user][j]) <= editDistanceLimit):
                        pairsWith2Edits += 1

    return totalPairs, pairsWith2Edits


with open(LEAKED_DATA, "r") as csv_file:
    for row in csv.reader(csv_file):
        if len(row) < 2:
            continue
        user = row[0]
        passwordList = json.loads(row[1])
        dict[user] = passwordList
    multiplePasswordFinder(dict)
    frequentPasswords = frequentPasswordsFinder(dict)
    totalPairs, pairsWith2Edits = editDistanceFinder(dict)

print("########### STATS - Multiple passwords ###########")
print("Users with multiple passwords: " + str(multiplePasswords))
print("\n\n\n\n\n\n\n########### STATS - Password Edit distances ###########")
print("Total number of password pairs compared: " + str(totalPairs))
print("Password pairs where the edit distance is less than 2 " + str(pairsWith2Edits))
print("Percentage of pairs with edit distance less than 2: " + str(pairsWith2Edits*100/totalPairs))
print("\n\n\n\n\n\n\n########### STATS - Frequent passwords ###########")
print("Most Frequent passwords in descending order: ")
for password in frequentPasswords:
    print(password)