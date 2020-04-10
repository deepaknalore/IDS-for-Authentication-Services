
# This is the main leaked user password -> U
LEAKED_DATA = "msn.csv"

# Preprocessed leaked data -> removing user password's where the leaked password is greater than 10
PREPROCESSED_DATA = "msn_pp.csv"

# This is the legitimate user password pair -> For a given service -> U_L
LEGITIMATE_USER_DATA = "user.csv"

# We remove user password pairs which are part of legitimate service -> U_A = U - U_L
LEAKED_DATA_UPDATED = "msn_updated.csv"

# Number of user password pairs required as part of the service
NUMBER_OF_LEGITIMATE_USERS = 10000

# The percentage of user's leaked from U_L
PERCENTAGE_LEAKED = 10

# This is a small percentage of legitimate users who are leaked
LEAKED_LEGITIMATE_USERS = "leaked.csv"

# This is the actual leak which the attacker uses -> U_A + 0.1*U_L
ALL_LEAKED_DATA = "all_leaked.csv"

# The database where user password is stored
DATABASE_NAME = "database.db"


FLASK_URL = "http://127.0.0.1:5000/"
REDIS_URL = "redis://:password@localhost:6379/0"
