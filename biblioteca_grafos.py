# biblioteca_grafos.py

from collections import defaultdict, deque

class Grafo: 
    def __init__ (self, representacao='lista'): 
        self.representacao = representacao 
        self.vertices = set() 
        self.arestas = [] 
        self.lista_adj = defaultdict(list) 
        self.matriz_adj = []

    def carregar_arquivo(self, caminho):
        with open(caminho, 'r') as f:
            linhas = f.readlines()
        n = int(linhas[0])  # número total de vértices declarado
        self.arestas = []
        self.vertices = set()
        for linha in linhas[1:]:
            if not linha.strip():
                continue
            dados = linha.strip().split()
            if len(dados) < 2:
                continue
            u, v, *peso = dados
            u, v = int(u), int(v)
            p = float(peso[0]) if peso else 1
            self.arestas.append((u, v, p))
            self.lista_adj[u].append((v, p))
            self.lista_adj[v].append((u, p))
            self.vertices.update([u, v])
        # garantir inclusão dos vértices isolados
        while len(self.vertices) < n:
            for i in range(1, n+1):
                self.vertices.add(i)
        if self.representacao == 'matriz':
            max_v = max(self.vertices) + 1
            self._construir_matriz(max_v)

    def _construir_matriz(self, n):
        self.matriz_adj = [[0]*n for _ in range(n)]
        for u, v, p in self.arestas:
            self.matriz_adj[u][v] = p
            self.matriz_adj[v][u] = p

    def salvar_info_grafo(self, caminho):
        n = len(self.vertices)
        m = len(self.arestas)
        graus = [len(self.lista_adj[v]) for v in self.vertices]
        grau_medio = sum(graus)/n
        dist_grau = defaultdict(int)
        for g in graus:
            dist_grau[g] += 1
        with open(caminho, 'w') as f:
            f.write(f"Numero de vertices: {n}\n")
            f.write(f"Numero de arestas: {m}\n")
            f.write(f"Grau medio: {grau_medio:.2f}\n")
            f.write("Distribuicao de grau:\n")
            for g in sorted(dist_grau):
                f.write(f"Grau {g}: {dist_grau[g]} vertices\n")

    def busca_largura(self, inicio, caminho_saida):
        visitado = {inicio}
        fila = deque([inicio])
        pai = {inicio: None}
        nivel = {inicio: 0}
        while fila:
            u = fila.popleft()
            for v, _ in self.lista_adj[u]:
                if v not in visitado:
                    visitado.add(v)
                    pai[v] = u
                    nivel[v] = nivel[u] + 1
                    fila.append(v)
        with open(caminho_saida, 'w') as f:
            for v in sorted(pai):
                f.write(f"Vertice: {v}, Pai: {pai[v]}, Nivel: {nivel[v]}\n")

    def busca_profundidade(self, inicio, caminho_saida):
        visitado = set()
        pai = {}
        nivel = {}
        def dfs(u, n):
            visitado.add(u)
            nivel[u] = n
            for v, _ in sorted(self.lista_adj[u]):
                if v not in visitado:
                    pai[v] = u
                    dfs(v, n+1)
        pai[inicio] = None
        dfs(inicio, 0)
        with open(caminho_saida, 'w') as f:
            for v in sorted(pai):
                f.write(f"Vertice: {v}, Pai: {pai[v]}, Nivel: {nivel[v]}\n")

    def componentes_conexos(self, caminho_saida):
        visitado = set()
        componentes = []
        for v in sorted(self.vertices):
            if v not in visitado:
                comp = []
                fila = deque([v])
                visitado.add(v)
                while fila:
                    u = fila.popleft()
                    comp.append(u)
                    for w, _ in self.lista_adj[u]:
                        if w not in visitado:
                            visitado.add(w)
                            fila.append(w)
                componentes.append(sorted(comp))
        componentes.sort(key=lambda c: len(c), reverse=True)
        with open(caminho_saida, 'w') as f:
            f.write(f"Numero de componentes: {len(componentes)}\n")
            for i, c in enumerate(componentes, 1):
                f.write(f"Componente {i} (tam={len(c)}): {' '.join(map(str, c))}\n")