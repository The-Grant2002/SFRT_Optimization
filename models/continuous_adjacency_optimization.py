from gurobipy import *
import matplotlib.pyplot as plt
import plotly.express as px
import pickle
import numpy as np
from scipy.optimize import minimize, rosen, rosen_der, NonlinearConstraint
import time
import threading

class OptimizationTimeoutException(Exception):
    pass
def optimization(nodes, adjacency):

    def optimize_with_timeout(func, x0, bounds=None, constraints=None, method='SLSQP', time_limit=10):
        """ Run optimization with a time limit. """

        result = {'success': False, 'message': 'Optimization not completed in time.'}
        result_lock = threading.Lock()

        def run_optimization():
            nonlocal result
            start_time = time.time()
            def callback(x):
                nonlocal result
                if time.time() - start_time > time_limit:
                    raise OptimizationTimeoutException()
            try:
                res = minimize(func, x0, bounds=bounds, constraints=constraints, method=method, callback=callback)
                with result_lock:
                    result.update({'success': res.success, 'message': res.message, 'x': res.x, 'fun': res.fun})
            except OptimizationTimeoutException:
                with result_lock:
                    result.update({'success': False, 'message': 'Time limit exceeded'})

        thread = threading.Thread(target=run_optimization)
        thread.start()
        thread.join(timeout=time_limit)

        if thread.is_alive():
            print('time limit exceeded. ending optimization')

            result.update({'success': False, 'message': 'Time limit exceeded'})

        return result


    a = np.identity(len(nodes), dtype = int) - adjacency
    a = a.tolist()
    objective = lambda x: (-1*sum(x[i]*adjacency[i][j]*x[j] for i in range(len(nodes)) for j in range(len(nodes))))
    x0 = [0]*len(nodes)
    con = lambda x: x**2 - x
    nlc = NonlinearConstraint(con,0,0)
    time_limit = 10

    result = optimize_with_timeout(objective, x0, constraints=nlc, time_limit=time_limit)

    print(result)

def plot(cube, size):

   fig = plt.figure()
   ax = fig.add_subplot(projection='3d')

   for i in range(size):
       ax.scatter(cube[i][0], cube[i][1], cube[i][2], s=10, c=1)
   plt.show()

if __name__ == '__main__':

    node_dict = {}
    with open("../data/node_data.pkl", 'rb') as openfile:
        node_dict = pickle.load(openfile)

    adjacency = []
    with open("../data/adjacency_matrix.pkl", 'rb') as openfile:
        adjacency = pickle.load(openfile)

    node_index = optimization(node_dict,adjacency)
    exit()
    optimal_nodes = []

    for i in range(len(node_index)):
       node_index[i] = int(node_index[i])
       if node_index[i] == 1.0:
           optimal_nodes.append(node_dict.get(str(i)))



    print(node_index)
    print(optimal_nodes)
    print(len(optimal_nodes))
    plot(optimal_nodes,len(optimal_nodes))
    x = []
    y = []
    z = []
    for i in range(len(optimal_nodes)):
        x.append(optimal_nodes[i][0])
        y.append(optimal_nodes[i][1])
        z.append(optimal_nodes[i][2])

    ifig = px.scatter_3d(x=x, y=y, z=z)
    ifig.show()
