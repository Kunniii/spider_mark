import pandas as pd
import re

p = re.compile('..1[3,4].+\d')
x = []
data = pd.read_csv('./data.csv')
for i in range(len(data)):
  roll = data.loc[:,"RollNumber"][i]
  if p.match(roll):
    continue
  x.append(data.iloc[i]["MemberCode"].lower())

print(x[0]["MemberCode"])