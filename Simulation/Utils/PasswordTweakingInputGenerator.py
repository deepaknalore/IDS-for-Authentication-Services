import random

local_data_info = "../Resources/user.csv"
credential_tweaking_info = "../Resources/credential_tweaking.csv"

percentage_leaked = 10
total_count = 0
list = []

with open(local_data_info) as local_data_info_f:
    lines = local_data_info_f.readlines()
    for line in lines:
        total_count += 1

count = int((total_count*percentage_leaked)/100)

pick_leaked_data = []
for x in range(count):
    pick_leaked_data.append(random.randint(1, total_count))

with open(local_data_info) as local_data_info_f:
    lines = local_data_info_f.readlines()
    line_count = 0
    for line in lines:
        if line_count in pick_leaked_data:
            password = line.split(",")[1]
            list.append(password)
        line_count += 1

out_file = open(credential_tweaking_info, "w")
for element in list:
    out_file.write(element)
out_file.close()
