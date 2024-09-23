import pickle
from collections import OrderedDict
from scipy.optimize import minimize
import numpy as np
from gurobipy import *

import random


def index(V0, G, v):
    """Select the next vertex based on the index procedure."""
    scores = {}
    for k in V0:
        scores[k] = sum(v[j] for j in range(len(G)) if G[k, j] > 0)

    # Find the maximum score
    max_score = max(scores.values())
    candidates = [k for k, score in scores.items() if score == max_score]

    # Tie-breaking by smallest neighborhood
    if len(candidates) > 1:
        candidates = sorted(candidates, key=lambda k: sum(G[k, j] > 0 for j in range(len(G))))

    # Randomly select among tied candidates
    return random.choice(candidates)


def find_maximal_independent_set(G):
    """Find a maximal independent set using Algorithm 3."""
    n = len(G)
    v = np.zeros(n)  # Initialize the vertex states to 0
    V1 = set(range(n))  # Remaining vertices for the first step
    V2 = set(range(n))  # Remaining vertices for the second step

    # Step 1
    while V1:
        k = index(V1, G, v)
        if sum(v[j] for j in range(n) if G[k, j] > 0) < 1:
            v[k] = 1  # Add k to independent set
        else:
            v[k] = 0  # Do not add k
        V1.remove(k)

    # Step 2
    while V2:
        k = index(V2, G, v)
        if all(v[j] == 0 for j in range(n) if G[k, j] > 0):
            v[k] = 1  # Add k to independent set
        V2.remove(k)

    # Construct the maximal independent set
    I = {i for i in range(n) if v[i] == 1}

    return I




def greedy_init(nodes, arcs_dict):
    arcs = OrderedDict(sorted(arcs_dict.items(), key = lambda x :-1*len(x[1])))
    sol = list(nodes.keys())
    for i in arcs:

        if i in sol:
            sol.remove(i)

        done = True
        for j in sol:
            for k in sol:
                if j in arcs_dict[k] and j != k:
                    done = False
                    break
            if done == False:
                break
        if done == True:
            init_list = []
            for j in range(len(nodes)):
                for k in range(len(sol)):
                    if int(sol[k]) == j:
                        init_list.append(1)
                else:
                    init_list.append(0)
            return sol, init_list

        sol = sorted(sol, key = lambda x : -1*len(arcs_dict[x]))

def greedy_2(nodes, arcs_dict):
    arcs = OrderedDict(sorted(arcs_dict.items(), key = lambda x :-1*len(x[1])))
    sol = list(arcs.keys())
    count = 0
    for i in arcs:

        if count == 2700:
            print(sol)
        if count ==2701:
            print(sol)
        count+=1
        sol.remove(i)

        done = True
        for j in sol:
            for k in sol:
                if j in arcs_dict[k] and j != k:
                    done = False
                    break
            if done == False:
                break
        if done == True:
            return sol
        sol = sorted(sol, key = lambda x : -1*len(arcs_dict[x]))

def objective_funciton(x,G):
    penalty = sum(x[i] * x[j] for i,j in zip(*np.nonzero(G)))
    return -(np.sum(x) - penalty**2)

def sph_constraint(x,r):
    return np.sum(x**2) - r**2

def find_max_ind_set(G,x):
    n = len(G)
    indices = np.argsort(-x)
    independent_set = set()

    for i in indices:
        if all(j not in independent_set for j in range(n) if G[i,j] >0):
            independent_set.add(i)

    return independent_set
def quadratic_opt_heuristic():

    node_dict = {}
    with open("../data/node_data.pkl", 'rb') as openfile:
        node_dict = pickle.load(openfile)

    arcs = {}
    with open("../data/arc_list.pkl", 'rb') as openfile:
        arcs = pickle.load(openfile)
    arc_data = []
    with open("../data/arc_data.pkl", 'rb') as openfile:
        arc_data = pickle.load(openfile)
    adj = []
    with open("../data/adjacency_matrix.pkl", 'rb') as openfile:
        adj = pickle.load(openfile)

    start, init_list = greedy_init(node_dict, arcs)




    #test = greedy_2({0:[],1:[],2:[]},{0:[],1:[],2:[]})
    test = greedy_2(node_dict,arcs)


    G_large = np.array(adj)
    #G = G_large[:300,:300]

    G = G_large

    #print(find_maximal_independent_set(G))


    #G = np.array([[0, 1, 0, 0],
    #              [1, 0, 0, 1],
    #              [0, 1, 0, 1],
    #              [1, 1, 0, 0]])
    r = 100
    x0 = np.random.rand(len(G))

    constraints = [{'type':'eq', 'fun': sph_constraint, 'args':(r,)}]
    print("begining optimization")
    result = minimize(objective_funciton, x0, args=(G,), method='SLSQP', constraints=constraints,bounds=[(0,1)]*len(G), tol=10000,options={"maxiter":1})

    max_ind_set = find_max_ind_set(G, result.x)

    print(max_ind_set)

quadratic_opt_heuristic()

