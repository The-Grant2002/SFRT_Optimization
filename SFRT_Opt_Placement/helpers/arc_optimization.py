from gurobipy import *
import matplotlib.pyplot as plt
import plotly.express as px
import random
import math
import json
import pickle

def optimization(nodes, arcs,time_limit):

   options = {
        "WLSACCESSID": "9a6728f5-f620-4829-b3b7-5e01b8e667d9",
        "WLSSECRET": "6f73eab7-cea6-4f6f-a167-510fd4aa9aa9",
        "LICENSEID": 2544834,
   }
   env = Env(params=options)
   model = Model("optimal", env=env)  # create model

   x = model.addVars(nodes, vtype=GRB.BINARY)

   model.addConstrs(x[i] + x[j] <= 1 for i,j in arcs)

   model.setObjective(quicksum(x[i] for i in nodes.keys()), GRB.MAXIMIZE)
   model.setParam("OutputFlag", 1)
   model.Params.TimeLimit = int(time_limit)
   #model.Params.TimeLimit = 160
   model.update()
   model.optimize()

   #if model.status == GRB.Status.OPTIMAL:
   holder = []
   holder = model.getAttr("x")

   return holder


def plot(cube, size):

   fig = plt.figure()
   ax = fig.add_subplot(projection='3d')

   for i in range(size):
       ax.scatter(cube[i][0], cube[i][1], cube[i][2], s=10, c=1)
   plt.show()
