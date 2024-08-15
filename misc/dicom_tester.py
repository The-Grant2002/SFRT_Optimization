import matplotlib.pyplot as plt
import pydicom
'''
from dicom_csv import join_tree
import DicomRTTool
from dicom_csv.rtstruct import read_rtstruct
import json
from pydicom.data import get_testdata_file
from DicomRTTool.ReaderWriter import DicomReaderWriter,ROIAssociationClass
import dicom_csv
from rt_utils import RTStructBuilder
from skrt import Image
'''
ds = pydicom.dcmread(r"C:\Users\grant\Downloads\SampleData\SampleData\CT\CT.2.16.840.1.114362.1.12306304.26355686295.676003073.823.3428.dcm")
#ds = pydicom.dcmread(r"C:\Users\grant\Downloads\SampleData\SampleData\CT\RS.2.16.840.1.114362.1.12306304.26355686295.676003074.403.3455.dcm")
print(ds)
exit()
df = r"C:\Users\grant\Downloads\SampleData\SampleData\CT"
Dicom_reader = DicomReaderWriter(description='Examples')
Dicom_reader.walk_through_folders(df)
all_rois = Dicom_reader.return_rois(print_rois=True)

Contour_names = ['body']
#associations = [ROIAssociationClass('body')]
Dicom_reader.set_contour_names_and_associations(contour_names=Contour_names)
Dicom_reader.get_images_and_mask()


image_numpy = Dicom_reader.ArrayDicom
mask_numpy = Dicom_reader.mask
image_sitk_handle = Dicom_reader.dicom_handle
mask_sitk_handle = Dicom_reader.annotation_handle
exit()

df_rtstruct = collect_rtstructs(df)
contours_dict = read_rtstruct(df_rtstruct.iloc[0])
print(contours_dict)
exit()
structures = {}

#print(ds.group_dataset(10))
#print(ds.to_json_dict()) #helpfull
js = ds.to_json_dict()

print(js.keys())

exit()
for item in ds.StructureSetROISequence:
   structures[item.ROINumber] = item.ROIName


roi_seq = ds.ROIContourSequence

contour_pts = []
'''
contour = roi_seq[0].ContourSequence[0]
for i in range(len(contour.ContourData)-2):
   contour_pts.append([contour.ContourData[i], contour.ContourData[i + 1], contour.ContourData[i + 2]])
   i += 2
#print(roi_seq[0].ContourSequence[0].ContourData)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for i in range(len(contour_pts)):
   ax.scatter(contour_pts[i][0], contour_pts[i][1], contour_pts[i][2], s=10, c=1)
plt.show()
print(contour_pts)
exit()
'''
for contour in roi_seq[0].ContourSequence:
   image_item = contour.ContourImageSequence[0]
   for i in range(len(contour.ContourData)-3):
       contour_pts.append([contour.ContourData[i], contour.ContourData[i+1], contour.ContourData[i+2]])
       i+=2
   print('ROI NAME: ', structures[roi_seq[0].ReferencedROINumber])
   print('coordinates: ', contour.ContourData)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for i in range(len(contour_pts)):
   ax.scatter(contour_pts[i][0], contour_pts[i][1], contour_pts[i][2], s=10, c=1)
plt.show()

exit()




rtstruct = RTStructBuilder.create_from(dicom_series_path=r"C:\Users\grant\Downloads\SampleData\SampleData\CT", rt_struct_path=r"C:\Users\grant\Downloads\SampleData\SampleData\RS\RS.2.16.840.1.114362.1.12306304.26355686295.676003074.403.3455.dcm")

#print(rtstruct.get_roi_names())
exit()
mask_3d = rtstruct.get_roi_mask_by_name("BODY")
mask_1 = rtstruct.get_roi_mask_by_name("Primary Gross Tumor Volume")
#print(rtstruct.ROIContourSequence)
exit()
mask_slice = mask_1d[:,:,50]
plt.imshow(mask_slice)
plt.show()


file = get_testdata_file('MR_small.dcm')
ds = pydicom.dcmread(file)
y = ds.PixelData
x = ds.pixel_array
#print(ds.pixel_array)



#print(ds)
#print(ds[0x30060086])
#plt.imshow(ds.pixel_array, cmap=plt.cm.gray)

#plt.show()