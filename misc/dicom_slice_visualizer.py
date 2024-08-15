'''

Given a RStruct DICOM file, extract contours and plot an indexed ROI as a 3d plot and a single slice of the ROI

'''

import pydicom
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


#load file r"path"
ds = pydicom.dcmread(r"C:\Users\Grant\Downloads\SampleData\SampleData\CT\RS.2.16.840.1.114362.1.12306304.26355686295.676003074.403.3455.dcm")


#extract contour names
contours = ds.ROIContourSequence

structures = {}
for item in ds.StructureSetROISequence:
   structures[item.ROINumber] = item.ROIName

print(structures.values())


points = []
k = 12  #ROI 12 = ptv_grid 19 = ptv spheres, 23 = PTV VMAT, 27 GRIDptv_TM_RESEARCH
i = 0  #data point
j = 2  #slice

#create lists for plotting values
x = []
y = []
z = []

for j in range(len(contours[k].ContourSequence)):
   i = 0
   while i < len(contours[k].ContourSequence[j].ContourData):
       #add (x,y,z) contour point to list points
       points.append([contours[k].ContourSequence[j].ContourData[i], contours[k].ContourSequence[j].ContourData[i+1], contours[k].ContourSequence[j].ContourData[i+2]])
       x.append(contours[k].ContourSequence[j].ContourData[i])
       y.append(contours[k].ContourSequence[j].ContourData[i+1])
       z.append(contours[k].ContourSequence[j].ContourData[i+2])
       i+=3

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter3D(x,y,z)
plt.show()

ifig = px.scatter_3d(x = x, y = y, z=z)
ifig.show()

print(str(len(points)) + " border/contour points in the ROI")


x1 = []
y1 = []

j=15 #slice
i=0
while i < len(contours[k].ContourSequence[j].ContourData):
    points.append([contours[k].ContourSequence[j].ContourData[i], contours[k].ContourSequence[j].ContourData[i + 1]])
    x1.append(contours[k].ContourSequence[j].ContourData[i])
    y1.append(contours[k].ContourSequence[j].ContourData[i + 1])
    i += 3

fig2 = plt.figure()
ax = plt.axes()
ax.scatter(x1,y1)
plt.show()