import json
import numpy as np
from solver import *

with open("model.json") as jfile:
	data = json.load(jfile)

print("\n-----------------")
# Convert input - Solver2
title = data["TITLE"]
print("\n",title)
dimensions = data["DIMENSIONS"]
coords = np.array(data["COORDS"])
connectedges = np.array(data["CONNECTEDGE"])
edgesElem= np.array(data["EDGESELEM"])
connect = np.array(data["CONNECTELEM"])
temp = np.array(data["TEMP"])
flux = np.array(data["FLUX"])
prop = np.array(data["PROPERTIES"])
solver(coords, connectedges, edgesElem, connect, temp, flux, prop)
print("-----------------\n")

