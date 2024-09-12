import math
import json
import pickle

def conversion(z,point, nodes):
    index = 0
    i = 0
    while i <= z:# and i <= len(nodes) - 1:
        j = 0
        while j <= point and j <= len(nodes[i]) - 1:
            index +=1
            j += 1
        i += 1
    return index


def create_edges(nodes, nodes_dict, min_dist = 30, z_space = 2.5): #z_space must be the space between z planes
    edges = []
    z_list = []

    for i in range(len(nodes)):
        if len(nodes[i]) != 0:
            z_list.append(nodes[i][0][2])

    for z in range(len(z_list)):
        i = 0
        z_min = z_list[z]-min_dist
        z_max = z_list[z]+min_dist
        z_min_holder = z_list[0]
        z_max_holder = z_list[-1]
        for i in z_list:
            if i <= z_min and abs(i - z_min) < abs(z_min_holder - z_min):
                z_min_holder = i
            if i >= z_max and i - z_max < z_max_holder - z_max:
                z_max_holder = i
        z_vals = []
        while z_min_holder <= z_max_holder:
            z_vals.append(z_min_holder)
            z_min_holder += z_space

        for i in range(len(nodes[z])):
            for j in range(len(z_vals)):
                for k in range(len(nodes[j])):
                    if math.dist(nodes[z][i], nodes[j][k]) <= min_dist and nodes[z][i] != nodes[j][k]:
                        edges.append([conversion(z, i, nodes), conversion(j,k,nodes)])
        print(str(z) + " out of " + str(len(z_list)) + " slices done")
    return edges

def create_arcs(nodes, min_dist = 30):
    arcs = []
    node_arcs = {}
    matrix = []
    neighborhood = {key: [] for key in nodes}
    for i in nodes.keys():
        count = 0

        holder = []
        holder.clear()
        matrix_holder = []
        matrix_holder.clear()
        for j in nodes.keys():
            if math.dist(nodes[i], nodes[j]) <= min_dist and i != j:
                arcs.append([i,j])
                holder.append(j)
                matrix_holder.append(1)
                count +=1
            elif min_dist < math.dist(nodes[i], nodes[j]) <= min_dist + 10 and i != j:
                neighborhood[i].append(j)
                matrix_holder.append(0)
            else:
                matrix_holder.append(0)
        node_arcs[i] = holder
        matrix.append(matrix_holder)
        for k in range(100):
            if i == str(round((len(nodes)*k)/100)):
                print(str(k) + " out of 100 done")
    return arcs, node_arcs, matrix, neighborhood


if __name__ == '__main__':

    node_list = []
    json_holder = []
    with open("../data/candidate_points.json", 'r') as openfile:
        json_holder = json.load(openfile)

    node_list = [ele for ele in json_holder if ele != []]

    print("file read")
    node_dict = {}
    neighborhood = {}
    index = 0
    for i in range(len(node_list)):
        for j in range(len(node_list[i])):
            node_dict[str(index)] = node_list[i][j]
            index += 1

    print("nodes loaded")

    arcs, node_arcs, matrix, neighborhood = create_arcs(node_dict)

    #arcs = create_edges(node_list, node_dict)

    print("arcs done")



    with open('../data/node_data.pkl', 'wb') as outfile:
        pickle.dump(node_dict, outfile)


    with open('../data/arc_data.pkl', 'wb') as outfile:
        pickle.dump(arcs, outfile)

    with open('../data/adjacency_matrix.pkl', 'wb') as outfile:
        pickle.dump(matrix, outfile)


    with open('../data/arc_list.pkl', 'wb') as outfile:
        pickle.dump(node_arcs, outfile)

    with open('../data/neighborhood.pkl', 'wb') as outfile:
        pickle.dump(neighborhood, outfile)