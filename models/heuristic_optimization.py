from gurobipy import *
import matplotlib.pyplot as plt
import plotly.express as px
import random
import math
import json
import pickle


def test_sol(sol, nodes, arcs):
    '''

    :param sol: dict
    :param nodes:
    :param arcs: arc list
    :return:
    '''
    valid = True
    for i in sol.keys():
        for j in sol.keys():
            if i in arcs[j]:
                valid = False
                break
    return valid


def get_new_sol(primary_sol, nodes, arcs, neighborhood):
    solutions = []
    init_sol = {}
    count = 0
    for i in nodes.keys():
        init_sol[i] = primary_sol[count]
        count += 1
    for i in init_sol:
        if init_sol[i] == 1.0:
            for j in neighborhood[i]:
                init_sol[j] = 1.0
                if test_sol(init_sol, nodes, arcs):
                    solutions.append(init_sol)
                else:
                    init_sol[j] = -0.0
            for j in arc_list[i]:
                init_sol[i] = -0.0
                init_sol[j] = 1.0
                for k in neighborhood[j]:
                    init_sol[k] = 1.0
                    if test_sol(init_sol, nodes, arcs):
                        solutions.append(init_sol)
                    else:
                        init_sol[k] = -0.0
                init_sol[i] = 1.0
                init_sol[j] = -0.0
    return solutions


def optimization(nodes, arcs, init_sol = [], go = True):

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

   if init_sol != []:
       sol = {}
       sol = get_new_sol(init_sol, nodes, arc_list, neighborhood)
       for i in nodes:
           x.Start[i] = sol[i]

   model.setParam("OutputFlag", 1)
   model.Params.TimeLimit = 5

   model.update()
   model.optimize()

   holder = []
   holder = model.getAttr("x")
   print(holder)

   if go == True:
       optimization(node_dict,arcs, init_sol = holder)

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

    arc_list = {}
    with open("../data/arc_list.pkl", 'rb') as openfile:
        arc_list = pickle.load(openfile)

    arcs = []
    with open("../data/arc_data.pkl", 'rb') as openfile:
        arcs = pickle.load(openfile)

    neighborhood = {}
    with open("../data/neighborhood.pkl", 'rb') as openfile:
        neighborhood = pickle.load(openfile)


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