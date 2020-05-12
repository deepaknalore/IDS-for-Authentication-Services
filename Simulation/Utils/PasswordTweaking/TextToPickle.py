import pickledb
import json

TWEAKED_PASSWORD_LIST = "../../Resources/tweaked_leaked_pass.txt"
TWEAKED_DB = "../../Resources/tweaked.db"

db = pickledb.load(TWEAKED_DB, False)
with open(TWEAKED_PASSWORD_LIST) as fd:
    lines = fd.readlines()
    for line in lines:
        row = line.split("\t")
        temp = json.loads(row[1])
        tweaks = []
        for tweak in temp[1:]:
            tweaks.append(tweak[0])
        db.set(temp[0],tweaks)
db.dump()
