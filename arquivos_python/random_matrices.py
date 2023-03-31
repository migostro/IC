import random
import numpy as np

class Random_matrices:
    def __init__(self, number_of_matrices, num_nodes, seed=0, non_zero_proportion = 0.6, positive_proportion=0.3):
        random.seed(seed)
        self.matrices = self.create_matrices(number_of_matrices, num_nodes, non_zero_proportion, positive_proportion)

    def _take_position_of_matrix(self, vector_of_nonzeros, n):
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
    
    def connected_M(self, M):
        """
            Verifica se a matriz M representa um grafo conexo
            :param M, matriz de adjacencia
            :return M caso a matriz represente um grafo conexo, ou M com modificações que a deixe conexa
        """
        n = M.shape[0]
        roots = []

        visited = np.zeros(n)
        queue = []

        for i in range(n):
            # dfs iterativa
            if (visited[i] == 0):
                roots.append(i)
                queue.append(i)
                while (len(queue) > 0):
                    current = queue[-1]
                    queue.pop()

                    visited[current] = 1

                    for j in range(n):
                        if (M[i,j] != 0 and visited[j] == 0):
                            queue.append(j)
                            visited[j] = 1
                        if (M[j,i] != 0 and visited[i] == 0):
                            queue.append(i)
                            visited[i] = 1
        
        reg = 1
        # roots[0] = roots[-1]
        roots.pop()
        for i in range(len(roots)):
            u = roots[i-1]
            v = roots[i]
            M[u, v] = reg
            reg = reg*(-1)
        
        return M


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
        for i in range(0, matrix_size[0]*matrix_size[1]-matrix_size[0]):
            if(i%n != n-1):
                vector_of_zeros.append(i)

        genes_that_will_be_init_by_first_gene = [i for i in range(0, n-1)]
        # gene 0 "desliga" após iniciar a cadeia
        matrix[n-1, n-1] = -1

        # genes que o gene inicial ativa
        for i in range(genes_start):
            ind = random.randrange(len(genes_that_will_be_init_by_first_gene)-1)

            pos = genes_that_will_be_init_by_first_gene[ind]

            # deleta a posição que foi utilizada da lista
            genes_that_will_be_init_by_first_gene[ind] = genes_that_will_be_init_by_first_gene[-1]
            genes_that_will_be_init_by_first_gene.pop()

            matrix[n-1, pos] = 1


        for i in range(num_positive):
            pos_i, pos_j = self._take_position_of_matrix(vector_of_zeros, n)
            matrix[pos_i, pos_j] = 1

        for i in range(num_negative):
            pos_i, pos_j = self._take_position_of_matrix(vector_of_zeros, n)
            matrix[pos_i, pos_j] = -1

        matrix = self.connected_M(matrix)

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