from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np

def my_algorithm(size):
   cube = [[[[] for i in range(size)] for j in range(size)] for k in range(size)]
   for i in range(size):
       for j in range(size):
           for k in range(size):
                   cube[i][j][k] = int(((2*((i+1) % 2)-1) * (2*((j+1) % 2)-1) * (2*((k+1) % 2)-1) + 1)*.5)

   return cube

def print_cube(cube):
   for i in range(len(cube)):
       for j in range(len(cube)):
           print(cube[i][j])
       print()
def evaluate(cube):
   total = 0
   for i in range(len(cube)):
       for j in range(len(cube)):
           for k in range(len(cube)):
            total += cube[i][j][k]
   return total

def optimization(size):

   model = Model("optimal") # create model

   x = model.addVars(size + 2, size + 2, size + 2, vtype = GRB.BINARY)

   model.addConstrs(x[i,j,k] + (x[i-1, j, k] + x[i+1, j, k] + x[i, j-1, k] + x[i, j+1, k] + x[i, j, k-1] + x[i, j, k+1])/7 <= 1 for i in range(1, size + 1) for j in range(1, size + 1) for k in range(1, size + 1))

   model.setObjective(quicksum(x[i+1,j+1,k+1] for i in range(size) for j in range(size) for k in range(size)), GRB.MAXIMIZE)

   model.setParam("OutputFlag", 1)
   model.update()
   model.optimize()

   if model.status == GRB.Status.OPTIMAL:
       holder = []
       holder = model.getAttr("x")

       return holder
   else:
       raise ValueError("Optimzation was weird")


def parse_solution(data, size):
   iteration = 0
   cube = [[[[] for i in range(size+2)] for j in range(size+2)] for k in range(size+2)]
   for i in range(size+2):
       for j in range(size+2):
           for k in range(size+2):
               cube[i][j][k] = int(data[iteration])
               iteration += 1
   return cube
def crop(cube, size):
   final = [[[[] for i in range(size)] for j in range(size)] for k in range(size)]
   for i in range(size):
       for j in range(size):
           for k in range(size):
               final[i][j][k] = cube[i+1][j+1][k+1]
   return final

def plot(cube, size):

   fig = plt.figure()
   ax = fig.add_subplot(projection='3d')

   for i in range(size):
       for j in range(size):
           for k in range(size):
               if cube[i][j][k] == 1:
                   ax.scatter(i,j,k, s=10, c=1)
   plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

   size = 10  #don't go past 20 ish

   my_solution = my_algorithm(size)

   print_cube(my_solution)
   print(evaluate(my_solution))

   optimal_solution = optimization(size)
   optimal_cube = parse_solution(optimal_solution,size)
   clean_cube = crop(optimal_cube, size)

   print_cube(clean_cube)
   print(evaluate(clean_cube))

   print("####################  SOLUTION  ####################")
   print("Cardinality of Maximum Independent Set for algorithm: " + str(evaluate(my_solution)))
   print("Cardinality of Maximum Independent Set for optimization: " + str(evaluate(clean_cube)))

   if evaluate(my_solution) == evaluate(clean_cube):
       print("Yay! its the same!")
       plot(my_solution, size)
   else:
       print("NOOO!")