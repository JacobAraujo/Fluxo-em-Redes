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
# falta colocar os pesos nas arestas mas nem sei se precisa pq talvez só seja usado para achar o ciclo
# talvez uma boa solucao seja colocar no grafo os vertices apenas se a aresta nao seja -1 -> foi feito isso na funcao criarGrafoBasicas()

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
    nx.draw(grafo, pos=pos, with_labels=True, node_size=1200, node_color='red')
    plt.show()
    return grafo

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
        custo += modelo[int(aresta[0])-1][int(aresta[1])-1][0] * alterna
        alterna *= -1
    return custo <= 0

def achaValorPivoteamento(modelo, ciclo):
    alterna = 1
    menorNegativo = float('inf')
    posicao = []
    for aresta in ciclo:
        if alterna == -1 and modelo[int(aresta[0])-1][int(aresta[1])-1][0] < menorNegativo:
            menorNegativo = modelo[int(aresta[0])-1][int(aresta[1])-1][0]
            posicao.append(int(aresta[0])-1)
            posicao.append(int(aresta[1])-1)
        alterna *= -1
    return menorNegativo, posicao
# custos = [2,5,3,7,4,1]
# oferta = [25,25]
# demanda = [15,15,20]

custos = [2,2,2,1,10,8,5,4,7,6,6,8]
oferta = [3,7,5]
demanda = [4,3,4,4]

modelo = inicializaModelo(custos, oferta, demanda)
# imprime(modelo)

cantoNoroeste(modelo, oferta, demanda)
# print("Aplicada a regra do canto noroeste: \n")

# display(criarGrafo(modelo, oferta, demanda))
display(criarGrafoBasicas(modelo, oferta, demanda))

for i in range(len(oferta)):
    for j in range(len(demanda)):
        if modelo[i][j][0] == -1:
            modeloTeste = copy.deepcopy(modelo)
            modeloTeste[i][j][0] = 1
            # acha o ciclo da variável não básica
            ciclo = nx.find_cycle(criarGrafoBasicas(modeloTeste, oferta, demanda))
            ciclo = formatarCiclo(ciclo, [str(i+1), str(j+1)])
            print("Modelo: ")
            imprime(modeloTeste)
            print("i: ", i)
            print("j: ", j)
            print("Ciclo: ")
            print(ciclo)
            print('Custo do ciclo: ', testeCiclo(modeloTeste, ciclo))
            if testeCiclo(modeloTeste, ciclo): # teste ciclo retorna True se o custo do ciclo for negativo       
                valorPivoteamento, posicao = achaValorPivoteamento(modeloTeste, ciclo)
                print('Valor: ', valorPivoteamento, '\n', 'Posicao: ', posicao)
                # pivoteamento