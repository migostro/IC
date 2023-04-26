class Regulation:
    def __init__(self, M):
        self.M = M
        self._positive_adj()
        self._negative_adj()

    def _positive_adj(self):
        self.positive_adj = []

        for i in range(self.M.shape[0]):
            adjs = []
            for j in range(self.M.shape[1]):
                if (self.M[i, j] == 1):
                    adjs.append(j)
            self.positive_adj.append(adjs)

    def _negative_adj(self):
        self.negative_adj = []

        for i in range(self.M.shape[0]):
            adjs = []
            for j in range(self.M.shape[1]):
                if (self.M[i, j] == -1):
                    adjs.append(j)
            self.negative_adj.append(adjs)

    def get_positive_adj(self, gene):
        return self.positive_adj(gene)

    def get_negative_adj(self, gene):
        return self.negative_adj(gene)
    
    def positive_leaves(self):
        """
            Retorna os genes que são folhas olhando apenas os arcos positivos
        """
        leaves = []
        for gene in range(self.M.shape[0]):
            if self.positive_adj[gene] == []:
                leaves.append(gene)
        return leaves