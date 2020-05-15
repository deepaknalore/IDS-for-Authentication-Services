
#commonPasswordList = ['123456', '123456789', 'qwerty', 'password', '111111', '12345678', 'abc123', '1234567', 'password1', '12345']
commonPasswordList = ['P3Rat54797', '123456', 'FQRG7CS493', '123456789', 'wmtmufc1', 'password1', 'password', 'abc123', 'p3rat54797', '123456a']

count = 0
with open("../Resources/user.csv") as fd:
    lines = fd.readlines()
    for line in lines:
        line = line.rstrip().split(",")
        if line[1] in commonPasswordList:
            count += 1

print("Common passwords in legitimate user: " + str(count))