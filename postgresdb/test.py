from flask import jsonify
import json
import requests

url = "http://172.26.0.2:5100/"

con = requests.get(url)
js = con.json()




import pandas as pd
import numpy as np

posts = pd.read_excel('plusminus.xlsx')
minus = posts["Negative Sense Word List"]
plus = posts["Positive Sense Word List"]








table = []





def findposneg(sadpost,table,plustable,negtable):
    neg = 0
    pos = 0
    sadpost = sadpost.lower()
    sadpost = sadpost.split()
    for i in plustable:
        if i in sadpost:
            pos += 1
    for i in negtable:
        if i in sadpost:
            neg += 1
    table.append([pos,neg])
    return None

for i in js:
    findposneg(i["Text"],table,plus,minus)
poss = 0
negg = 0
for i in table:
    poss += i[0]
    negg += i[1]
print(poss,negg)
