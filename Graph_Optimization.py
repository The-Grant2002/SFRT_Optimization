from gurobipy import *
import matplotlib.pyplot as plt
import random
import math
def create_nodes(size, num):
   nodes = {}
   seed = 5364
   random.seed(seed)
   for i in range(num):
       nodes[i] = [random.random()*size, random.random()*size, random.random()*size]
   return nodes

def create_arcs(nodes, min_dist):
   arcs = []
   for i in nodes.keys():
       for j in nodes.keys():
           if math.dist(nodes[i], nodes[j]) <= min_dist and i != j:
               arcs.append([i,j])
   return arcs

def create_matrix(nodes, arcs):
   matrix = [[[] for i in range(len(nodes)) ] for j in range(len(nodes))]
   for i in range(len(nodes)):
       for j in range(len(nodes)):
           matrix[i][j] = 0
   for i in range(len(nodes)):
       for j in range(len(nodes)):
           for k in arcs:
               if [i,j] == k:
                   matrix[i][j] = 1
   return matrix
def print_cube(cube):
   for i in range(len(cube)):
       print(cube[i])

def optimization(nodes, arcs):
   model = Model("optimal")  # create model

   x = model.addVars(nodes, vtype=GRB.BINARY)

   model.addConstrs(x[i] + x[j] <= 1 for i,j in arcs)
   #model.addConstrs(x[i] + quicksum(0.00001 * x[j] for i,j in arcs) <= 1 for i in nodes.keys())
   #model.addConstrs(x[i] + quicksum(x[j]*.0000001 for j in arcs[i]) <= 1 for i in nodes.keys())

   model.setObjective(quicksum(x[i] for i in nodes.keys()), GRB.MAXIMIZE)
   model.setParam("OutputFlag", 0)
   model.update()
   model.optimize()

   if model.status == GRB.Status.OPTIMAL:
       holder = []
       holder = model.getAttr("x")

       return holder
   else:
       raise ValueError("Optimzation was weird")


def plot(cube, size):

   fig = plt.figure()
   ax = fig.add_subplot(projection='3d')

   for i in range(size):
       ax.scatter(cube[i][0], cube[i][1], cube[i][2], s=10, c=1)
   plt.show()

nodes = create_nodes(10,1000)
arcs = create_arcs(nodes, 1.5)

#arc_matrix = create_matrix(nodes, arcs)

node_index = optimization(nodes,arcs)

optimal_nodes = []
max_set_size = 0

for i in range(len(nodes)):
   if node_index[i] == 1:
       optimal_nodes.append(nodes.get(i))
       max_set_size += 1


print(node_index)
print(optimal_nodes)
print(max_set_size)
plot(optimal_nodes,len(optimal_nodes))
plot(nodes,len(nodes))