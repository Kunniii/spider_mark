import re
import pandas as pd
from threading import Thread
from Spider import Spider

# DATA = pd.read_csv("./data.csv")
spidermans = []
number_of_spider = 4
usernames = []
# p = re.compile("..1[3,4].+\d")

# for i in range(len(DATA)):
#     roll = DATA.loc[:, "RollNumber"][i]
#     if p.match(roll):
#         pass
#     else:
#         print(f"[+] Loaded {roll}")
#         usernames.append(DATA.iloc[i]["MemberCode"].lower() + "+")

with open("logins.txt", "r") as f:
    usernames = [i.replace("\n", "") for i in f.readlines()]

total = len(usernames)


def gogo():
    while usernames:
        username = usernames.pop(0)
        print(f"[+] Getting {username}")
        Spider(username).run()


for i in range(number_of_spider):
    spidermans.append(Thread(target=gogo))

for spiderman in spidermans:
    spiderman.start()
