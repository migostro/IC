import numpy as np
import nodes as no
import random
from graphviz import Digraph

class Graph:
    def _list_num (self, list_s):
        """
        Converts a binary list of a number into the corresponding decimal number.
        Example: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0] --> 4
        :param list_s: Binary number in a list format.
        :return: Decimal number, type int.
        """
        str_s = "".join(map(str, list_s))
        int_s = int(str_s, 2)
        return int_s

    def _num_list (self, int_s):
        """
        Converts a decimal number to binary type number, then separates all the digits and puts them in a list.
        (int type values).
        :param int_s: Any integer number from 0 to 2047;
        :return: A binary list corresponding to that number expressed in 11 digits.
        Example: Converts 2 into [0, 0, 0, 0, 0, 1, 0].
        """
        n = self.num_genes
        list_s = [0 for i in range(n)]
        str_s = f'{int_s:b}'
        i = -1
        for s in str_s[::-1]:
            list_s[i] = int (s)
            i -= 1
        return np.array(list_s)
    
    def _next_state(self, actual_state, teta = []):
        if teta == []:
            teta = np.zeros([self.num_genes])
        
        actual_state_list = self._num_list(actual_state)
        next_state_list = np.zeros([len(actual_state_list)], dtype=np.int16)

        for i in range(self.num_genes):
            sum = np.inner(actual_state_list, self.M[i,:])

            if (sum-teta[i] > 0):
                next_state_list[i] = 1
            elif (sum-teta[i] < 0):
                next_state_list[i] = 0
            else:
                next_state_list[i] = actual_state_list[i]
        
        return self._list_num(next_state_list)
    
    def state_transition_list(self, teta=[]):
        D = []

        num_states = 2**self.M.shape[0]

        for actual_state in range(num_states):
            next_state = self._next_state(actual_state, teta)

            D.append([actual_state, next_state])

        return D

    def _init_vector_visited(self):
        """
            Inicializa o vetor visited, em que cada vertice terá um número inteiro associado a sua  bacia de atração a qual ele pertence
        """
        if (self.visited[0] != 0):
            return

        for i in range(self.n):
            if(self.visited[i] == 0):
                self.inicial_state.append(i)
                self.num_basins_atraction += 1
                self.states_per_basin.append(1)
                self._init_vector_visited_aux(i)
            else:
                j = self.vertice_id(i)
                self.states_per_basin[j] += 1

    def _init_vector_visited_aux(self, v):

        self.visited[v] = self.num_basins_atraction

        fathers = self.nos.fathers(v)

        for next_state in fathers:
            if(self.visited[next_state] == 0):
                self._init_vector_visited_aux(next_state)

        next_state = self.in_v[v]
        if(self.visited[next_state] == 0):
            self._init_vector_visited_aux(next_state)

    def next_state(self, state):
        return self.in_v[state]

    def get_states_per_basin(self):
        return self.states_per_basin
        
    def get_attractors(self):
        return self.attractors
    
    def vertice_id(self, v):
        """
            Retorna o id da bacia de atração que v pertence
            :param v, vertice do grafo (diagrama de estados)
            :return id do vertice
        """
        
        return self.visited[v]-1
    
    def is_states_in_same_basin(self, state1, state2):
        """
            Verifica se os estados pertencem a mesma bacia de atração
            :param estado1, do diagrama de estados
            :param estado2, do diagrama de estados

            :return True se pertencem e False caso contrario
        """
        return self.vertice_id(state1) == self.vertice_id(state2)

    def attractors_of(self, v):
        """
            Encontra os atratores de um dado vertice em O(1)
            :param um vértice v do grafo
            :return uma lista de atratores que o vertice v é atraido 
        """
        if(self.attractors == []):
            self.construct_attractors()

        ind = self.vertice_id(v)

        return self.attractors[ind]

    def find_attractors(self, v):
        """
            Encontra os atratores de um dado vertice em O(n)
            :param um vértice v do grafo
            :param o tamanho n do grafo
            :return uma lista de atratores que o vertice v é atraido 
        """
        visited_aux = np.zeros(self.n, dtype=np.uint32)
        
        current_state = v
        next_state = self.in_v[v]
        while(visited_aux[current_state] != 1):
            visited_aux[current_state] = 1
            current_state = next_state
            next_state = self.in_v[current_state]

        attractors = [current_state]

        first_state_attractor = current_state
        while(first_state_attractor != next_state):
            attractors.append(next_state)
            current_state = next_state
            next_state = self.in_v[current_state]

        return attractors
        # return self.find_attractors_aux(v, visited_aux)

    def find_attractors_aux(self, v, visited_aux):

        if(visited_aux[v] == 0):
            visited_aux[v] = 1
            next_state = self.in_v[v]
            return self.find_attractors_aux(next_state, visited_aux)
        else:
            attractors = [v]
            
            next_state = self.in_v[v]

            while(next_state != v):
                visited_aux[next_state] = 1
                attractors.append(next_state)
                next_state = self.in_v[v]
                if visited_aux[next_state] == 1:
                    v = next_state
                    attractors = [v]
                    next_state = self.in_v[v]

            return attractors

    def construct_attractors(self):
        """
            Constroi a lista de atratores, de forma a deixar a procura dos atratores de um dado vertice em O(1)
            :param o tamanho n do grafo
        """
        if(self.visited[0] == 0):
            self._init_vector_visited()

        i = 0
        unseen_basins = np.ones(self.num_basins_atraction)
        num_of_unseen_basins = self.num_basins_atraction

        for i in range(self.num_basins_atraction):
            self.attractors.append([])
        
        for i in range(len(self.inicial_state)):
            state = self.inicial_state[i]

            att = self.find_attractors(state)
            self.attractors[i] = att


    def calculate_w_for_s(self, v):
        """
            Constroi os vetores sum e dist para o calculo de w
            :param um inteiro v que representa um vertice
        """
        fathers = self.nos.fathers(v)
        for u in fathers:
            self.sum[u] = self.nos.get_flow_amount(u) + self.sum[v]
            self.dist[u] = self.dist[v] + 1

            self.calculate_w_for_s(u)

    def calculate_w(self):
        """
            Constroi o vetore w a partir de sum e dist
        """

        if len(self.attractors) == 0:
            self.construct_attractors()

        i = 0
        unseen_basins = np.ones(self.num_basins_atraction)
        num_of_unseen_basins = self.num_basins_atraction
        
        while(num_of_unseen_basins > 0):
            num_basin = self.visited[i]-1
            
            if(unseen_basins[num_basin] == 1):
                unseen_basins[num_basin] = 0
                num_of_unseen_basins -= 1

                attractors = self.attractors_of(i)
                for attractor in attractors:
                    fathers = self.nos.fathers(attractor)

                    for father in fathers:
                        if not father in attractors:
                            self.sum[father] = self.nos.get_flow_amount(father)
                            self.dist[father] = 1
                            self.calculate_w_for_s(father)

            i += 1

        for i in range(self.n):
            if(self.dist[i] != 0):
                self.w[i] = self.sum[i]/self.dist[i]
            else:
                self.w[i] = 0

    def calculate_W(self):
        if(self.w[0] == 0):
            self.calculate_w()

        return np.sum(self.w)/len(self.w)

    def take_path_to_atraction(self, state):
        """
            :param stado de que começa o caminho
            :return o caminho do estado até seu atrator
        """

        path = []
        current = state
        basin_of_att = self.attractors_of(state)

        while(current != basin_of_att[0]):
            path.append(current)
            current = self.in_v[current]
        path.append(current)
        return path

    def M_to_W(self, M):
        """
            Calcula o valor W a partir da matriz de regulação M
            :param M, matriz de regulação
            :param names, nome de cada gene
            :return W
        """

        D_transitions = self.state_transition_list()

        out_v = []
        in_v = []

        # converte a lista binária de transições de estados de lista para uma lista de inteiro
        for i in range(len(D_transitions)):
            out_num = D_transitions[i][0]
            in_num  = D_transitions[i][1]
            out_v.append(out_num)
            in_v.append(in_num)
        n = len(out_v)
        graph = Graph(out_v, in_v, n)

        graph.calculate_w()
        W = graph.W()

        return W
        
    def draw(self):
        
        g = Digraph('G')
        # g.attr(size='120')
        n = self.M.shape[0]
    
        names = [str(i) for i in range(n)]
        
        for i in range(n):
           for j in range(n):
             if self.M[i][j] < 0:
               g.edge (str(names[j]),str(names[i]), arrowhead = "tee", color="red")
             if self.M[i][j] > 0:
               g.edge (str(names[j]),str(names[i]))
        return g
        
    def draw_STG(self, engine='sfdp'):
    
        g = Digraph('G', engine=engine)
        # g.attr(size='9')
        
        n_states = len(self.in_v)
        
        for i in range(n_states):
            out_state = str(i) 
            in_state = str(self.in_v[i])
    
            g.edge(out_state, in_state)
        
        return g
    
    def dist_to_attractor(self, state):
        dist = 0
        while (not state in self.attractors_of(state)):
            dist += 1
            state = self.next_state(state)
        return dist
    
    def attractors_of_biggest_basin(self):
        """
            :param graph, do tipo Graph ou similares
            :return os atratores da maior bacia de atração
        """

        bigger_basin = max(self.states_per_basin)

        index = self.states_per_basin.index(bigger_basin)
        attractors_of_bigger_basin = self.attractors[index]

        return attractors_of_bigger_basin, bigger_basin
    
    def fathers(this, i):
        """
            :return os fathers do estado
        """
        return this.nos.fathers(i)