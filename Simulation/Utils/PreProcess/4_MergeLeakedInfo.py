import random

LEAKED_DATA_INFO = "../../Resources/msn_pp.csv"
LEAKED_LEGITIMATE_USERS = "../../Resources/leaked.csv"
ALL_LEAKED_DATA = "../../Resources/all_leaked.csv"

leaked_data_count = 0

list = []
with open(LEAKED_DATA_INFO) as fd:
    lines = fd.readlines()
    for line in lines:
        list.append(line)
        leaked_data_count += 1

leaked_legitimate_user_count = 0
with open(LEAKED_LEGITIMATE_USERS) as fd:
    lines = fd.readlines()
    for line in lines:
        leaked_legitimate_user_count += 1

pick_leaked_data = []
for x in range(leaked_legitimate_user_count):
    pick_leaked_data.append(random.randint(1, leaked_data_count))

index = 0
with open(LEAKED_LEGITIMATE_USERS) as local_data_info_f:
    lines = local_data_info_f.readlines()
    for line in lines:
        list.insert(pick_leaked_data[index],line)

out_file = open(ALL_LEAKED_DATA, "w")
for element in list:
    out_file.write(element)
out_file.close()