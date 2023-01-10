import itertools
import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import display
import copy

def inicializaModelo(custos, oferta, demanda):
    num = len(oferta) * len(demanda)
    modelo = []
    for i in range(len(oferta)):
        modelo.append([])
        for j in range(len(demanda)):
            modelo[i].append([-1, -1])
    # Preenche o modelo com os custos
    cont = 0     
    for i in range(len(oferta)):
        for j in range(len(demanda)):
            modelo[i][j][1] = custos[cont]
            cont += 1
    return modelo
        
# Imprime o modelo
def imprime(modelo):
    for i in range(len(modelo)):
        for j in range(len(modelo[i])):
            print(modelo[i][j], end=' ')
        print("\n")
    
def cantoNoroeste(modelo, oferta, demanda):    
    limite = len(oferta)+len(demanda)-1
    cont, linha, coluna = 0, 0, 0

    while(cont < limite): 
        if oferta[linha] <= demanda[coluna]:
            modelo[linha][coluna][0] = oferta[linha]
            demanda[coluna] -= oferta[linha]
            oferta[linha] = 0
            linha += 1
            
        elif demanda[coluna] < oferta[linha]:
            modelo[linha][coluna][0] = demanda[coluna]
            oferta[linha] -= demanda[coluna]
            demanda[coluna] = 0
            coluna += 1

        cont += 1
    return modelo, oferta, demanda

# falta testar para achar ciclo
def buscaProfundidade(grafo, inicio):
  pilha = [inicio]
  visitados = []

  while pilha:
    v = pilha.pop()
    if v not in visitados:
      visitados.append(v)
      for vizinho in grafo[v]:
        pilha.append(vizinho)

  return visitados

# funcao sem especificar posicao de plotagem

# def criarGrafo(modelo, oferta, demanda):
#     grafo = nx.Graph()
#     for origens in range(1, len(oferta)+1):
#         grafo.add_node("a" + str(origens))
#     for destinos in range(1, len(demanda)+1):
#         grafo.add_node("b" + str(destinos))
#     for i in range(1, len(oferta)+1):
#         for j in range(1, len(demanda)+1):
#             grafo.add_edge(("a"+str(i)), ("b"+str(j)))
#     nx.draw(grafo, with_labels=True, node_size=1200, node_color='red')
#     plt.show()    

# especificando posicao de plotagem
def criarGrafo(modelo, oferta, demanda):
    grafo = nx.Graph()
    pos = {}
    x = -1
    for i, o in enumerate(oferta, start=1):
        grafo.add_node("a" + str(i))
        pos["a" + str(i)] = (x, -i)
    x = 1
    for j, d in enumerate(demanda, start=1):
        grafo.add_node("b" + str(j))
        pos["b" + str(j)] = (x, -j)
    for i, o in enumerate(oferta, start=1):
        for j, d in enumerate(demanda, start=1):
            grafo.add_edge("a" + str(i), "b" + str(j))
    nx.draw(grafo, pos=pos, with_labels=True, node_size=1200, node_color='red')
    plt.show()
    return grafo

def criarGrafoBasicas(modelo, oferta, demanda):
    grafo = nx.Graph()
    pos = {}
    x = -1
    for i, o in enumerate(oferta, start=1):
        grafo.add_node("a" + str(i))
        pos["a" + str(i)] = (x, -i)
    x = 1
    for j, d in enumerate(demanda, start=1):
        grafo.add_node("b" + str(j))
        pos["b" + str(j)] = (x, -j)
    for i, o in enumerate(oferta, start=1):
        for j, d in enumerate(demanda, start=1):
            # verificar se o valor é positivo no modelo -> variavel basica
            if modelo[i-1][j-1][0] != -1:
                grafo.add_edge("a" + str(i), "b" + str(j))
    # nx.draw(grafo, pos=pos, with_labels=True, node_size=1200, node_color='red')
    # plt.show()
    return grafo

def achaCiclo(graph):
    stack = []
    visited = []
    ciclo = []

    # Adicione o vértice inicial à pilha e à lista de vértices visitados.
    stack.append(next(iter(graph)))
    visited.append(stack[-1])

    curr_vertex = ''
    while stack:
        # Remova o vértice do topo da pilha.
        parent = curr_vertex 
        curr_vertex = stack[-1]
        flag = True

        # Para cada vértice vizinho do vértice atual que ainda não tenha sido visitado:
        neighbors = list(graph.neighbors(curr_vertex))
        # print('Vertice atual: ', curr_vertex)
        # print('Parent: ', parent)
        # print('Visited: ', visited)
        # print('Stack: ', stack)
        for neighbor in neighbors:         
            if neighbor != parent and neighbor in visited:
                # Se o vértice vizinho já foi visitado anteriormente, então um ciclo foi encontrado.
                # Retorne a pilha como a lista de vértices que formam o ciclo.
                while True:
                    if stack:
                        ciclo.insert(0, stack.pop())
                        if ciclo[0] == neighbor:
                            return ciclo
        for neighbor in neighbors:     
            if neighbor not in visited:
                # Adicione o vértice vizinho à pilha e à lista de vértices visitados.
                stack.append(neighbor)
                visited.append(neighbor)
                flag = False
                break  
        if flag:       
            for neighbor in neighbors:
                if neighbor == parent and neighbor in stack:
                    # Adicione o vértice vizinho à pilha e à lista de vértices visitados.
                    stack.pop()
                    visited.append(neighbor)  
                    continue        


    # Se a pilha estiver vazia e nenhum ciclo for encontrado, retorne uma lista vazia.
    return []

def verticeParaAresta(ciclo):
    cicloEmArestas = []
    ciclo = list(ciclo)
    anterior = ''
    primeiraIteracao = True
    for vertice in ciclo:
        if primeiraIteracao:
            anterior = vertice
            primeiraIteracao = False
            continue
        cicloEmArestas.append((anterior, vertice))
        anterior = vertice
    cicloEmArestas.append((ciclo[-1], ciclo[0]))
    return cicloEmArestas

def arestaParaModelo(aresta):
    if aresta[0][0] == 'a':
        return [aresta[0][1], aresta[1][1]]
    else:
        return [aresta[1][1], aresta[0][1]]

def cicloFormatarij(ciclo):
    cicloFormatoij = []
    for aresta in ciclo:
        cicloFormatoij += [arestaParaModelo(aresta)]
    return cicloFormatoij

def formatarCiclo(ciclo, arestaInicial):
    cicloFormatoij = cicloFormatarij(ciclo)
    cicloFormatado = []
    flag = False
    for aresta in cicloFormatoij:
        if aresta == arestaInicial:
            flag = True
        if flag:
            cicloFormatado += [aresta]
    for aresta in cicloFormatoij:
        if aresta == arestaInicial:
            break
        cicloFormatado += [aresta]
    return cicloFormatado

def testeCiclo(modelo, ciclo):
    alterna = 1
    custo = 0
    for aresta in ciclo:
        custo += modelo[int(aresta[0])-1][int(aresta[1])-1][1] * alterna
        alterna *= -1
    return custo < 0

def achaValorPivoteamento(modelo, ciclo):
    alterna = 1
    menorNegativo = float('inf')
    posicao = [0, 0]
    for aresta in ciclo:
        if alterna == -1 and modelo[int(aresta[0])-1][int(aresta[1])-1][0] < menorNegativo:
            menorNegativo = modelo[int(aresta[0])-1][int(aresta[1])-1][0]
            posicao[0] = (int(aresta[0])-1)
            posicao[1] = (int(aresta[1])-1)
        alterna *= -1
    return menorNegativo, posicao

def pivoteamento(modelo, ciclo, valor, posicao):
    alterna = -1
    modelo[int(ciclo[0][0])-1][int(ciclo[0][1])-1][0] = valor
    for aresta in ciclo[1:]:
        modelo[int(aresta[0])-1][int(aresta[1])-1][0] += valor * alterna
        alterna *= -1
    modelo[posicao[0]][posicao[1]][0] = -1
    
def custoRelativo(modelo):
    custoRelativo = 0
    for i in range(len(modelo)):
        for j in range(len(modelo[i])):
            if modelo[i][j][0] > 0:
                custoRelativo += modelo[i][j][0] * modelo[i][j][1]
    return custoRelativo
    
# custos = [2,5,3,7,4,1]
# oferta = [25,25]
# demanda = [15,15,20]

# custos = [2,2,2,1,10,8,5,4,7,6,6,8]
# oferta = [3,7,5]
# demanda = [4,3,4,4]

custos = [2, 3, 4, 3, 5, 6, 4, 3, 5, 6, 6, 8]
oferta = [4, 5, 15]
demanda = [5, 6, 7, 6]

modelo = inicializaModelo(custos, oferta, demanda)

cantoNoroeste(modelo, oferta, demanda)
imprime(modelo)

# display(criarGrafo(modelo, oferta, demanda))
display(criarGrafoBasicas(modelo, oferta, demanda))

flag = True # continua verificando
while(flag):
    flag = False
    for i in range(len(oferta)):
        for j in range(len(demanda)):
            if modelo[i][j][0] == -1:
                modeloTeste = copy.deepcopy(modelo)
                modeloTeste[i][j][0] = 1
                # acha o ciclo da variável não básica
                ciclo = nx.find_cycle(criarGrafoBasicas(modeloTeste, oferta, demanda))
                # ciclo = achaCiclo(criarGrafoBasicas(modeloTeste, oferta, demanda))
                # ciclo = verticeParaAresta(ciclo)
                ciclo = formatarCiclo(ciclo, [str(i+1), str(j+1)])
                print(ciclo)
                # print("Modelo: ")
                # imprime(modeloTeste)
                # print("i: ", i)
                # print("j: ", j)
                # print("Ciclo: ")
                # print(ciclo)
                # print('Custo do ciclo: ', testeCiclo(modeloTeste, ciclo))
                if testeCiclo(modeloTeste, ciclo): # teste ciclo retorna True se o custo do ciclo for negativo       
                    valorPivoteamento, posicao = achaValorPivoteamento(modeloTeste, ciclo)
                    # print('Valor: ', valorPivoteamento, '\n', 'Posicao: ', posicao)
                    pivoteamento(modelo, ciclo, valorPivoteamento, posicao)
                    flag = True
                    # print('Modelo depois do pivoteamento: ')
                    imprime(modelo)
                    print('Custo Relativo: ', custoRelativo(modelo))

print('Custo Relativo: ', custoRelativo(modelo))