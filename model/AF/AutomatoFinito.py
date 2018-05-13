'''
    Classe que representa um autômato finito.
'''
from itertools import product

from model.AF.Estado import Estado


class AutomatoFinito:

    '''
        Método construtor.
    '''
    def __init__(self):
        self.__producoes = {} # conjunto de transições
        self.__estado_inicial = None
        self.__estados_finais = []
        self.__vt = set() # conjunto de símbolos terminais

    '''
        Adiciona uma nova produção para um estado a partir de um simbolo terminal.
        \:param estado é um símbolo não-terminal (ou um conjunto deles).
        \:param caractere é um simbolo terminal.
        \:param destino é um simbolo não-terminal (ou um conjunto deles).s
    '''
    def adiciona_transicao(self, estado, caractere, destino):
        self.__producoes.setdefault(estado, {})
        self.__producoes[estado].setdefault(caractere, [])
        self.__producoes[estado][caractere].append(destino)

    '''
        Adiciona uma novo estado.
        \:param estado é um símbolo não-terminal (ou um conjunto deles).
    '''
    def adiciona_estado(self, estado):
        self.__producoes.setdefault(estado, {})

    '''
        Retorna o conjunto de transições do autômato.
        \:return um dicionário onde a chave é um estado e os dados são 
            um dicionário onde a chave é um símbolo não terminal e os dados são um conjunto de símbolos não-terminais (pode ser vazio).
    '''
    def get_transicoes(self):
        return self.__producoes

    '''
        Modifica o estado inicial do autômato.
        \:param estado é o novo estado inicial.
    '''
    def set_estado_inicial(self, estado):
        self.__estado_inicial = estado

    '''
        Modifica o conjunto de estados finais do autômato.
        \:param lista é a lista de novos estados finais.
    '''
    def set_estados_finais(self, lista):
        self.__estados_finais = lista

    '''
        Modifica o conjunto de símbolos terminais do autômato.
        \:param vt é o novo conjunto de símbolos terminais.
    '''
    def set_vt(self, vt):
        self.__vt = vt

    '''
        Retorna o conjunto de símbolos terminais do autômato.
        \:return o conjunto de símbolos terminais do autômato.
    '''
    def get_vt(self):
        return self.__vt

    '''
        Transforma um autômato finito em uma gramática.
        \:return a gramática que gera a mesma linguagem que o autômato reconhece.
    '''
    def transforma_em_GR(self):
        from model.Gramatica import Gramatica

        gramatica = Gramatica()
        gramatica.set_vt(self.__vt)
        gramatica.set_simbolo_inicial(self.__estado_inicial)

        # Construção das produções de acordo com os itens A e B do algoritmo visto em aula
        for b in self.__producoes.keys():
            producoes_af = self.__producoes[b]
            producoes_g = []
            for a in producoes_af.keys():
                for c in producoes_af[a]:
                    c = c.to_string()
                    if c != "-":
                        producoes_g.append((a, c))
                        if c in self.__estados_finais:
                            producoes_g.append((a, "&"))
            b = b.to_string()
            gramatica.adiciona_producao(b, producoes_g)

        # Item C do algoritmo visto em aula
        # Se & pertence à linguagem
        if self.__estado_inicial in self.__estados_finais:
            simbolo_novo = gramatica.novo_simbolo()

            # Copia produções do estado inicial atual
            si = Estado(self.__estado_inicial)
            producoes_novo_si = [] # lista de tuplas

            producoes_si = gramatica.get_producoes()[si.to_string()]
            for p in producoes_si:
                producoes_novo_si.append(p)

            # Adiciona produção de & para o novo símbolo inicial
            producoes_novo_si.append(("&", "&"))

            gramatica.adiciona_producao(simbolo_novo, producoes_novo_si)
            # Atualiza o símbolo inicial
            gramatica.set_simbolo_inicial(simbolo_novo)
        return gramatica

    '''
            
    '''
    def reconhece_sentenca(self, sentenca):
        sentenca_lista = list(sentenca)
        estados = self.__producoes[Estado(self.__estado_inicial)]
        tamanho_lista = len(sentenca_lista)

        if tamanho_lista == 0 or (tamanho_lista == 1 and sentenca_lista[0] == "&"):
            if self.__estado_inicial in self.__estados_finais:
                return True

        for index in range(tamanho_lista):
            simbolo = sentenca_lista[index]
            if simbolo in estados:
                transicoes = estados[simbolo]
                if index == len(sentenca_lista)-1:
                    for t in transicoes:
                        if (t.to_string() in self.__estados_finais):
                            return True
            else:
                return False
            # Copia produções dos próximos estados
            estados = {}
            for t in transicoes:
                for x in self.__producoes[t]:
                    estados.setdefault(x, [])
                    for y in self.__producoes[t][x]:
                        estados[x].append(y)
            index = index + 1
        return False

    '''
        
    '''
    def enumera_sentencas(self, tamanho):
        sentencas_reconhecidas = []
        vt = list(self.__vt)
        combinacoes = []

        if tamanho != 0:
            combinacoes = product(vt, repeat=tamanho)
        else:
            combinacoes.append("&")

        for s in combinacoes:
            if self.reconhece_sentenca(s):
                sentencas_reconhecidas.append(s)
        return sentencas_reconhecidas

    '''
        Transforma o autômato em uma matriz de strings.
        A primeira linha é composta pelos símbolos terminais do autômato e as linhas seguintes representam as transições para cada símbolo não terminal.
        \:return uma matriz de strings.
    '''
    def to_string(self):
        matriz =[]
        primeira_prod = []

        vt = list(self.__vt)
        vt = sorted(vt, key=str.lower)
        vt.insert(0, "")
        matriz.append(vt)
        vt = list(self.__vt)
        vt = sorted(vt, key=str.lower)
        for p in self.__producoes:
            linha = []
            simbolo = p.to_list()
            simb_inicial = self.__estado_inicial in simbolo
            simb_final = False
            for s in simbolo:
                simb_final = simb_final or s in self.__estados_finais
            simbolo = ''.join(simbolo)
            if simb_inicial:
                simbolo = "->" + simbolo
            if simb_final:
                simbolo = "*" + simbolo
            linha.append(simbolo)
            prod = self.__producoes[p]
            for x in vt:
                if x in prod:
                    lista_estados = []
                    for estado in prod[x]:
                        lista_estados.append(estado.to_string())
                    linha.append(lista_estados)
                else:
                    estado = ["-"]
                    linha.append(estado)
            if simb_inicial:
                primeira_prod = linha
            else:
                matriz.append(linha)
        matriz.insert(1, primeira_prod)
        return matriz

    '''
        Exibe as estruturas do autômato no console.
    '''
    def printa(self):
        print("VT:")
        for x in self.__vt:
            print(x)

        print("-------")
        print("Produções:")
        for k in self.__producoes.keys():
            print(k.to_string())
            prod = ""
            for x in self.__producoes[k]:
                est = ""
                for y in self.__producoes[k][x]:
                    y = y.to_string()
                    est += y + " , "
                prod += x + ": " + est
            print("{ " + prod + " }")

        print("-------")
        print("Estados finais:")
        for y in self.__estados_finais:
            print(y)

        print("xxxxxxx")
        print()