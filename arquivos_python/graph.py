import numpy as np
import nodes as no
from tbn import tbn
import random
from graphviz import Digraph

class Graph:
    """
        Inicializa as variáveis de acordo o tipo de digrafo

        tipo 1 (pré-definido)
        :param out_v, vertices que estão saindo as arestas
        :param in_v, vertices que as arestas estão entrando
        :param n, numero de vertices do digrafo

        tipo 2 (arvore aleatoria)
        :param n, numero de vertices do digrafo
        :param seed, seed utilizada para a aleatorização
    """
    # def init(self):
        # digrafo pré definido
        # if(seed == -1):
        #     self.n = n
        #     self.in_v = in_v
        #     self.nos = no.Nodes(out_v, in_v, n)
        #     self.nos.calcula_fluxo()
        #     self.vetor_pesos = np.zeros(n, dtype=np.uint32)
        #     for i in range(n):
        #         self.vetor_pesos[i] = self.nos.get_flow_amount(i)
        # # digrafo aleatório
        # else:
        #     self.n = n
        #     self.in_v = np.zeros(n, dtype=np.uint32)
        #     self.nos = no.Nodes(n, seed)
        #     self.nos.calcula_fluxo()
        #     self.vetor_pesos = np.zeros(n, dtype=np.uint32)
        #     for i in range(n):
        #         self.in_v[i] = self.nos.adj(i)[0][1]
        #         self.vetor_pesos[i] = self.nos.get_flow_amount(i)  

        # self.num_basins_atraction = 0
        # # visited[i] guarda a qual bacia de atração o vertice i pertence. 1 <= visited[i] <= num_basins_atraction
        # self.visited = np.zeros(self.n, dtype=np.uint32)
        # self.states_per_basin = []
        # self.attractors = []
        # # sum[i] é a menor soma dos pesos das arestas do vertice i até um de seus atratores
        # self.sum = np.zeros(self.n, dtype=np.uint32)
        # # dist[i] é a menor quantidade de arestas do vertice i até um de seus atratores
        # self.dist = np.zeros(self.n, dtype=np.uint32)
        
        # # estados iniciais de cada bacia de atração
        # self.inicial_state = []
        # self.vector_w = np.zeros(self.n, dtype=np.float64)
        
        # self._init_vector_visited()
        # self.construct_attractors()

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

    def w(self):
        """
            Constroi o vetore w a partir de sum e dist
            :param um inteiro v que representa um vertice
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
                self.vector_w[i] = self.sum[i]/self.dist[i]
            else:
                self.vector_w[i] = 0

    def W(self):
        if(self.vector_w[0] == 0):
            self.w()

        return np.sum(self.vector_w)/len(self.vector_w)
    """
        :param stado de que começa o caminho
        :return o caminho do estado até seu atrator
    """
    def take_path_to_atraction(self, state):
        #if(self.visited[0] == 0):
        #    self._init_vector_visited()
        path = []
        current = state
        basin_of_att = self.attractors_of(state)

        while(current != basin_of_att[0]):
            path.append(current)
            current = self.in_v[current]
        path.append(current)
        return path

    # def random_M(n, positive_chance, negative_chance):
    #     """
    #         Cria uma matriz de regulação
    #         :param n, numero de colunas/linhas da matriz
    #         :param positive_chance, a chance de uma ocorrência de um 1
    #         :param negative_chance, a chance de uma ocorrência de um -1
    #         :return uma matriz de regulação
    #     """
    #     M = np.zeros([n,n])

    #     for i in range(n):
    #         for j in range(n):
    #             choice = random.random()

    #             if choice <= positive_chance:
    #                 M[i,j] = 1
    #             elif choice >= 1 - negative_chance:
    #                 M[i,j] = -1
    #     return connected_M(M)

    def M_to_W(self, M):
        """
            Calcula o valor W a partir da matriz de regulação M
            :param M, matriz de regulação
            :param names, nome de cada gene
            :return W
        """

        names = [str(i) for i in range(M.shape[0])]
        
        R = tbn(M, names)

        D_transitions = R.state_transition_list()

        out_v = []
        in_v = []

        # converte a lista binária de transições de estados de lista para uma lista de inteiro
        for i in range(len(D_transitions)):
            out_num = R._list_num(D_transitions[i][0])
            in_num  = R._list_num(D_transitions[i][1])
            out_v.append(out_num)
            in_v.append(in_num)
        n = len(out_v)
        graph = Graph(out_v, in_v, n)

        graph.w()
        W = graph.W()

        return W
        
    def draw(self, M):
        
        g = Digraph('G')
        # g.attr(size='120')
        n = M.shape[0]
    
        names = [str(i) for i in range(n)]
        
        for i in range(n):
           for j in range(n):
             if M[i][j] < 0:
               g.edge (str(names[j]),str(names[i]), arrowhead = "tee", color="red")
             if M[i][j] > 0:
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