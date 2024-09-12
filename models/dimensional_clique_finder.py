import math
import networkx as nx
from gurobipy import *
import pickle

def optimization(nodes, arcs):
    model = Model("optimal")  # create model

    c = []
    x = {}
    for i in range(len(nodes)):
        c.append(10*i)
    for i in nodes:
        for j in nodes:
            x[i,j] = model.addVar(vtype=GRB.BINARY)
    p = []
    #for i in nodes:
    #    for j in nodes:
    #        p[i,j] = 0

    model.addConstrs(sum((x[i,k]-x[j,k])**2 for k in nodes) == 2 for i,j in arcs)
    #model.addGenConstrexp(x[i,k]-x[j,k])**2 for k in nodes == 1 for i,j in arcs

    model.addConstrs(x[i,j] <= 1 for i in nodes for j in nodes)
    model.addConstrs(x[i,j] >= 0 for i in nodes for j in nodes)

    model.setObjective(sum(x[i,j]*c[j] for j in nodes for i in nodes), GRB.MINIMIZE)

    model.setParam("OutputFlag", 1)

    model.update()
    model.optimize()

    if model.status == GRB.Status.OPTIMAL:
        holder = {}
        holder = model.getAttr("x")
        return holder

node_dict = {}
with open("../data/node_data.pkl", 'rb') as openfile:
    node_dict = pickle.load(openfile)

arcs = []
with open("../data/arc_data.pkl", 'rb') as openfile:
    arcs = pickle.load(openfile)


T = nx.complete_graph(4)

G = nx.Graph()

G.add_nodes_from(node_dict.keys())
G.add_edges_from(arcs)

G_c = nx.complement(G)

test_sol = optimization(dict(T.nodes()), T.edges)



#vectors = optimization(node_dict,list(G_c.edges))

with open('../data/clique_test.pkl', 'wb') as outfile:
    pickle.dump(test_sol, outfile)

for i in range(len(test_sol)):
    print(test_sol[i])


'''
with open('../data/dimensional_cliques.pkl', 'wb') as outfile:
    pickle.dump(vectors, outfile)
    '''