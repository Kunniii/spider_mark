import re
import pandas as pd
from threading import Thread
from Spider import Spider

DATA = pd.read_csv('/home/kunix/coding/spider-mark/data.csv')
spidermans = []
number_of_spider = 2
usernames = []
p = re.compile('..1[3,4].+\d')

for i in range(len(DATA)):
  roll = DATA.loc[:, "RollNumber"][i]
  if p.match(roll):
    pass
  else:
    usernames.append(DATA.iloc[i]["MemberCode"].lower()+'+')

total = len(usernames)

def gogo():
  while usernames:
    username = usernames.pop(0)
    print(f'\t{abs(len(username)-total)}/{total}',end='\r')
    Spider(username).run()


for i in range(number_of_spider):
  spidermans.append(Thread(target=gogo))

for spiderman in spidermans:
  spiderman.start()