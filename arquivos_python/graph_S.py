import numpy as np
from graph import Graph
import math

class Graph_S(Graph):
    """
        Utiliza dois vetores para iniciar o grafo de transição de estados
    """

    def __init__(self, out_v, in_v):
        # super().__init__()
        self.n = len(out_v)
        self.num_genes = math.log2(self.n)
        self.in_v = np.zeros(self.n, dtype=np.uint32)
        # self.nos = no.Nodes(self.n, seed)
        self.nos.calcula_fluxo()
        self.vetor_pesos = np.zeros(self.n, dtype=np.uint32)
        for i in range(self.n):
            self.in_v[i] = in_v[i]
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
        self.w()