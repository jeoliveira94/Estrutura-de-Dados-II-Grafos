class Vertice(object):
    """docstring for Vertice."""
    def __init__(self, nome):
        self.nome = nome
        self.adjacencias = []
        self.cor = 'branco'
        self.inicio = 0
        self.fim = 0
        self.pai = self  # adicionei o campo pai
        self.visitado = False

    def addAdjacencia(self, vertice):
            self.adjacencias.append(vertice)

    def __str__(self):
        lista = ''
        for adj in self.adjacencias:
            lista += '['+ adj.nome + ']'
        return '{}-->{}'.format(self.nome, lista)

class Aresta(object):
    """docstring for Aresta."""
    def __init__(self, origem: Vertice, destino: Vertice, peso: float):
        self.origem = origem
        self.destino = destino
        self.peso = peso

    def __str__(self):
        return '{}--{}-->{}'.format(self.origem.nome, self.peso, self.destino.nome)


class Grafo(object):
    """docstring for Grafo."""
    def __init__(self, numero_de_vertices, tipo ):
        self.arestas = []
        self.vertices = []
        self.tipo = tipo
        self.numero_de_vertices = numero_de_vertices
        self.matriz = self.matriz = [[0]*self.numero_de_vertices for _ in range(self.numero_de_vertices)]

    def addAresta(self, origem: Vertice, destino: Vertice, peso: float=1):
        e = Aresta(origem, destino, peso)
        origem.addAdjacencia(destino)
        self.arestas.append(e)
        if self.tipo != 'dirigido':
            print('entrou')
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

    def getVertice(self, nome):
        for v in self.vertices:
            if nome == v.nome:
                return v
        return None

    def lista_arestas(self):
        for e in self.arestas:
            print(e)

    def lista_vertices(self):
        for v in self.vertices:
            print(v)

    def lista_de_adjacencias(self):
        lista = ''
        for v in self.vertices:
            lista += v.nome + ' -> '
            for e in self.arestas:
                if v == e.origem:
                    lista += '({}, {}) '.format(e.destino.nome, str(e.peso))
            lista += '\n'
        return lista

    def show_matriz(self):
        for v in self.vertices:
            for e in self.arestas:
                if v.nome == e.origem.nome:
                    self.matriz[int(v.nome)][int(e.destino.nome)] = e.peso
        cols = list(range(self.numero_de_vertices))
        print('   ', end='')
        for i in cols:
            print(i, '', end=' ')
        print()
        for i, linha in enumerate(self.matriz):
            print(i, linha)

    def busca_profundidade(self, nome_vertice):
        class Pilha(list):
            """
            Uma pilha bem basica
            Usei herança pra sobrescrever os metodos
            deixando a contagem de inicio e fim  de cada vertice
            nas mãos da Pilha
            """
            def __init__(self):
                self.contador = 0
                super(Pilha, self).__init__()

            def append(self, elm: Vertice):
                elm.inicio = self.contador + 1
                self.contador += 1
                super().append(elm)

            def pop(self):
                elm = super().pop()
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
            if v.visitado is False:
                self.__dfs_recursiva(pilha, v)
        return self.vertices  # lista com os vertices

    def __dfs_recursiva(self, pilha, v):
        v.visitado = True
        pilha.append(v)
        for u in v.adjacencias:
            if u.visitado is False:
                self.__dfs_recursiva(pilha, u)
        pilha.pop()

    def busca_largura(self, nome_vertice):  # retorna um vetor com a ordem de visitação
        fila_de_prioridade = []  # fila de prioridade
        ordem_de_visitacao = []  # vetor com ordem de visitação
        for v in self.vertices:
            v.cor = 'branco'
        for t in self.vertices:  # procuro o vertice v na lista de vertices
            if t.nome == nome_vertice:
                fila_de_prioridade.append(t)  # adiciono ele na fila
                while fila_de_prioridade:
                    t = fila_de_prioridade.pop(0)
                    if t.cor == 'preto':  # se o que eu pegar for preto eu pego o proximo
                        t = fila_de_prioridade.pop(0)
                    else:
                        t.cor = 'cinza'  # pinta o vertice da fila de cinza
                    for x in t.adjacencias:  # coloca todos os que ele alcança na fila
                        if x not in fila_de_prioridade:
                            x.pai= t
                            fila_de_prioridade.append(x)
                    t.cor = 'preto'  # pinta ele de preto
                    ordem_de_visitacao.append(t.nome)
                    if t.nome != t.pai.nome:
                        t.inicio = t.pai.inicio + 1  # o tempo dele é o do pai mais 1
                    # print(t.nome,t.inicio) #mostra o tempo de descoberta e o vertice
        return ordem_de_visitacao

    def getTransposto(self):
        for e in self.arestas:
            e.origem, e.destino = e.destino, e.orige



if __name__ == '__main__':
    with open('./grafo.txt', mode='r', encoding='utf-8') as arquivo:
        tipo = arquivo.readline()[:-1]
        numero_de_vertices = int(arquivo.readline())
        g = Grafo(numero_de_vertices, tipo)
        for linha in arquivo:
            dados = linha.split()
            u = g.addVertice(str(dados[0]))
            v = g.addVertice(str(dados[1]))
            # bloco try se o grafo for ponderado
            try:
                peso = dados[2]
            except IndexError as error:
                peso = 1
            g.addAresta(u, v, int(peso))

    # A partir daqui pode brincar com o grafo e testar as funções
    print(g.lista_de_adjacencias())
    g.show_matriz()
    #print("\n",g.busca_largura('0'))
    vertices = g.busca_profundidade('0')
    for v in vertices:
        print(v.nome, v.inicio, v.fim)
