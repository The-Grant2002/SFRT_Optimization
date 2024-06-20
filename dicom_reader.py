'''

Given a rstruct dicom file, get contour points for a given indexed ROI,  get a list of all internal points for that ROI

Note: one unit = one millimeter


'''


import pydicom
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.style as mplstyle
from grid_placement import get_candidate_points
from grid_placement import plot2d

#supposedly speeds up matplotlib
mplstyle.use("fast")

ds = pydicom.dcmread(r"C:\Users\Grant\Downloads\SampleData\SampleData\CT\RS.2.16.840.1.114362.1.12306304.26355686295.676003074.403.3455.dcm")

contours = ds.ROIContourSequence

structures = {}
for item in ds.StructureSetROISequence:
   structures[item.ROINumber] = item.ROIName

print(structures.values())



points = []
k = 12  #ROI 12 = ptv_grid 19 = ptv spheres, 23 = PTV VMAT, 27 GRIDptv_TM_RESEARCH
i = 0
j = 0 #slice

x = []
y = []
z = []

candidates = []
def get_planar_points(j,contours, granularity = 1):

    i = 0
    z_val = contours[k].ContourSequence[j].ContourData[2]
    points.clear()
    while i < len(contours[k].ContourSequence[j].ContourData):
        points.append([contours[k].ContourSequence[j].ContourData[i], contours[k].ContourSequence[j].ContourData[i + 1]])
        i += 3
    points_holder = get_candidate_points(points = points,granularity= granularity, plot = False)

    for i in range(len(points_holder)):
        candidates.append([points_holder[i][0], points_holder[i][1], z_val])
        x.append(points_holder[i][0])
        y.append(points_holder[i][1])
        z.append(z)
    return candidates

candidate_points = []


for i in range(len(contours[k].ContourSequence)):
    candidate_points.append(get_planar_points(i,contours, 1)) #granularity in (mm)
    print('slice: ' + str(i))

#test to make sure list is properly shaped
for i in range(len(candidate_points)):
    for j in range(len(candidate_points[i])):
        if len(candidate_points[i][j]) != 3:
            print("nooooo")

print("Finished placing " + str(len(x)) + " points across " + str(len(contours[k].ContourSequence)) + " slices")


'''
fig_3D = plt.figure()
ax1 = fig_3D.add_subplot(projection='3d')
print("starting to plot..")
for i in range(len(x)):
    ax1.scatter(x[i],y[i],z[i])
    print(i)
print("plotting")
plt.show()
'''