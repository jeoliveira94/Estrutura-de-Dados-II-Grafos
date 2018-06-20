class Grafo(object):
    """docstring for Grafo."""
    def __init__(self, arq_grafo):
        with open(arq_grafo) as arquivo:
            grafo_info = []
            for linha in arquivo:
                grafo_info.append(linha.split())
            dirigido  = int(grafo_info[0][0])
            ponderado = int(grafo_info[1][0])
            tamanho = int(grafo_info[2][0])
            self.matriz = [0] * tamanho
            for i in range(tamanho):
                self.matriz[i] = [0] * tamanho
        grafo_info = grafo_info[3:]
        if dirigido:
            for info in grafo_info:
                self.inserir(int(info[i][0]),
                             int(info[i][1]),
                             dirigido=dirigido)
        else:
            for info in grafo_info:
                self.inserir(int(info[i][0]),
                             int(info[i][1]),
                             float(info[i][2]),
                             dirigido=dirigido)


    def inserir(self, origem, destino, peso=1, dirigido=0):
        self.matriz[origem][destino] = peso
        if not dirigido:
            self.matriz[destino][origem] = peso

    def showMatriz(self):
        for i in range(len(self.matriz)):
            for j in range(self.matriz[i]):
                print(self.matriz[i][j])

if __name__ == '__main__':
    g = Grafo('grafo-a.txt')
    g.showMatriz()
