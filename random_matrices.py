import random
import numpy as np
from graph import Graph

class Random_matrices:
    def __init__(self, size, number_of_matrices, seed):
        random.seed(seed)
        self.matrices = self.create_matrices(number_of_matrices, size)

    def _take_position_of_matrix(vector_of_nonzeros, n):
        '''
            Pega uma posição da matriz que é zero e muda o vector_of_nonzeros
            :param vector_of_nonzeros, vetor que guarda as posições da matriz que ainda são zero
            :n número de linhas da matriz
            :return pos_i, pos_j onde a matriz[pos_i, pos_j] == 0
        '''

        ind = random.randrange(len(vector_of_nonzeros)-1)
        pos = vector_of_nonzeros[ind]
        pos_i = pos // n
        pos_j = pos % n

        # deleta a posição que foi utilizada da lista
        vector_of_nonzeros[ind] = vector_of_nonzeros[-1]
        vector_of_nonzeros.pop()

        return pos_i, pos_j


    def create_matrix(self, matrix_size, num_positive, num_negative, genes_start=4):
        '''
            Cria uma matriz com num_positive de 1's e num_negative de -1's
            :param matrix_size, [num_columns, num_lines] onde num_columns == num_lines
            :param num_positive, quantidade de numeros 1's na matriz
            :param num_negative, quantidade de numeros -1's na matriz
            :param genes_start, quantidade de genes iniciados pelo primeiro gene
            :return matriz criada aleatoriamente com os parâmetros passados, onde o gene 0 é o que inicia o processo (não há arcos que têm ele como target)
        '''
        matrix = np.zeros(matrix_size)
        
        n = matrix_size[0]

        # keep the positions of the matrix that are zeros
        # vector_of_zeros = [i for i in range(matrix[0]+1, matrix_size[0]*matrix_size[1])]
        vector_of_zeros = []
        for i in range(matrix_size[0]+1, matrix_size[0]*matrix_size[1]):
            if(i%matrix_size[0] != 0):
                vector_of_zeros.append(i)

        genes_that_will_be_init_by_first_gene = [i for i in range(1, matrix_size[0])]
        # gene 0 "desliga" após iniciar a cadeia
        matrix[0, 0] = -1

        # genes que o gene 0 ativa
        for i in range(genes_start):
            ind = random.randrange(len(genes_that_will_be_init_by_first_gene)-1)

            pos = genes_that_will_be_init_by_first_gene[ind]

            # deleta a posição que foi utilizada da lista
            genes_that_will_be_init_by_first_gene[ind] = genes_that_will_be_init_by_first_gene[-1]
            genes_that_will_be_init_by_first_gene.pop()

            matrix[0, pos] = 1


        for i in range(num_positive):
            pos_i, pos_j = self._take_position_of_matrix(vector_of_zeros, n)
            matrix[pos_i, pos_j] = 1

        for i in range(num_negative):
            pos_i, pos_j = self._take_position_of_matrix(vector_of_zeros, n)
            matrix[pos_i, pos_j] = -1

        matrix = Graph.connected_M(matrix)

        return np.transpose(matrix)

    def create_matrices(self, num_matrices, num_nodes, non_zero_proportion, positive_proportion):
        zero_numbers = (num_nodes-1)*(num_nodes-1)
        non_zero = zero_numbers*non_zero_proportion
        num_positive = int(non_zero*positive_proportion)
        num_negative = int(non_zero*(1-positive_proportion))

        matrices = []

        for i in range(num_matrices):
            matrices.append(self.create_matrix([num_nodes, num_nodes], num_positive, num_negative))

        return matrices