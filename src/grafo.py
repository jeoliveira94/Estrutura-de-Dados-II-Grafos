def selection_sort(conjunto):
    for i in range(len(conjunto) - 1):
        max = i
        for j in range(i, len(conjunto)):
            if conjunto[j].fim > conjunto[max].fim:
                max = j
        if conjunto[i] != conjunto[max]:
            aux = conjunto[i]
            conjunto[i] = conjunto[max]
            conjunto[max] = aux
    return True

class Vertice(object):
    """docstring for Vertice."""
    def __init__(self, nome):
        self.nome = nome
        self.adjacencias = []
        self.cor = 'branco'
        self.inicio = 0
        self.fim = 0
        self.pai = None
        self.distancia = 0

    def addAdjacencia(self, vertice):
        self.adjacencias.append(vertice)

    def __str__(self):
        lista = ''
        for adj in self.adjacencias:
            lista += '['+ adj.nome + ']'
        return '{}-->{}'.format(self.nome, lista)

    def __lt__(self, other):
        return self.nome < other.nome


class Aresta(object):
    """docstring for Aresta."""
    def __init__(self, origem: Vertice, destino: Vertice, peso: float):
        self.origem = origem
        self.destino = destino
        self.peso = peso
        self.tipo = ''

    def __str__(self):
        return 'origem[{}]--peso[{}]--destino[{}]---tipo[{}]'.format(self.origem.nome, self.peso, self.destino.nome, self.tipo)


class Grafo(object):
    """docstring for Grafo."""
    def __init__(self, numero_de_vertices, tipo):
        self.arestas = []
        self.vertices = []
        self.tipo = tipo  # dirigido ou não dirigido
        self.numero_de_vertices = numero_de_vertices
        self.matriz = self.matriz = self.__geraMatriz(numero_de_vertices)
        self.numero_de_ciclos = 0

    def __geraMatriz(self, tamanho):
        """
        Gera Matriz preenchida com zero de ordem tamanho x tamanho
        """
        return [[0]*tamanho for _ in range(tamanho)]

    def addAresta(self, origem: Vertice, destino: Vertice, peso: float=1):
        e = Aresta(origem, destino, peso)
        origem.addAdjacencia(destino)
        self.arestas.append(e)
        if self.tipo != 'dirigido':
            a = Aresta(destino, origem, peso)
            destino.addAdjacencia(origem)
            self.arestas.append(a)
        return True

    def addVertice(self, nome: str):
        for v in self.vertices:
            if v.nome == nome:
                return v
        v = Vertice(nome)
        self.vertices.append(v)
        return v

    def __getVertice(self, nome):
        for v in self.vertices:
            if nome == v.nome:
                return v
        return None

    def lista_de_adjacencias(self):
        lista = ''
        for v in self.vertices:
            lista += 'origem: ' + v.nome + ' -> '
            for e in self.arestas:
                if v == e.origem:
                    lista += '(destino: {}, peso: {}) '.format(e.destino.nome, str(e.peso))
            lista += '\n'
        with open('../outputs/lista_de_adjacencias.txt', mode='w', encoding='utf-8') as lista_f:
            lista_f.write(lista)
        print(lista)
        return

    def matriz_de_adjacencia(self):
        for v in self.vertices:
            for e in self.arestas:
                if v.nome == e.origem.nome:
                    self.matriz[int(v.nome)][int(e.destino.nome)] = e.peso
        cols = list(range(self.numero_de_vertices))
        with open('../outputs/matriz_de_adjacencias.txt', mode='w', encoding='utf-8') as matriz_f:
            matriz_f.write('    ')
            for i in cols:
                matriz_f.write('{}  '.format(str(i)) )
            matriz_f.write('\n')
            for i, linha in enumerate(self.matriz):
                matriz_f.write(' {} {}\n'.format(str(i), str(linha)))

        with open('../outputs/matriz_de_adjacencias.txt', mode='r', encoding='utf-8') as matriz_f:
            print(matriz_f.read())
        return

    def busca_profundidade(self, nome_vertice):
        class Pilha(list):
            def __init__(self):
                self.contador = 0
                self.arvore_de_busca = []
                super(Pilha, self).__init__()

            def append(self, elm: Vertice):
                elm.inicio = self.contador + 1
                self.contador += 1
                super().append(elm)

            def pop(self):
                elm = super().pop()
                self.arvore_de_busca.append(elm)
                elm.fim = self.contador + 1
                self.contador += 1

        pilha = Pilha()  # empilhar->'.append', desempilhar->'.pop()'
        for vertice in self.vertices:
            vertice.inicio = 0  # definindo tempo de inicio = fim = 0
            vertice.fim = 0
            if vertice.nome == nome_vertice:  # selecionando vertice para iniciar a busca
                v = vertice
        if v is None:  # vertice não valido
            return None
        pilha = Pilha()  # incializando a pilha
        self.__dfs_recursiva(pilha, v)  # iniciando a busca no vertice v
        for v in self.vertices:  # procura vertices desconexos que ainda não foram visitados
            if v.cor == 'branco':
                self.__dfs_recursiva(pilha, v)
        pilha.arvore_de_busca.reverse()
        return pilha.arvore_de_busca
        
    def __dfs_recursiva(self, pilha, v):
        v.cor = 'cinza'  # vertice visitado
        pilha.append(v)  # empilha
        for u in v.adjacencias:
            self.__classificar_aresta(v, u)  # classifa aresta correspondente
            if u.cor == 'branco':  # vertice ainda não visitado
                u.pai = v
                self.__dfs_recursiva(pilha, u)
        v.cor = 'preto'  # vertice totalmente visitado
        pilha.pop()  # desempilha

    def ordenacao_topologica(self, nome_vertice):
        DFS = self.busca_profundidade(nome_vertice)
        # ordenação topológica so pode ser feita em grafo dirigido e aciclico
        if self.tipo == 'dirigido' and self.numero_de_ciclos == 0:
            # selectioin sort para ordenar a listar de vertices pelo tempo de fim
            selection_sort(self.vertices)
        else:
            print('ERRO, GRAFO CONTEM CLICOS')
            return None
        return self.vertices  #  retorna lista de vertices

    def elementos_conexos(self, nome_vertice):
        DFS = self.busca_profundidade(nome_vertice)
        self.__setTransposto()  # transpondo o grafo
        v = self.__getMaiorTempo()  # vertice com maior tempo de fim
        # busca em profundidade no grafo transposto começando pelo cara de maior tempo
        DFS = self.busca_profundidade(v.nome)
        # remoção de arestas que não seja do tipo arvore
        for e in self.arestas:
            #print(e)
            if e.tipo != 'arvore':
                self.arestas.remove(e)
        return self.arestas

    def __getMaiorTempo(self):
        u = self.vertices[0]
        for v in self.vertices:
            if v.fim > u.fim:
                u = v
        return u

    def __getAresta(self, origem: Vertice, destino: Vertice):
        for e in self.arestas:
            if e.origem == origem and e.destino == destino:
                return e
        return None

    def __classificar_aresta(self, origem: Vertice, destino: Vertice):
        e = self.__getAresta(origem, destino)
        if e is None:
            return
        if destino.cor == 'branco':
            e.tipo = 'arvore'
        elif destino.cor == 'cinza':
            self.numero_de_ciclos += 1
            e.tipo = 'retorno'
        elif destino.cor == 'preto':
            if origem.inicio < destino.inicio:
                e.tipo = 'avanco'
            else:
                e.tipo = 'cruz'
        return

    def __setTransposto(self):
        for e in self.arestas:
            e.origem, e.destino = e.destino, e.origem

    def sort(self):
        # ordena por ordem alfabetica a lista dos vertices do grafo
        self.vertices.sort()
        # ordenação da lista de adjacencias de cada vertice por ordem alfabetica
        for v in self.vertices:
            v.adjacencias.sort()
        return ''

    def info(self):
        with open('../outputs/info.txt', mode='w', encoding='utf-8') as info_f:
            info_f.write('Numero de Vertices: {}\n'.format(len(self.vertices)))
            info_f.write('Numero de Arestas: {}\n'.format(len(self.arestas)))
            info_f.write('Numero de ciclos: {}\n'.format(self.numero_de_ciclos))

    def busca_em_largura(self, nome_vertice):
        v = self.__getVertice(nome_vertice)
        if v is None:
            return None

        class Fila(list):
            def __init__(self):
                self.arvore_de_busca = []
                super(Fila, self).__init__()

            def append(self, vertice, pai_vertice=None):
                vertice.pai = pai_vertice
                if pai_vertice is None:
                    vertice.inicio = 1
                else:
                    vertice.inicio = pai_vertice.inicio + 1
                vertice.cor = 'preto'
                super().append(vertice)

            def pop(self):
                vertice = super().pop(0)
                for v in vertice.adjacencias:
                    if v.cor == 'branco':
                        self.append(v, pai_vertice=vertice)
                return vertice
        fila = Fila()
        fila.append(v, pai_vertice=None)
        resultado = []
        while len(fila) > 0:
            resultado.append(fila.pop())
        return resultado


    def gerar_arvore_de_busca(self, resultado_da_busca, tipo_busca=''):
        with open('../outputs/arvore_de_busca_em_'+tipo+'.txt', mode='w', encoding='utf=8') as arvore_f:
            for item in resultado_da_busca:
                try:
                    var = 'Pai: {}, Vertice: {}, Nivel: {}'.format(item.pai.nome, item.nome, item.inicio)
                except AttributeError as e:
                    var = 'Pai: {}, Vertice: {}, Nivel: {}'.format('NULL', item.nome, item.inicio)
                arvore_f.write(var + '\n')
                print(var)

    def dijkstra(self, nome_origem):
        def relax(v: Vertice, u: Vertice):
            '''Relaxa aresta (v, u)'''
            e = self.__getAresta(v, u)
            distancia = v.distancia + e.peso
            if distancia < u.distancia:
                u.distancia = distancia
                u.pai = v
        def tem_branco(vertices):
            '''verificar se existe vertice aberto, de cor branca'''
            for v in vertices:
                if v.cor == 'branco':
                    return True
            return False
        def get_menor_branco(vertices):
            '''retorna vertice branco com menor distancia'''
            lista = []
            for v in self.vertices:
                if v.cor == 'branco':
                    lista.append(v)
            menor = lista[0]
            for elm in lista:
                if elm.distancia < menor.distancia:
                    menor = elm
            menor.cor = 'preto'
            return menor
        # procura pelo vertice de origem
        start = self.__getVertice(nome_origem)
        # verifica se o vertice é valido
        if start is None:
            print('Vertice invalido')
            return None
        # vertice de origem tem distancia 0 dele mesmo
        start.distancia = 0
        # definindo distancia de todos os vertices demais como 99999
        for v in self.vertices:
            v.pai = None
            v.cor = 'branco'
            if v != start:
                v.distancia = 99999
        while(tem_branco(self.vertices)):
            v = get_menor_branco(self.vertices)
            for u in v.adjacencias:
                if u.cor == 'branco':
                    relax(v, u)
        return True

    def menor_caminho(self, nome_origem, nome_destino):
        '''retorna menor caminho entre 2 vertices'''
        v = self.__getVertice(nome_origem)
        u = self.__getVertice(nome_destino)
        if u is None or v is None:
            print('vertices invalidos')
            return None
        self.dijkstra(v.nome)
        lista = []
        while u is not None:
            lista.append(u)
            u = u.pai
        # faz um reverse na lista pois a lista contem o
        # caminho inverso de destino para origem
        lista.reverse()
        return lista  # retorna lista com o caminho mais curto

    def floyd_warsall(self,numero_de_vertices):
        '''printa uma matriz com os caminhos mais curtos'''
        matriz_caminho_min = [[0]*numero_de_vertices for _ in range(numero_de_vertices)]
        if self.tipo != 'não dirigido': # só
            for i in range(len(matriz_caminho_min)): # faço a matriz de adjacencias
                for j in range(len(matriz_caminho_min[i])):
                    for k in self.arestas:
                        if k.origem.nome == str(i) and k.destino.nome == str(j):
                            matriz_caminho_min[i][j] = k.peso

            for i in range(len(matriz_caminho_min)):# coloco infinito(i) em todos os estados que são 0
                for j in range(len(matriz_caminho_min[i])):
                    if matriz_caminho_min[i][j] == 0:
                        matriz_caminho_min[i][j] = 'i'
            for k in range(numero_de_vertices):#coloco 0 na diagonal principal
                matriz_caminho_min[k][k] = 0
            for k in range(numero_de_vertices): # faço o calculo da matriz de caminho minimo
                for i in range(len(matriz_caminho_min)):
                    for j in range(len(matriz_caminho_min[i])):
                        if matriz_caminho_min[i][k] != 'i' and matriz_caminho_min[k][j] != 'i':
                            if matriz_caminho_min[i][j] == 'i' or matriz_caminho_min[i][j] > matriz_caminho_min[i][k] + matriz_caminho_min[k][j]:

                                matriz_caminho_min[i][j] = matriz_caminho_min[i][k] + matriz_caminho_min[k][j]
            for i in range(len(matriz_caminho_min)):

                for j in range(len(matriz_caminho_min[i])):
                    print(matriz_caminho_min[i][j],'\t',end = "")
                print('')
        else:
            print('ERRO, O GRAFO É DIRIGIDO')
        return None
