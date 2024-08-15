
import pydicom
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import plotly.express as px

#supposedly speeds up matplotlib
mplstyle.use("fast")

ds = pydicom.dcmread(r"C:\Users\Grant\Downloads\SampleData\SampleData\CT\RS.2.16.840.1.114362.1.12306304.26355686295.676003074.403.3455.dcm")

contours = ds.ROIContourSequence

structures = {}
for item in ds.StructureSetROISequence:
   structures[item.ROINumber] = item.ROIName

print(structures.values())

def get_x_boundary(points):
    '''
    Takes a set of points and returns the domain of the set
    :param points: list of (x,y) pairs
    :return: the maximum and minimum x values of the set
    '''
    xmax = points[0][0]
    for i in range(len(points)):
        if points[i][0] > xmax:
            xmax = points[i][0]
    xmin = points[0][0]
    for i in range(len(points)):
        if points[i][0] < xmin:
            xmin = points[i][0]

    return xmin, xmax

def get_x_values(xstart, xmin,xmax, granularity):
    '''
    Takes a domain and returns a list of all x values within that domain with a given granularity
    :param xmin: int: lowest x value
    :param xmax: int: max x value
    :param granularity: distance between points
    :return: list of all points between max and min
    '''
    x = []
    i = xstart
    while i <= xmax:
        if i >= xmin and i <= xmax:
            x.append(i)
        i += granularity
    return x


def get_line_intercept(p1, p2, x):
    '''
    helper function that returns f(x) for the line between p1,p2
    :param p1: list: single (x,y) pair
    :param p2: list: single (x,y) pair
    :param x: single x value
    :return: single y value
    '''
    slope = (p1[1] - p2[1]) / (p1[0] - p2[0])
    y = slope * (x - p1[0]) + p1[1]
    return y


def get_y_bounds(x, points):
    '''
    finds all y values of intercepts of the shape formed by the imputed points at the value of x
    :param x: single x value
    :param points: points that define the shape #### MUST BE ORDERED #####################
    :return: list of y values of intercepts at given x
    '''
    boundaries = []
    # Find boundary points
    for i in range(len(points)-1):
        if points[i][0] >= x and points[i+1][0] < x or points[i][0] <= x and points[i+1][0] > x:
            boundaries.append([points[i],points[i+1]])
    if points[-1][0] >= x and points[0][0] < x or points[-1][0] <= x and points[0][0] > x:
        boundaries.append([points[-1], points[0]])
    y = []
    for i in boundaries:
        y.append(get_line_intercept(i[0], i[1], x))
    return y

def get_y_values(ystart, ymin, ymax, granularity):
    '''
    Takes a range and returns a list of all y values within that range with a given granularity
    :param ymin: int: lowest y value
    :param ymax: int: max y value
    :param granularity: distance between points
    :return: list of all points between max and min
    Yes, this is the same as get_x_values()
    '''
    y = []
    i = ystart
    while i <= ymax:
        if i >= ymin and i <= ymax:
            y.append(i)
        i += granularity
    return y

def place_points(points, global_xmin, global_ymin, granularity = 30):

    xmin, xmax = get_x_boundary(points)

    x_list = get_x_values(global_xmin, xmin, xmax, granularity)

    #get valid y range
    y_bounds = []
    y_list = []

    coordinates = []

    for i in range(len(x_list)):
        y_list = []
        y_bounds.append(get_y_bounds(x_list[i], points))

        if len(y_bounds[i]) == 2: #if shape at x value is convex combination of points (only 2 points for an x)
            ymin = min(y_bounds[i])
            ymax = max(y_bounds[i])
            y_list.append(get_y_values(global_ymin, ymin, ymax, granularity))## Get y values for each x
        elif len(y_bounds[i]) == 1: #if there is only a single point for an x, just add that value
            y_list.append(y_bounds[i])
            print('single point placed')
        elif len(y_bounds[i]) % 2 == 0 and not(len(y_bounds[i]) == 2): #For an even number of points with convexity, assume that there is a hole
            y_subset = []
            y_holder = []
            y_bounds[i] = sorted(y_bounds[i])
            for j in range(len(y_bounds[i])):
                if j % 2 == 0:
                    y_subset.append(get_y_values(global_ymin, min(y_bounds[i][j], y_bounds[i][j+1]), max(y_bounds[i][j], y_bounds[i][j+1]), granularity))

            for j in range(len(y_subset)):
                y_holder.extend(y_subset[j])
            y_list.append(y_holder)

        elif len(y_bounds[i]) % 2 == 1 and len(y_bounds) != 1: # for an odd number of intersections, need to fix this algorithm
            print("odd intersections algorithm used")
            y_subset = []
            y_holder = []
            y_bounds[i] = sorted(y_bounds[i])
            print("bounds before")
            print(y_bounds[i])
            num = 0
            while num < len(y_bounds[i]):
                for index in points:
                    if [str(x_list[i]), str(y_bounds[i][num])] == index:
                        y_subset.append([y_bounds[i][num]])
                        del y_bounds[i][num]
                        num-=1
                num +=1

            print("bounds after")
            print(y_bounds[i])
            for j in range(len(y_bounds[i])):
                if j % 2 == 0 and y_bounds[i][j] != y_bounds[i][-1]:
                    y_subset.append(get_y_values(global_ymin, (y_bounds[i][j], y_bounds[i][j+1]), max(y_bounds[i][j], y_bounds[i][j+1]), granularity))
            for j in range(len(y_subset)):
                y_holder.extend(y_subset[j])
            y_list.append(y_holder)


        for j in range(len(y_list)):
            for k in range(len(y_list[j])):
                coordinates.append([x_list[i], y_list[j][k]])
    if coordinates != None:
        return coordinates


points = []
k = 12  #ROI 12 = ptv_grid 19 = ptv spheres, 23 = PTV VMAT, 27 GRIDptv_TM_RESEARCH
i = 0
j = 0 #slice

x = []
y = []
z = []

candidates = []
def get_planar_points(j, contours, globalx_min, globaly_min, granularity = 30):

    i = 0
    z_val = contours[k].ContourSequence[j].ContourData[2]
    points = []
    candidates = []

    while i < len(contours[k].ContourSequence[j].ContourData):
        points.append([contours[k].ContourSequence[j].ContourData[i], contours[k].ContourSequence[j].ContourData[i + 1]])
        i += 3
    points_holder = place_points(points = points,granularity= granularity, global_xmin = globalx_min, global_ymin = globaly_min)
    if (points_holder != None):
        for i in range(len(points_holder)):
            candidates.append([points_holder[i][0], points_holder[i][1], float(z_val)])
            x.append(points_holder[i][0])
            y.append(points_holder[i][1])
            z.append(z)
    return candidates

def run_heuristic(startingx, startingy):
    candidate_points = []

    p = 0

    for i in range(len(contours[k].ContourSequence)):
        if (contours[k].ContourSequence[p].ContourData[2] - contours[k].ContourSequence[0].ContourData[2]) % 30 == 0:
            candidate_points.append(get_planar_points(j = p, contours = contours, globalx_min=startingx, globaly_min = startingy, granularity= 30)) #granularity in (mm)
        p+=1



    #test to make sure list is properly shaped
    for i in range(len(candidate_points)):
        for j in range(len(candidate_points[i])):
            if len(candidate_points[i][j]) != 3:
                print("nooooo")
    results = []
    for index in range(len(candidate_points)):
        results.extend(candidate_points[index])
    return results

def plot(cube, size):

   fig = plt.figure()
   ax = fig.add_subplot(projection='3d')

   for i in range(size):
       ax.scatter(cube[i][0], cube[i][1], cube[i][2], s=10, c=1)
   plt.show()



beginning = -1000
space = .1
i = beginning
j = beginning

results = []

while i <= beginning + 30:
    while j <= beginning + 30:
        results_holder = run_heuristic(i,j)
        if len(results_holder) > len(results):
            results = results_holder
        j += space
    i += space

print("placed " + str(len(results)) + " points")
print(results)

x = []
y = []
z = []

for i in range(len(results)):
    x.append(results[i][0])
    y.append(results[i][1])
    z.append(results[i][2])

ifig = px.scatter_3d(x=x, y=y, z=z)
ifig.show()

