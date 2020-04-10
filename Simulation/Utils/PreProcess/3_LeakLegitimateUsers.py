import random

LEGITIMATE_USERS = "../../Resources/user.csv"
PERCENTAGE_LEAKED = 10
LEAKED_LEGITIMATE_USERS = "../../Resources/leaked.csv"

legitimate_user_data_count = 0
with open(LEGITIMATE_USERS) as local_data_info_f:
    lines = local_data_info_f.readlines()
    for line in lines:
        legitimate_user_data_count += 1

leaked_user_count = int((legitimate_user_data_count*PERCENTAGE_LEAKED)/100)

pick_leaked_data = []
for x in range(leaked_user_count):
    pick_leaked_data.append(random.randint(1, legitimate_user_data_count))

leaked_list = []
with open(LEGITIMATE_USERS) as local_data_info_f:
    lines = local_data_info_f.readlines()
    line_count = 0
    for line in lines:
        if line_count in pick_leaked_data:
            leaked_list.append(str(line))
        line_count += 1

# Write it to a leaked csv file
out_file = open(LEAKED_LEGITIMATE_USERS, "w")
for element in leaked_list:
    out_file.write(element)
out_file.close()

# Append the leaked password with the main leaked password -> U_A + 0.1 * U_L
