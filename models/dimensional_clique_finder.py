import math

from gurobipy import *
import pickle

def optimization(nodes, arcs):
    model = Model("optimal")  # create model

    c = []
    for i in range(len(nodes)):
        c.append(10^i)
    x = model.addVars(nodes, nodes, vtype=GRB.CONTINUOUS)

    model.addConstrs(math.sqrt(sum((x[i][k]-x[j][k])^2 for k in nodes.keys)) == 1 for i,j in arcs)

    model.setObjective(quicksum(x[i][j]*c[j] for j in nodes.keys for i in nodes.keys), GRB.MAXIMIZE)
    model.setParam("OutputFlag", 1)

    model.update()
    model.optimize()

    if model.status == GRB.Status.OPTIMAL:
        holder = []
        holder = model.getAttr("x")
        return holder

node_dict = {}
with open("../data/node_data.pkl", 'rb') as openfile:
    node_dict = pickle.load(openfile)

arcs = []
with open("../data/arc_data.pkl", 'rb') as openfile:
    arcs = pickle.load(openfile)

node_index = optimization(node_dict,arcs)