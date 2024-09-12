from gurobipy import *
import matplotlib.pyplot as plt
import plotly.express as px
import random
import math
import json
import pickle

def optimization(nodes, arcs):

   options = {
        "WLSACCESSID": "9a6728f5-f620-4829-b3b7-5e01b8e667d9",
        "WLSSECRET": "6f73eab7-cea6-4f6f-a167-510fd4aa9aa9",
        "LICENSEID": 2544834,
   }
   #env = Env(params=options)
   model = Model("optimal")#,env=env)  # create model

   x = model.addVars(nodes, vtype=GRB.BINARY)

   model.addConstrs(x[i] + x[j] <= 1 for i,j in arcs)

   model.setObjective(quicksum(x[i] for i in nodes.keys()), GRB.MAXIMIZE)
   model.setParam("OutputFlag", 1)
   model.Params.TimeLimit = 21600
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

if __name__ == '__main__':

    node_dict = {}
    with open("../data/node_data.pkl", 'rb') as openfile:
        node_dict = pickle.load(openfile)

    arcs = []
    with open("../data/arc_data.pkl", 'rb') as openfile:
        arcs = pickle.load(openfile)

    node_index = optimization(node_dict,arcs)

    optimal_nodes = []

    for i in range(len(node_index)):
       node_index[i] = int(node_index[i])
       if node_index[i] == 1.0:
           optimal_nodes.append(node_dict.get(str(i)))



    print(node_index)
    print(optimal_nodes)
    print(len(optimal_nodes))
    plot(optimal_nodes,len(optimal_nodes))
    x = []
    y = []
    z = []
    for i in range(len(optimal_nodes)):
        x.append(optimal_nodes[i][0])
        y.append(optimal_nodes[i][1])
        z.append(optimal_nodes[i][2])

    ifig = px.scatter_3d(x=x, y=y, z=z)
    ifig.show()

    #plot(node_dict.values(),len(node_dict))