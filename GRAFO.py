class Vertice(object):
    """docstring for Vertice."""
    def __init__(self, nome):
        self.nome = nome
        self.adjacencias = []
        self.cor = 'branco'
        self.inicio = 0
        self.fim = 0

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
        return 'Arvore'

    def busca_largura(self, nome_vertice):
        return 'Arvore'

    def getTransposto(self):
        for e in self.arestas:
            e.origem, e.destino = e.destino, e.origem


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
