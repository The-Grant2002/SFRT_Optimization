import pickle

node_dict = {}
with open("../data/node_data.pkl", 'rb') as openfile:
    node_dict = pickle.load(openfile)

arcs = []
with open("../data/arc_list.pkl", 'rb') as openfile:
    arcs = pickle.load(openfile)

optimal = {}
for i in arcs.keys():
    optimal[i] = len(arcs[i])

holder = sorted(optimal.items(), key=lambda item: item[1])

neighborhood = []

for i in range(len(holder)):
    neighborhood.append(holder[i][0])
i = 0
while i < len(neighborhood):
    j = i
    while len(arcs[neighborhood[i]]) == len(arcs[neighborhood[j]]):
        j += 1
        if j == len(neighborhood):
            break

    next_degree = {}
    for k in range(i,j):
        holder = 0
        for l in arcs[neighborhood[k]]:
            holder += len(arcs[l])
        next_degree[neighborhood[k]] = holder
    list_holder = []
    list_holder = sorted(next_degree, key=lambda item: item[0])
    l = 0
    for k in range(i,j):
        neighborhood[k] = list_holder[l]
        l += 1
    i += 1


index = 0
for i in neighborhood:
    for j in arcs[i]:
        if neighborhood.index(j) > index:
            optimal.pop(j, None)
    index += 1
print(optimal)
print(len(optimal))