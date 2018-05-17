# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from itertools import product

from model.AF.Estado import Estado
from model.exception.AFNDError import AFNDError

'''
    Classe que representa um autômato finito.
'''
class AutomatoFinito:

    '''
        Método construtor.
    '''
    def __init__(self, determinizado = False):
        self.__producoes = {} # conjunto de transições
        self.__estado_inicial = None
        self.__estados_finais = set()
        self.__vt = set() # conjunto de símbolos terminais
        self.__determinizado = determinizado

    '''
        Adiciona uma nova produção para um estado a partir de um simbolo terminal.
        \:param estado é um símbolo não-terminal (ou um conjunto deles).
        \:param caractere é um simbolo terminal.
        \:param destino é um simbolo não-terminal (ou um conjunto deles).s
    '''
    def adiciona_transicao(self, estado, caractere, destino):
        self.__vt.add(caractere)
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
        gramatica.set_simbolo_inicial(self.__estado_inicial.to_string())

        # Construção das produções de acordo com os itens A e B do algoritmo visto em aula
        for b in self.__producoes.keys():
            producoes_af = self.__producoes[b]
            producoes_g = []
            for a in producoes_af.keys():
                for c in producoes_af[a]:
                    c_string = c.to_string()
                    if c_string != "-":
                        producoes_g.append((a, c_string))
                        if c in self.__estados_finais:
                            producoes_g.append((a, "&"))
            b = b.to_string()
            gramatica.adiciona_producao(b, producoes_g)

        # Item C do algoritmo visto em aula
        # Se & pertence à linguagem
        if self.__estado_inicial in self.__estados_finais:
            simbolo_novo = gramatica.novo_simbolo()

            # Copia produções do estado inicial atual
            producoes_novo_si = [] # lista de tuplas

            producoes_si = gramatica.get_producoes()[self.__estado_inicial.to_string()]
            for p in producoes_si:
                producoes_novo_si.append(p)

            # Adiciona produção de & para o novo símbolo inicial
            producoes_novo_si.append(("&", "&"))

            gramatica.adiciona_producao(simbolo_novo, producoes_novo_si)
            # Atualiza o símbolo inicial
            gramatica.set_simbolo_inicial(simbolo_novo)
        return gramatica

    '''
        Verifica se a sentença dada pertence à linguagem reconhecida pelo AFD.
        \:param sentenca é a sentença a ser verificada.
        \:return True se a sentença é reconhecida pelo autômato e False caso contrário.
    '''
    def reconhece_sentenca(self, sentenca):

        if not self.isAFND():
            estados = self.__producoes[self.__estado_inicial]
            tamanho_sentenca = len(sentenca)

            if tamanho_sentenca == 0 or (tamanho_sentenca == 1 and sentenca[0] == "&"):
                if self.__estado_inicial in self.__estados_finais:
                    return True

            for index in range(tamanho_sentenca):
                simbolo = sentenca[index]
                if simbolo in estados:
                    transicoes = estados[simbolo]
                    if index == tamanho_sentenca-1:
                        for t in transicoes:
                            if t in self.__estados_finais:
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
        else:
            raise AFNDError("reconhecimento de sentença.")

    '''
        Retorna todas as sentenças reconhecidas pelo autômato do tamanho indicado pelo parâmetro.
        \:param tamanho é o tamanho das sentenças reconhecidas.
        \:return uma lista de strings com as sentenças reconhecidas pelo autômato. Se nenhuma senteça do tamanho dado for reconhecida, a lista será vazia.
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
                sentencas_reconhecidas.append(''.join(s))
        return sentencas_reconhecidas

    '''
        
    '''
    def determiniza(self):
        if self.isAFND():
            af = AutomatoFinito(True) # Indica que o autômato é determinizado
            af.set_vt(self.__vt)
            af.set_estado_inicial(self.__estado_inicial)

            estados_visitados = set()
            estados_criados = set()
            estados_criados.add(self.__estado_inicial)
            estados_finais = set()
            estados_a_visitar = set()
            estados_a_visitar.add(self.__estado_inicial)

            while len(estados_a_visitar) != 0:
                estado = estados_a_visitar.pop()
                estados_visitados.add(estado)
                for simbolo in self.__vt:
                    nova_transicao = []
                    for i in estado.to_list():
                        e = Estado(i)
                        if e in self.__estados_finais:
                            estados_finais.add(estado)
                        if len(self.__producoes[e]) != 0:
                            if simbolo in self.__producoes[e]:
                                transicoes = self.__producoes[e][simbolo]
                                for t in transicoes:
                                    nova_transicao.append(t.to_string())
                    nova_transicao = Estado(nova_transicao)
                    af.adiciona_transicao(estado, simbolo, nova_transicao)
                    estados_criados.add(nova_transicao)
                estados_a_visitar = estados_criados - estados_visitados
            af.set_estados_finais(list(estados_finais))
            return af
        else:
            raise Exception("O autômato já é um autômato finito determinístico.")
    '''
        Verifica se o autômato é um autômato finito não determinístico (AFND).
        \:return True se o autômato for um AFND ou False caso contrário.
    '''
    def isAFND(self):

        if self.__determinizado:
            return False

        for estado in self.__producoes:
            transicoes = self.__producoes[estado]
            for t in transicoes:
                if len(transicoes[t]) > 1: # Se tem mais de uma transição para um símbolo
                    return True
                if t == "&" and len(transicoes.keys()) > 1: # Se tem &-transição e mais outras transições através de outros símbolos
                    return True
        return False

    '''
        Verifica se o autômato é completo, ou seja, contém transições para todos os símbolos em cada estado.
        \:return True se o autômato for completo ou False caso contrário.
    '''
    def isComplete(self):
        return True

    '''
        Transforma o autômato em uma matriz de strings.
        A primeira linha é composta pelos símbolos terminais do autômato e as linhas seguintes representam as transições para cada símbolo não terminal.
        \:return uma matriz de strings.
    '''
    # TODO - diferente para quando o autômato for determinizado(aparece os estados com[])
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
            print(y.to_string())

        print("xxxxxxx")
        print()