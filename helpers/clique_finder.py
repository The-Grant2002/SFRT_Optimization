import networkx as nx
import json
import pickle

G = nx.Graph()

with open("../data/node_data.pkl", 'rb') as openfile:
    node_dict = pickle.load(openfile)

arcs = []
with open("../data/arc_data.pkl", 'rb') as openfile:
    arcs = pickle.load(openfile)

G.add_nodes_from(node_dict.keys())
G.add_edges_from(arcs)

sol = list(nx.find_cliques(G))

with open('../data/cliques.pkl', 'wb') as outfile:
    pickle.dump(sol, outfile)