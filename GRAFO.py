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
        self.matriz = None

    def addAresta(self, nome_origem: Vertice, nome_destino: Vertice, peso: float=1):
        origem = self.getVertice(nome_origem)
        if origem is None:
            origem = Vertice(nome_origem)

        destino = self.getVertice(nome_destino)
        if destino is None:
            destino = Vertice(nome_destino)

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
        if nome not in self.vertices:
            vertice = Vertice(nome)
            self.vertices.append(vertice)
        return True

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
        if self.matriz is None:
            self.matriz = []
            self.matriz = [[0]*self.numero_de_vertices for _ in range(self.numero_de_vertices)]
            for linha in self.matriz:
                linha = [0] * self.numero_de_vertices
            for v in self.vertices:
                for e in self.arestas:
                    if v.nome == e.origem.nome:
                        self.matriz[int(v.nome)][int(e.destino.nome)] = e.peso
            for linha in self.matriz:
                print(linha)

    def busca_profundidade(self, nome_vertice):
        return 'Arvore'

    def busca_largura(self, nome_vertice):
        return 'Arvore'

    def getTransposto(self):
        for e in self.arestas:
            e.origem, e.destino = e.destino, e.origem


if __name__ == '__main__':
    g = Grafo(5, tipo='não dirigido')
    g.addVertice('4')
    g.addVertice('3')
    g.addAresta('4', '3', 0.56)
    # g.addAresta('3', '4', 0.5)
    print(g.lista_de_adjacencias())
    g.show_matriz()
