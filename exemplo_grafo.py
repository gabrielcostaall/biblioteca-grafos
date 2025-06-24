from biblioteca_grafos import Grafo

# Caminho para o arquivo de entrada contendo o grafo
arquivo_entrada_com_peso = 'grafo_com_peso_positivo.txt'

# Instancia o grafo com lista de adjacência (pode trocar para 'matriz' se quiser)
g = Grafo(representacao='lista')

# Carrega o grafo a partir do arquivo
g.carregar_arquivo(arquivo_entrada_com_peso)
print("Grafo carregado com sucesso!")

# Informações gerais do grafo (imprime no console)
n = len(g.vertices)
m = len(g.arestas)
graus = [len(g.lista_adj[v]) for v in g.vertices]
grau_medio = sum(graus) / n
print(f"Número de vértices: {n}")
print(f"Número de arestas: {m}")
print(f"Grau médio: {grau_medio:.2f}")

# Imprime grau de cada vértice
print("Grau de cada vértice:")
for v in sorted(g.vertices):
    print(f"  Vértice {v}: grau {len(g.lista_adj[v])}")

# Salva informações básicas do grafo em arquivo
g.salvar_info_grafo('saida_info.txt')
print("Informações do grafo salvas em 'saida_info.txt'")

# Busca em largura, salva resultados em arquivo
g.busca_largura(inicio=1, caminho_saida='busca_largura.txt')
print("Busca em largura concluída. Resultados salvos em 'busca_largura.txt'")

# Busca em profundidade, salva resultados em arquivo
g.busca_profundidade(inicio=1, caminho_saida='busca_profundidade.txt')
print("Busca em profundidade concluída. Resultados salvos em 'busca_profundidade.txt'")

# Identifica componentes conexos, salva em arquivo
g.componentes_conexos('componentes_conexos.txt')
print("Componentes conexos identificados e salvos em 'componentes_conexos.txt'")

# Distância mínima e caminho entre 1 e 3 (imprime no console)
dist, caminho = g.distancia_caminho_minimo(1, 3)
print(f"Distância mínima entre 1 e 3: {dist}")
print(f"Caminho mínimo entre 1 e 3: {' -> '.join(map(str, caminho))}")
