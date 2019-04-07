from grafo import Grafo

if __name__ == '__main__':
    while True:
        print('''\nEstrutura de dados II - Implementação 3\n\n[ 1 ] Carregar Grafo\n[ 0 ] Sair do Programa''')
        opc = int(input('Escolha uma Opção: '))
        if opc == 0:
            print('')
            break
        if opc == 1:
            print('''[ 1 ] Grafo Dirigido\n[ 2 ] Grafo Não Dirigido\n[ 3 ] Entre Com seu grafo''')
            opc = int(input('Escolha uma Opção: '))
            if opc != 1 and opc != 2 and opc != 3:
                print('ERRO, OPÇÃO INVALIDA')
                break
            if opc == 3:
                grafo = str(input('Entre com o caminho de onde o Grafo se encontra\n'))
            else:
                grafo = '../grafos/grafo' + str(opc)+'.txt'
            with open(grafo, mode='r', encoding='utf-8') as arquivo:
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

            while True:
                print('Como deseja representar o Grafo?')
                print('''[ 1 ] Lista de Adjacencias\n[ 2 ] Matriz de Adjacencias\n[ 3 ] Ir para os Algoritmos''')
                opc = int(input('Escolha uma Opção: '))
                if opc == 1:
                    g.lista_de_adjacencias()
                elif opc == 2:
                    g.matriz_de_adjacencia()
                elif opc == 3:
                    break
                else:
                    print('ERRO, OPÇÃO INVALIDA')
                    break
        else:
            print('ERRO, OPÇÃO INVALIDA')
            break
        while True:
            print('''[ 1 ] Realizar Busca\n[ 2 ] Componentes Fortemente Conexos\n[ 3 ] Caminho Minimo\n[ 4 ] Ordenação Topologica\n[ 5 ] Sair''')
            opc = int(input('Escolha uma Opção: '))
            if opc == 1:
                opc = int(input('1 - Largura\n2 - Profundidade'))
                if opc == 1:
                    vertice_inicio = str(input('Qual o vertice origem?\n'))
                    resultado = g.busca_em_largura(vertice_inicio)
                    for i in resultado:
                        print('Vertice:', i.nome, '\ttempo de Descoberta:', i.inicio)
                    g.gerar_arvore_de_busca(resultado, tipo_busca='largura')
                elif opc == 2:
                    vertice_inicio = str(input('Qual o vertice origem?\n'))
                    resultado = g.busca_profundidade(vertice_inicio)
                    for i in resultado:
                        print('Vertice:', i.nome, '\ttempo de Descoberta:', i.inicio, '\ttempo de termino: ', i.fim)
                    g.gerar_arvore_de_busca(resultado, tipo_busca='largura')
                else:
                    print('ERRO, OPÇÃO INVALIDA')
                    break
                g.info()
            elif opc == 2:
                nome_origem = '0'
                elementos_conexos = g.elementos_conexos(nome_origem)
                print('Numero de Elementos Conexos: {}'.format(len(elementos_conexos)))
                i =0
                for elm in elementos_conexos:
                    i+=1
                    print('Origem: {}-->Destino: {}'.format(elm.origem.nome, elm.destino.nome))
                print('Numero de elementos fortemente conexos: ', i)
            elif opc == 3:
                opc = int(input('[ 1 ] Dijkstra\n[ 2 ] Floyd-Warshall'))
                if opc == 1:
                    print('Usando Dijkstra\nCaminho do vertice {} ate o vertice{}'.format('origem', ' destino'))
                    for v in g.menor_caminho('0', '2'):
                        print('Vertice: {}, Distancia: {}'.format(v.nome, v.distancia))
                elif opc == 2:
                    print('')
                    g.floyd_warsall(g.numero_de_vertices)
                    print('')
                else:
                    print('ERRO, OPÇÃO INVALIDA')
                    break
            elif opc == 4:
                nome_origem = str(input('Qual o vertice origem?\n'))
                ordenacao_topologica = g.ordenacao_topologica(nome_origem)
                if ordenacao_topologica != None:
                    print('sequência aconselhada')
                    for i in ordenacao_topologica:
                        print('Vertice:', i.nome, '\t', end='')
                    print('\n')
                    for i in ordenacao_topologica:
                        print('Vertice:', i.nome, '\ttempo de Descoberta:', i.inicio, '\ttempo de termino: ', i.fim)
            elif opc == 5:
                break
            else:
                print('ERRO, OPÇÃO INVALIDA')
                break