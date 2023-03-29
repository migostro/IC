import numpy as np
import nodes as no
from tbn import tbn
import random
from graphviz import Digraph
from graph import Graph


class Graph_M(Graph):
    """
        Utiliza uma matriz n x n para gerar o grafo e a transição de estados
    """

    def __init__(self, M):
        # super().__init__(out_v, in_v, n, seed)
        out_v, in_v = self.M_to_transitions_states(M)
        self.n = 2**(M.shape[0])

        self.in_v = in_v
        self.nos = no.Nodes(out_v, in_v, self.n)
        self.nos.calcula_fluxo()
        self.vetor_pesos = np.zeros(self.n, dtype=np.uint32)
        for i in range(self.n):
            self.vetor_pesos[i] = self.nos.get_flow_amount(i)

        # CÓDIGO DUPLICADO, PENSAR EM UMA PADRÃO MELHOR PARA USAR
        self.num_basins_atraction = 0
        # visited[i] guarda a qual bacia de atração o vertice i pertence. 1 <= visited[i] <= num_basins_atraction
        self.visited = np.zeros(self.n, dtype=np.uint32)
        self.states_per_basin = []
        self.attractors = []
        # sum[i] é a menor soma dos pesos das arestas do vertice i até um de seus atratores
        self.sum = np.zeros(self.n, dtype=np.uint32)
        # dist[i] é a menor quantidade de arestas do vertice i até um de seus atratores
        self.dist = np.zeros(self.n, dtype=np.uint32)
        
        # estados iniciais de cada bacia de atração
        self.inicial_state = []
        self.vector_w = np.zeros(self.n, dtype=np.float64)
        
        self._init_vector_visited()
        self.construct_attractors()


    def M_to_transitions_states(self, M):
        names = np.array([str(i) for i in range(M.shape[0])])
        n = 2**M.shape[0]
        out_v = np.zeros(n, dtype=np.uint32)
        in_v = np.zeros(n, dtype=np.uint32)
        R = tbn(M,names)
        
        D = R.state_transition_list()
        
        for i in range(len(D)):
            out_v[i] = R._list_num(D[i][0])
            in_v[i] = R._list_num(D[i][1])
            
        return out_v, in_v