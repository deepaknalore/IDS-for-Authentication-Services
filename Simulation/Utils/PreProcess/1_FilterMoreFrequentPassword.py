import json
import csv

LEAKED_DATA = "../../Resources/msn.csv"
PREPROCESSED_DATA = "../../Resources/msn_pp.csv"

PASSOWRD_LENGTH_FILTER = 10

with open(PREPROCESSED_DATA, "w") as pre_csv_file:
    writer = csv.writer(pre_csv_file)
    with open(LEAKED_DATA) as csv_file:
        for row in csv.reader(csv_file):
            if len(row) < 2:
                continue
            user = row[0]
            temp = json.loads(row[1])
            if(len(temp) > PASSOWRD_LENGTH_FILTER):
                continue
            writer.writerow(row)
