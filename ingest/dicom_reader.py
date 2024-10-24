'''

Given a rstruct dicom file, get contour points for a given indexed ROI,  get a list of all internal points for that ROI

Note: one unit = one millimeter


'''


import pydicom
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.style as mplstyle
from relative_grid_placement import get_candidate_points
from grid_placement import plot2d
import json

#supposedly speeds up matplotlib
mplstyle.use("fast")

ds = pydicom.dcmread(r"C:\Users\Grant\Downloads\Anonymized grid\Grid 2 anonymized\2024-07__Studies\Grid2_Grid2_RTst_2024-07-29_145646_._ARIA.RadOnc.Structure.Sets_n1__00000\2.16.840.1.114362.1.12306304.27066498827.682660245.301.301.dcm")
#ds = pydicom.dcmread(r"C:\Users\Grant\Downloads\SampleData\SampleData\RS\RS.2.16.840.1.114362.1.12306304.26355686295.676003074.403.3455.dcm")
contours = ds.ROIContourSequence

structures = {}
for item in ds.StructureSetROISequence:
   structures[item.ROINumber] = item.ROIName

print(structures.values())



points = []
k =  39#12  #ROI 12 = ptv_grid 19 = ptv spheres, 23 = PTV VMAT, 27 GRIDptv_TM_RESEARCH
i = 0
j = 0 #slice

x = []
y = []
z = []

candidates = []
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

with open('../data/candidate_points.json', 'w') as outfile:
    outfile.write(json_object)

exit()
fig_3D = plt.figure()
ax1 = fig_3D.add_subplot(projection='3d')
print("starting to plot..")
for i in range(len(x)):
    ax1.scatter(x[i],y[i],z[i])
    print(i)
print("plotting")
plt.show()
