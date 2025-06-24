from collections import defaultdict, deque
import heapq

class Grafo:
    def __init__(self, representacao='lista'):
        # Inicializa a estrutura do grafo
        self.representacao = representacao
        self.vertices = set()
        self.arestas = []
        self.lista_adj = defaultdict(list)
        self.matriz_adj = []

    def carregar_arquivo(self, caminho):
        # Carrega grafo a partir de arquivo
        with open(caminho, 'r') as f:
            linhas = f.readlines()

        n = int(linhas[0])  # Número de vértices esperado
        self.arestas.clear()
        self.vertices.clear()
        self.lista_adj.clear()

        # Processa cada linha de aresta
        for linha in linhas[1:]:
            dados = linha.strip().split()
            if len(dados) < 2:
                continue

            u, v, *peso = map(float, dados)
            u, v = int(u), int(v)
            p = peso[0] if peso else 1.0  # Peso padrão = 1.0

            self.arestas.append((u, v, p))
            self.lista_adj[u].append((v, p))
            self.lista_adj[v].append((u, p))
            self.vertices.update([u, v])

        # Garante que todos os vértices esperados estão presentes
        while len(self.vertices) < n:
            for i in range(1, n + 1):
                self.vertices.add(i)

        if self.representacao == 'matriz':
            self._construir_matriz(max(self.vertices) + 1)

    def _construir_matriz(self, n):
        # Constrói matriz de adjacência
        self.matriz_adj = [[0] * n for _ in range(n)]
        for u, v, p in self.arestas:
            self.matriz_adj[u][v] = p
            self.matriz_adj[v][u] = p

    def salvar_info_grafo(self, caminho):
        # Salva informações básicas sobre o grafo
        n = len(self.vertices)
        m = len(self.arestas)
        graus = [len(self.lista_adj[v]) for v in self.vertices]
        grau_medio = sum(graus) / n

        dist_grau = defaultdict(int)
        for grau in graus:
            dist_grau[grau] += 1

        with open(caminho, 'w') as f:
            f.write(f"Numero de vertices: {n}\n")
            f.write(f"Numero de arestas: {m}\n")
            f.write(f"Grau medio: {grau_medio:.2f}\n")
            f.write("Distribuicao de grau:\n")
            for grau in sorted(dist_grau):
                f.write(f"Grau {grau}: {dist_grau[grau]} vertices\n")

    def busca_largura(self, inicio, caminho_saida):
        # Busca em largura com escrita em arquivo
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
        # Busca em profundidade recursiva com saída em arquivo
        visitado = set()
        pai = {inicio: None}
        nivel = {}

        def dfs(u, n):
            visitado.add(u)
            nivel[u] = n
            for v, _ in sorted(self.lista_adj[u]):
                if v not in visitado:
                    pai[v] = u
                    dfs(v, n + 1)

        dfs(inicio, 0)

        with open(caminho_saida, 'w') as f:
            for v in sorted(pai):
                f.write(f"Vertice: {v}, Pai: {pai[v]}, Nivel: {nivel[v]}\n")

    def componentes_conexos(self, caminho_saida):
        # Identifica componentes conexos usando BFS
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

        componentes.sort(key=len, reverse=True)

        with open(caminho_saida, 'w') as f:
            f.write(f"Numero de componentes: {len(componentes)}\n")
            for i, c in enumerate(componentes, 1):
                f.write(f"Componente {i} (tam={len(c)}): {' '.join(map(str, c))}\n")

    def tem_pesos_positivos(self):
        # Verifica se todas as arestas têm peso >= 0
        return all(p >= 0 for _, _, p in self.arestas)

    def dijkstra(self, inicio):
        # Algoritmo de Dijkstra com heap para menores distâncias
        dist = {v: float('inf') for v in self.vertices}
        pai = {v: None for v in self.vertices}
        dist[inicio] = 0
        heap = [(0, inicio)]

        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, peso in self.lista_adj[u]:
                alt = d + peso
                if alt < dist[v]:
                    dist[v] = alt
                    pai[v] = u
                    heapq.heappush(heap, (alt, v))
        return dist, pai

    def reconstruir_caminho(self, pai, destino):
        # Reconstrói caminho a partir do destino usando dicionário pai
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = pai[atual]
        caminho.reverse()  # Inverte para ordem correta: origem → destino
        return caminho

    def _bfs_caminho_minimo(self, inicio, destino=None):
        # BFS para encontrar caminho mínimo sem pesos
        visitado = {inicio}
        fila = deque([inicio])
        pai = {inicio: None}
        dist = {inicio: 0}

        while fila:
            u = fila.popleft()
            for v, _ in self.lista_adj[u]:
                if v not in visitado:
                    visitado.add(v)
                    pai[v] = u
                    dist[v] = dist[u] + 1
                    fila.append(v)

        if destino is not None:
            if destino not in pai:
                return float('inf'), []
            caminho = self.reconstruir_caminho(pai, destino)
            return dist[destino], caminho
        else:
            caminhos = {}
            for v in dist:
                caminho = self.reconstruir_caminho(pai, v)
                caminhos[v] = caminho
            return dist, caminhos

    def distancia_caminho_minimo(self, inicio, destino):
        # Caso grafo sem pesos ou todos pesos iguais a 1 → BFS
        if not self.arestas or all(p == 1 for _, _, p in self.arestas):
            return self._bfs_caminho_minimo(inicio, destino)

        # Caso tenha pesos negativos → também usa BFS (ignora pesos)
        if not self.tem_pesos_positivos():
            print("Aviso: grafo contém pesos negativos. Usando BFS sem considerar pesos.")
            return self._bfs_caminho_minimo(inicio, destino)

        # Caso contrário, usa Dijkstra (pesos positivos)
        dist, pai = self.dijkstra(inicio)

        # Se destino não é alcançável
        if dist.get(destino, float('inf')) == float('inf'):
            return float('inf'), []

        caminho = self.reconstruir_caminho(pai, destino)
        return dist[destino], caminho
