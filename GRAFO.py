class Vertice(object):
    """docstring for Vertice."""
    def __init__(self, nome):
        self.nome = nome
        self.adjacencias = []
        self.cor = 'branco'
        self.inicio = 0
        self.fim = 0
        self.pai = self  # adicionei o campo pai

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
        self.ciclico = False  # Usar DFS para definir True ou False
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
        with open('./lista_de_adjacencias.txt', mode='w', encoding='utf-8') as lista_f:
            lista_f.write(lista)
        for linha in lista:
            print(linha, end='')
        return

    def matriz_de_adjacencia(self):
        for v in self.vertices:
            for e in self.arestas:
                if v.nome == e.origem.nome:
                    self.matriz[int(v.nome)][int(e.destino.nome)] = e.peso
        cols = list(range(self.numero_de_vertices))
        with open('./matriz_de_adjacencias.txt', mode='w', encoding='utf-8') as matriz_f:
            matriz_f.write('    ')
            for i in cols:
                matriz_f.write('{}  '.format(str(i)) )
            matriz_f.write('\n')
            for i, linha in enumerate(self.matriz):
                matriz_f.write(' {} {}\n'.format(str(i), str(linha)))

        with open('./matriz_de_adjacencias.txt', mode='r', encoding='utf-8') as matriz_f:
            for linha in matriz_f:
                print(linha, end='')


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
            if v.cor == 'branco':
                self.__dfs_recursiva(pilha, v)
        return self.arestas

    def __dfs_recursiva(self, pilha, v):
        v.cor = 'cinza'  # vertice visitado
        pilha.append(v)  # empilha
        for u in v.adjacencias:
            self.__classificar_aresta(v, u)  # classifa aresta correspondente
            if u.cor == 'branco':  # vertice ainda não visitado
                self.__dfs_recursiva(pilha, u)
        v.cor = 'preto'  # vertice totalmente visitado
        pilha.pop()  # desempilha

    def ordenacao_topologica(self, nome_vertice):
        DFS = self.busca_profundidade(nome_vertice)
        # ordenação topológica so pode ser feita em grafo dirigido e aciclico
        if self.tipo == 'dirigido' and self.ciclico is False:
            # selectioin sort para ordenar a listar de vertices pelo tempo de fim
            for i in range(len(self.vertices)- 1):
                max = i
                for j in range(i, len(self.vertices)):
                    if self.vertices[j].fim > self.vertices[max].fim:
                        max = j
                if self.vertices[i] != self.vertices[max]:
                    aux =  self.vertices[i]
                    self.vertices[i] = self.vertices[max]
                    self.vertices[max] = aux
        else:
            print('ERRO, GRAFO COMTEM CLICOS')
            return None
        return self.vertices  #  retorna lista de vertices

    def elementos_fortemente_conexos(self, nome_vertice):
        DFS = self.busca_profundidade(nome_vertice)
        self.__setTransposto()  # transpondo o grafo
        v = self.__getMaiorTempo()  # vertice com maior tempo de fim
        # busca em profunidade no grafo transposto começando pelo cara de maior tempo
        DFS = self.busca_profundidade(v.nome)
        # remoção de arestas que não seja do tipo arvore
        for e in self.arestas:
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
            self.ciclico = True
            self.numero_de_ciclos += 1
            e.tipo = 'retorno'
        elif destino.cor == 'preto':
            if origem.inicio < destino.inicio:
                e.tipo = 'avanco'
            else:
                e.tipo = 'cruz'
        return

    def busca_em_largura(self, nome_vertice):  # retorna um vetor com a ordem de visitação
        fila_de_prioridade = []  # empilha]  # fila de prioridade
        ordem_de_visitacao = []  # vetor com ordem de visitação
        for v in self.vertices:
            v.cor  # classifa aresta correspondente = 'branco'
        for t in self.vertices:  # procuro o vertic  # vertice ainda não visitadoe v na lista de vertices
            if t.nome == nome_vertice:
                fila_de_prioridade.append(t)  # adiciono ele na fila  # vertice totalmente visitado
                while fila_de_prioridade:  # desempilha
                    t = fila_de_prioridade.pop(0)
                    if t.cor == 'preto':  # se o que eu pegar for preto eu pego o proximo
                        t = fila_de_prioridade.pop(0)
                    else:
                        t.cor = 'cinza'  # pinta o vertice da fila de cinza
                    for x in t.adjacencias:  # coloca todos os que ele alcança na fila
                        if x not in fila_de_prioridade:
                            x.pai = t
                            fila_de_prioridade.append(x)
                    t.cor = 'preto'  # pinta ele de preto
                    ordem_de_visitacao.append(t.nome)
                    if t.nome != t.pai.nome:
                        t.inicio = t.pai.inicio + 1  # o tempo dele é o do pai mais 1
                    # print(t.nome,t.inicio) #mostra o tempo de descoberta e o vertice
        return ordem_de_visitacao

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
        with open('./info.txt', mode='w', encoding='utf-8') as info_f:
            info_f.write('Numero de Vertices: {}\n'.format(len(self.vertices)))
            info_f.write('Numero de Arestas: {}\n'.format(len(self.arestas)))
            info_f.write('Numero de ciclos: {}\n'.format(self.numero_de_ciclos))

#
# if __name__ == '__main__':
#     welcome_msg = 'Olá!!'
#     grafo_dir_pon = './grafo.txt'
#     grafo_not_dir_pon = './grafo2.txt'
#     grafo_not_dir_not_pon = './grafo3.txt'
#     grafo_dir_not_pon = './grafo4.txt'
#     grafo_dir_pon_aci = './grafo5.txt'
#     load_sucess_msg = 'Grafo carregado com Sucesso!!!'
#     ciclico = int(input('Ciclico?? <1> yes <2> no\n'))
#     ponderado = int(input('ponderado?? <1> yes <2> no\n'))
#     dirigido = int(input('dirigido?? <1> yes <2> no\n'))

if __name__ == '__main__':
    with open('./grafo3.txt', mode='r', encoding='utf-8') as arquivo:
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
        g.sort()

    # A partir daqui pode brincar com o grafo e testar as funções
    g.lista_de_adjacencias()
    # g.matriz_de_adjacencia()
    # for elm in g.busca_profundidade('0'):
    #     print(elm)

    # for elm in g.elementos_fortemente_conexos('0'):
    #     print(elm)
    # for elm in g.prim('0'):
    #     print(elm)
