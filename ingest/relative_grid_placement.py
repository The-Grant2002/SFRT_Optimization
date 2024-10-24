'''

helper functions and a function that takes a list of (x,y) pairs of ordered border points and outputs all internal points
Works for 2D slices

'''

from matplotlib import pyplot as plt
import random
import math

def plot2d(points):
    '''
    takes points, plots 2d slice
    :param points: (x,y) list of points:
    :return: none
    '''
    x = []
    y = []
    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][1])
    plt.scatter(x,y)
    plt.show()
def create_points(radius, num):
    '''
    Creates circular border points for testing purposes
    :param radius: radius of shape
    :param num: number of border points
    :return: list of (x,y) border points
    '''
    nodes = []
    i = 0
    while i < 2*math.pi:
        nodes.append([radius*math.cos(i), radius*math.sin(i)])
        i += (2*math.pi)/num
    return nodes

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

def get_x_values(xmin,xmax, granularity, init):
    '''
    Takes a domain and returns a list of all x values within that domain with a given granularity
    :param xmin: int: lowest x value
    :param xmax: int: max x value
    :param granularity: distance between points
    :return: list of all points between max and min
    '''
    x = []
    i = math.ceil(xmin)
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

def get_y_values(ymin,ymax, granularity, init):
    '''
    Takes a range and returns a list of all y values within that range with a given granularity
    :param ymin: int: lowest y value
    :param ymax: int: max y value
    :param granularity: distance between points
    :return: list of all points between max and min
    Yes, this is the same as get_x_values()
    '''
    y = []
    i = math.ceil(ymin)
    while i <= ymax:
        if i >= ymin and i <= ymax:
            y.append(i)
        i += granularity
    return y




############   RUN       ###########




def get_candidate_points(points, test_radius = 10, test_boundary_num = 17, granularity = .5, plot = True, test_data = False):
    '''
    Function that takes points and returns all internal points

    :param points: Set of points that defines a shape   #######   POINTS MUST BE ORDERED     ##########
    :param test_radius: for testing, radius of created circle
    :param test_boundary_num: for testing, number of points in created circle
    :param granularity: distance between created points
    :param plot: True if you want to plot individual slices, will probably overload HTML if you run on too many slices
    :param test_data: True if you want to use created circle, ideal convex data
    :return: all internal points - list of (x,y) pairs
    '''
    #create and plot points, test
    if test_data == True:
        points = create_points(test_radius, test_boundary_num)
        plot2d(points)


    #get the x bounds
    xmin, xmax = get_x_boundary(points)

    init_val = -1000
    #get x values
    x_list = get_x_values(xmin, xmax, granularity, init_val)

    #get valid y range
    y_bounds = []
    y_list = []

    #get bounds of y values ######    ASSUMES CONVEXITY   ############
    for i in range(len(x_list)):
        y_bounds.append(get_y_bounds(x_list[i], points))

        if len(y_bounds[i]) == 2: #if shape at x value is convex combination of points (only 2 points for an x)
            ymin = min(y_bounds[i])
            ymax = max(y_bounds[i])
            y_list.append(get_y_values(ymin, ymax, granularity, init_val))   ## Get y values for each x
        elif len(y_bounds[i]) == 1: #if there is only a single point for an x, just add that value
            y_list.append(y_bounds[i])
        elif len(y_bounds[i]) % 2 == 0 and not(len(y_bounds[i]) == 2): #For an even number of points with convexity, assume that there is a hole
            y_subset = []
            y_holder = []
            y_bounds[i] = sorted(y_bounds[i])
            for j in range(len(y_bounds[i])):
                if j % 2 == 0:
                    y_subset.append(get_y_values(min(y_bounds[i][j], y_bounds[i][j+1]), max(y_bounds[i][j], y_bounds[i][j+1]), granularity, init_val))

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
                    y_subset.append(get_y_values(min(y_bounds[i][j], y_bounds[i][j+1]), max(y_bounds[i][j], y_bounds[i][j+1]), granularity, init_val))
            for j in range(len(y_subset)):
                y_holder.extend(y_subset[j])
            y_list.append(y_holder)
        else:
            raise("NOOO Theres a weird number of points!") #really shouldn't ever happen unless something is very wrong

    #create (x,y) coordinate pairs for all internal values
    coordinates = []

    for i in range(len(x_list)):
        for j in range(len(y_list[i])):
            coordinates.append([x_list[i], y_list[i][j]])

    if plot == True:
        plot2d(coordinates) #plot coordinates

    return coordinates



