from biblioteca_grafos import Grafo

# Arquivos de entrada
arquivo_entrada_com_peso = 'grafo_com_peso_positivo.txt'
arquivo_entrada_com_peso_negativo = 'grafo_com_peso_negativo.txt'
arquivo_entrada_sem_peso = 'grafo_sem_peso.txt'

# ----- Grafo com pesos positivos -----
g = Grafo(representacao='lista')
g.carregar_arquivo(arquivo_entrada_com_peso)
dist, caminho = g.distancia_caminho_minimo(1, 3)
print("\n📗 Grafo com Peso Positivo:")
print(f"Distância mínima entre 1 e 3: {dist}")
print(f"Caminho mínimo entre 1 e 3: {' -> '.join(map(str, caminho))}")

# ----- Grafo com pesos negativos -----
g_neg = Grafo(representacao='lista')
g_neg.carregar_arquivo(arquivo_entrada_com_peso_negativo)
dist, caminho = g_neg.distancia_caminho_minimo(1, 3)
print("\n📕 Grafo com Peso Negativo:")
print(f"Distância mínima entre 1 e 3: {dist}")
print(f"Caminho mínimo entre 1 e 3: {' -> '.join(map(str, caminho))}")

# ----- Grafo sem pesos -----
g_sem = Grafo(representacao='lista')
g_sem.carregar_arquivo(arquivo_entrada_sem_peso)
dist, caminho = g_sem.distancia_caminho_minimo(1, 3)
print("\n📘 Grafo Sem Peso:")
print(f"Distância mínima entre 1 e 3: {dist}")
print(f"Caminho mínimo entre 1 e 3: {' -> '.join(map(str, caminho))}")
