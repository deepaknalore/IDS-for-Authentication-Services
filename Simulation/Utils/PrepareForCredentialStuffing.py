import csv
import random

main_data_leak_info = "../Resources/msn.csv"
local_data_info = "../Resources/user.csv"
credential_data_info = "../Resources/credential_stuffing.csv"
percentage_leaked = 10

list = []
master_data_count = 0
with open(main_data_leak_info) as main_data_leak_f:
    lines = main_data_leak_f.readlines()
    for line in lines:
        master_data_count += 1
        list.append(line)

count = 0
with open(local_data_info) as local_data_info_f:
    lines = local_data_info_f.readlines()
    for line in lines:
        count += 1
        line = line.split(",")
        for element in list:
            if line[0] in element:
                list.remove(element)
                break

count = int((count*percentage_leaked)/100)

pick_leaked_data = []
for x in range(count):
    pick_leaked_data.append(random.randint(1, 152673))

with open(local_data_info) as local_data_info_f:
    lines = local_data_info_f.readlines()
    line_count = 0
    for line in lines:
        if line_count in pick_leaked_data:
            list.insert(random.randint(1,master_data_count), line)
        line_count += 1

out_file = open(credential_data_info, "w")
for element in list:
    out_file.write(element)
out_file.close()

