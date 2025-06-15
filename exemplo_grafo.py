# exemplo_uso_grafo.py
from biblioteca_grafos import Grafo

# Caminho para o arquivo de entrada contendo o grafo
# Formato: primeira linha = numero de vertices
# Demais linhas = arestas no formato "u v peso" ou "u v"
arquivo_entrada = 'grafo.txt'

# Criação do grafo com representação por lista de adjacência
g = Grafo(representacao='lista')

# Leitura do grafo a partir do arquivo
g.carregar_arquivo(arquivo_entrada)
print("Grafo carregado com sucesso!")

# Geração de informações gerais do grafo
g.salvar_info_grafo('saida_info.txt')
print("Informações do grafo salvas em 'saida_info.txt'")

# Realização de busca em largura a partir do vértice 0
g.busca_largura(inicio=1, caminho_saida='busca_largura.txt')
print("Busca em largura concluída. Resultados salvos em 'busca_largura.txt'")

# Realização de busca em profundidade a partir do vértice 0
g.busca_profundidade(inicio=1, caminho_saida='busca_profundidade.txt')
print("Busca em profundidade concluída. Resultados salvos em 'busca_profundidade.txt'")

# Descoberta dos componentes conexos
g.componentes_conexos('componentes_conexos.txt')
print("Componentes conexos identificados e salvos em 'componentes_conexos.txt'")

# OBS: para usar representação por matriz, basta instanciar com:
# g = Grafo(representacao='matriz')
