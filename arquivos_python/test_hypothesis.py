from graph import Graph
import numpy as np

def vector():
    return np.zeros([5])

def grow_vector_size(vector, n):
    if (vector.shape[0] < n):
        new_vector = np.zeros([n+1])
        m = vector.shape[0]
        new_vector[0:m] = vector
        return new_vector
        # return np.resize(frequencie_of_positive_hipotesis, [n, n])
    return vector

def grow_matrix_size(matrix, n):
    if(matrix.shape[0] < n):
        new_matrix = np.zeros([n, n])
        m = matrix.shape[0]
        new_matrix[0:m, 0:m] = matrix
        return new_matrix
        # return np.resize(frequencie_of_positive_hipotesis, [n, n])
    return matrix

def histogram_dist_to_attractor(graphs, states):
    """
        recebe uma lista de estados e joga no histograma a distancia de cada estado ao seu atrator
        :param states, estados que devem ser testados
    """
    vec = vector()
    for i in range(graphs):
        dist = graphs[i].dist_to_attractor(states[i])
        if (dist >= vec.size()):
            grow_vector_size(vec, dist)
            vec[dist] += 1

    return vec