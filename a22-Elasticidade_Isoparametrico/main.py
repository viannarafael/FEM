import json
import numpy as np
from solver import *

with open("model.json") as jfile:
	data = json.load(jfile)

print("\n-----------------")
# Convert input
title = data["TITLE"]
print("\n",title)
dimensions = data["DIMENSIONS"]
coords = np.array(data["COORDS"])
connect = np.array(data["CONNECT"])
load= np.array(data["LOAD"])
restr = np.array(data["RESTR"])
prop = np.array(data["PROP"])
solver(coords, connect, load, restr, prop)
print("-----------------\n")
