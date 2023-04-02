# from graph import Graph
from graph_M import Graph_M
import numpy as np

def vector():
    return np.zeros([5])

def grow_vector_size(vector, n):
    """
        Aumenta o tamanho do vetor para n+1
        :param vector, vetor que deseja aumentar
        :param n, tamanho que o vetor deve receber
        :return vector(n+1) 
    """
    if (vector.shape[0] < n):
        new_vector = np.zeros([n+1])
        m = vector.shape[0]
        new_vector[0:m] = vector
        return new_vector
    return vector

def add_in_vector(vector, val):
    """
        Soma +1 em vector[val]
        :param vector, vetor que fará a soma
        :param val, posição do vetor que será somado
    """
    if (val >= vector.size()):
        grow_vector_size(vector, val)
    vector[val] += 1

def matrix():
    return np.zeros([5, 5])

def grow_matrix_size(matrix, n):
    """
        Aumenta o tamanho da matriz para n+1 x n+1
        :param matriz, vetor que deseja aumentar
        :param n, tamanho que o vetor deve receber
        :return matriz(n+1, n+1) 
    """
    if(matrix.shape[0] <= n):
        new_matrix = np.zeros([n+1, n+1])
        m = matrix.shape[0]
        new_matrix[0:m, 0:m] = matrix
        return new_matrix
    return matrix

def add_in_matrix(matrix, val_row, val_col):
    """
        Soma +1 em matrix[val_row, val_col]
        :param matrix, vetor que fará a soma
        :param val_row, posição da matriz que será somado
        :param val_col, posição da matriz que será somado
    """
    if(matrix.shape[0] <= val_col):
        matrix = grow_matrix_size(matrix, val_col)
    if (matrix.shape[1] <= val_row):
        matrix = grow_matrix_size(matrix, val_row)
    matrix[val_row, val_col] += 1

def histograms(graphs, states, attractors):
    """
        Calcula a frequencia de algumas propriedades do diagrama de estados
        :param graphs, lista de grafos (pode ser do tipo Graph e derivados)
        :param states, lista de listas de estados que supostamente são o inicio do caminho central
        :param attractors, lista de listas de atratores das maiores bacias de atração de cada graph

        :return frequencia de ocorrencias das distancias até o atrator; das ocorrencias das quantidades de atratores que possuem seus states na mesma bacia de atração
    """
    matrix_of_dists = matrix()
    matrix_same_basin = matrix()

    for i, graph in enumerate(graphs):
        num_same_basin = 0
        attractors_size = len(states[i])
        # num_not_in_same_basin = 0
        for j in range(len(states[i])):
            print(j)
            print(len(states[i]), len(attractors[i]))
            if (graph.is_states_in_same_basin(states[i][j], attractors[i][j])):
                num_same_basin += 1
                
                dist = graph.dist_to_attractor(states[i][j])
                add_in_matrix(matrix_of_dists, dist, attractors_size)

        add_in_matrix(matrix_same_basin, num_same_basin, attractors_size)
            

    return matrix_of_dists, matrix_same_basin


############################################### TESTES ################################################

def histogram_test1():
    matriz_yeast = np.array([
    [-1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0, -1,  0 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0, -1,  0 ],
    [ 0,  0,  1, -1,  0,  0,  0,  0,  0,  0,  0 ],
    [ 0,  0,  0, -1,  0,  0,  1, -1,  0, -1,  0 ],
    [ 0,  0,  0,  0,  0, -1,  1,  0,  0, -1,  1 ],
    [ 0,  0,  0,  0,  0,  0, -1,  0,  0,  1,  1 ],
    [ 0,  1,  0,  0,  0,  0, -1,  0, -1,  0,  0 ],
    [ 0,  0,  0, -1,  0,  1,  1, -1,  0, -1,  0 ],
    [ 0,  0,  0,  0, -1,  0, -1,  1, -1,  0,  1 ],
    [ 0,  0,  0,  0,  0,  0,  0,  1,  0,  1, -1 ]], dtype=int)
    graph = Graph_M(matriz_yeast)
    graphs = [graph]

    print(histograms(graphs, [[1735]], [[564]]))