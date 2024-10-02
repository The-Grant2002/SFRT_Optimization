import os
import pydicom
import pickle
import json
import csv
from SFRT_Opt_Placement.helpers.grid_placement import get_candidate_points
from SFRT_Opt_Placement.helpers.parameter_writer import create_arcs
from SFRT_Opt_Placement.helpers.arc_optimization import optimization

count = 0
for file in os.listdir(r"..\SFRT_Opt_Placement\dicom_file"):
    if file.endswith(".dcm"):
        count +=1
        path = os.path.join(r"..\SFRT_Opt_Placement\dicom_file", file)

if count != 1:
    raise Exception("Incorrect Number of dicom files in dicom_file, verify that only one dicom file (Rstruct) is in dicom_file directory")


ds = pydicom.dcmread(path)

contours = ds.ROIContourSequence

structures = {}
for item in ds.StructureSetROISequence:
   structures[item.ROINumber] = item.ROIName

print(structures.values())

points = []
try:
    k = list(structures.values()).index('PTV GRID')#39#12  #ROI 12 = ptv_grid 19 = ptv spheres, 23 = PTV VMAT, 27 GRIDptv_TM_RESEARCH
    if k != None:
        raise Exception("yay")
except Exception as e:
    pass
try:
    k = list(structures.values()).index('ptv_grid')
    if k != None:
        raise Exception("yay")
except Exception as e:
    pass

i = 0
j = 0 #slice

x = []
y = []
z = []

def get_planar_points(j, contours, granularity = 1):
    '''
    Takes contours, read from dicom file, outputs a list of x,y,z pairs
    :param j:
    :param contours:
    :param granularity:
    :return:
    '''

    i = 0
    z_val = contours[k].ContourSequence[j].ContourData[2]
    points = []
    candidates = []

    while i < len(contours[k].ContourSequence[j].ContourData):
        points.append([contours[k].ContourSequence[j].ContourData[i], contours[k].ContourSequence[j].ContourData[i + 1]])
        i += 3
    points_holder = get_candidate_points(points = points,granularity= granularity, plot = False)
    for i in range(len(points_holder)):
        candidates.append([points_holder[i][0], points_holder[i][1], float(z_val)])
        x.append(points_holder[i][0])
        y.append(points_holder[i][1])
        z.append(z)
    return candidates

candidate_points = []


p = 0
for i in range(len(contours[k].ContourSequence)):
    candidate_points.append(get_planar_points(j = p, contours = contours, granularity= 10)) #granularity in (mm)
    print('slice: ' + str(i))
    p+=1



#test to make sure list is properly shaped
for i in range(len(candidate_points)):
    for j in range(len(candidate_points[i])):
        if len(candidate_points[i][j]) != 3:
            print("nooooo")

print("Finished placing " + str(len(x)) + " points across " + str(len(contours[k].ContourSequence)) + " slices")

json_object = json.dumps(candidate_points)

with open(r'data\candidate_points.json', 'w') as outfile:
    outfile.write(json_object)


node_list = []
json_holder = []
with open("data\candidate_points.json", 'r') as openfile:
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

arcs, node_arcs, matrix, neighborhood, num_arcs = create_arcs(node_dict)

    #arcs = create_edges(node_list, node_dict)

print("arcs done")
print("created "+ str(num_arcs) + " arcs")



with open('data/node_data.pkl', 'wb') as outfile:
    pickle.dump(node_dict, outfile)

with open('data/arc_data.pkl', 'wb') as outfile:
    pickle.dump(arcs, outfile)

with open('data/arc_list.pkl', 'wb') as outfile:
    pickle.dump(node_arcs, outfile)



node_dict = {}
with open("data/node_data.pkl", 'rb') as openfile:
    node_dict = pickle.load(openfile)

arcs = []
with open("data/arc_data.pkl", 'rb') as openfile:
    arcs = pickle.load(openfile)

time_limit = input("How many seconds should the model run for?")

node_index = optimization(node_dict,arcs, time_limit)

optimal_nodes = []

for i in range(len(node_index)):
    node_index[i] = int(node_index[i])
    if node_index[i] == 1.0:
        optimal_nodes.append(node_dict.get(str(i)))

with open('Optimal_Points.csv','w', newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(optimal_nodes)
print()
print()
print("##########   Model completed   ###########################")
print(str(len(optimal_nodes)) + " spheres found")
print("Optimal Sphere Coordinates wrote to Optimal_Points.csv")