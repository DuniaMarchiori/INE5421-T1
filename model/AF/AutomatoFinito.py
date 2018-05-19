# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from itertools import product
from model.AF.Estado import Estado
from string import ascii_uppercase
from model.exception.AFNDError import AFNDError
from model.Elemento import *

'''
    Classe que representa um autômato finito.
'''
class AutomatoFinito(Elemento):

    '''
        Método construtor.
    '''
    def __init__(self, nome, determinizado = False):
        super(AutomatoFinito, self).__init__(TipoElemento.AF, nome)
        self.__producoes = {} # conjunto de transições
        self.__estado_inicial = None
        self.__estados_finais = set()
        self.__vt = set() # conjunto de símbolos terminais
        self.__determinizado = determinizado
        if determinizado:
            self.__deterministico = True
        else:
            self.__deterministico = None

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

        gramatica = Gramatica(self.get_nome() + " (convertido para GR)")
        gramatica.set_vt(self.__vt)
        gramatica.set_simbolo_inicial(self.__estado_inicial.to_string())

        # Construção das produções de acordo com os itens A e B do algoritmo visto em aula
        for b in self.__producoes.keys():
            producoes_af = self.__producoes[b]
            producoes_g = []
            for a in producoes_af.keys():
                if a != "&":
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
            index = 0
            estados = self.__producoes[self.__estado_inicial]
            tamanho_sentenca = len(sentenca)

            if tamanho_sentenca == 0 or (tamanho_sentenca == 1 and sentenca[0] == "&"):
                if self.__estado_inicial in self.__estados_finais:
                    return True

            while index < tamanho_sentenca:
                simbolo = sentenca[index]
                transicoes = []
                if "&" in estados:
                    for t in estados["&"]:
                        if t.to_string() != "&":
                            transicoes.append(t)
                if (simbolo in estados):
                    for x in estados[simbolo]:
                        transicoes.append(x)
                    if index == tamanho_sentenca-1:
                        for t in transicoes:
                            if t in self.__estados_finais:
                                return True
                    index = index + 1
                else:
                    if len(transicoes) == 0:
                        return False
                # Copia produções dos próximos estados
                estados = {}
                for t in transicoes:
                    for x in self.__producoes[t]:
                        estados.setdefault(x, [])
                        for y in self.__producoes[t][x]:
                            estados[x].append(y)
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
        vt = list(self.__vt - set("&"))
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
        Determiniza este autômato e o retorna como um autômato novo.
        \:return o autômato determinizado.
    '''
    def determiniza(self):
        if self.isAFND():
            af = AutomatoFinito(self.get_nome() + " (determinizado)", True) # Indica que o autômato é determinizado
            af.set_vt(self.__vt)
            af.set_estado_inicial(self.__estado_inicial)

            estados_finais = set() # Conjuntos de estados finais do novo autômato
            estados_visitados = set()
            estados_criados = set()
            estados_criados.add(self.__estado_inicial)
            estados_a_visitar = set()
            estados_a_visitar.add(self.__estado_inicial)

            while len(estados_a_visitar) != 0: # Se ainda há estados a visitar
                estado = estados_a_visitar.pop()
                estados_visitados.add(estado)
                for simbolo in self.__vt:
                    nova_transicao = []
                    for i in estado.to_list(): # Em um autômato determinizado, um estado do autômato pode ser composto por mais de um estado do autômato anterior
                        e = Estado(i)
                        if e in self.__estados_finais:
                            estados_finais.add(estado)
                        if len(self.__producoes[e]) != 0:
                            if simbolo in self.__producoes[e]: # Se á produções desse estado a partir do símbolo não terminal sendo analisado
                                transicoes = self.__producoes[e][simbolo]
                                for t in transicoes:
                                    nova_transicao.append(t.to_string())
                    if len(nova_transicao) != 0: # Se há produções a partir desse estado
                        nova_transicao = Estado(nova_transicao)
                        af.adiciona_transicao(estado, simbolo, nova_transicao) # Adiciona a transição ao novo autômato
                        estados_criados.add(nova_transicao)
                    else:
                        af.adiciona_estado(estado) # Se não há produções a partir desse estado, cria um estado com produções vazias
                estados_a_visitar = estados_criados - estados_visitados
            af.set_estados_finais(list(estados_finais))
            return af
        else:
            raise Exception("O autômato já é um autômato finito determinístico.")

    '''
        Minimiza este autômato.
        \:return o autômato mínimo deste autômato.
    '''
    def minimiza(self):
        estados = set(self.__producoes.keys())
        estados_inuteis = self.estados_inacessiveis().union(self.estados_mortos())
        estados = estados - estados_inuteis

        estado_indefinicao = self.novo_estado()
        transicoes_indef = {}
        lista = [estado_indefinicao]
        for simbolo in self.__vt:
            transicoes_indef[simbolo] = lista
        self.__producoes[estado_indefinicao] = transicoes_indef # Item adicionado apenas para auxiliar na minimização

        k_f = estados - self.__estados_finais
        k_f.add(estado_indefinicao)
        f = estados - k_f

        ce_k_f_anterior = []
        ce_f_anterior = []
        novo_ce_k_f = [k_f]
        novo_ce_f = [f]

        # Forma os conjuntos equivalentes
        while ce_k_f_anterior != novo_ce_k_f or ce_f_anterior != novo_ce_f:
            ce_k_f_anterior = list(novo_ce_k_f)
            ce_f_anterior = list(novo_ce_f)
            ce = ce_k_f_anterior + ce_f_anterior

            # K-F
            for conjunto in ce_k_f_anterior:
                estado = next(iter(conjunto))
                set_e = set()
                set_e.add(estado)
                for outro_estado in conjunto - set_e:
                    if not self.__estados_equivalentes(estado, outro_estado, ce, estado_indefinicao):
                        adicionado = False
                        for outro_set in novo_ce_k_f:
                            if outro_set != conjunto:
                                e = next(iter(outro_set))
                                if self.__estados_equivalentes(outro_estado, e, ce, estado_indefinicao):
                                    outro_set.add(outro_estado)
                                    adicionado = True
                                    break
                            else:
                                outro_set.remove(outro_estado)
                        if not adicionado:
                            set_outro_estado = set()
                            set_outro_estado.add(outro_estado)
                            novo_ce_k_f.append(set_outro_estado)

            # F
            for conjunto in ce_f_anterior:
                estado = next(iter(conjunto))
                set_e = set()
                set_e.add(estado)
                for outro_estado in conjunto - set_e:
                    if not self.__estados_equivalentes(estado, outro_estado, ce, estado_indefinicao):
                        adicionado = False
                        for outro_set in novo_ce_f:
                            if outro_set != conjunto:
                                e = next(iter(outro_set))
                                if self.__estados_equivalentes(outro_estado, e, ce, estado_indefinicao):
                                    outro_set.add(outro_estado)
                                    adicionado = True
                                    break
                            else:
                                outro_set.remove(outro_estado)
                        if not adicionado:
                            set_outro_estado = set()
                            set_outro_estado.add(outro_estado)
                            novo_ce_f.append(set_outro_estado)

        # Constrói o autômato
        ce = novo_ce_k_f + novo_ce_f
        af_minimo = AutomatoFinito(self.get_nome() + " (minimizado)")
        af_minimo.set_vt(self.__vt)

        # Estado inicial
        for e in ce:
            if self.__estado_inicial in e:
                index = ce.index(e)
                nome_estado = "q" + str(index)
                af_minimo.set_estado_inicial(Estado(nome_estado))
                break

        # Estados finais
        estados_finais = set()
        for e in novo_ce_f:
            index = ce.index(e)
            nome_estado = "q" + str(index)
            estados_finais.add(Estado(nome_estado))
        af_minimo.set_estados_finais(estados_finais)

        # Produções
        ce_indefinido =  self.__get_ce_respectivo(ce, estado_indefinicao)
        for estado in self.__producoes:
            nome_estado = self.__get_ce_respectivo(ce, estado)
            transicoes = self.__producoes[estado]
            for simbolo in self.__vt:
                if simbolo in transicoes:
                    estado_t = transicoes[simbolo]
                    nome_estado_t = self.__get_ce_respectivo(ce, estado_t[0])
                    af_minimo.adiciona_transicao(Estado(nome_estado), simbolo, Estado(nome_estado_t))
                else:
                    af_minimo.adiciona_transicao(Estado(nome_estado), simbolo, Estado(ce_indefinido))

        del self.__producoes[estado_indefinicao] # Deleta a entrada auxiliar

        return af_minimo

    '''
        Determina a qual conjunto de equivalência o estado pertence durante o processo de minimização.
        \:param ce é o conjunto total de conjuntos de equivalência.
        \:param estado é o estado que se deseja determinar o conjunto a qual ele pertence.
        \:return o nome do estado que representa o conjunto de equivalência.
    '''
    def __get_ce_respectivo(self, ce, estado):
        for e in ce:
            if estado in e:
                index = ce.index(e)
                return "q" + str(index)

    '''
        Determina se dois estados são equivalentes de acordo com os conjuntos de equivalência no processo de minimização.
        \:param estado é um dos dois estados usados na comparação.
        \:param outro_estado é o segundo estado usado na comparação.
        \:param ce é o conjunto total de conjuntos de equivalência.
        \:param estado_indefinicao é o estado criado para representar a indefinicao no autômato.
        \:return True se os dois estados são equivalentes e False caso não sejam.
    '''
    def __estados_equivalentes(self, estado, outro_estado, ce, estado_indefinicao):
        for simbolo in self.__vt:
            if simbolo in self.__producoes[estado]:
                transicao_estado = self.__producoes[estado][simbolo]
            else:
                transicao_estado = [estado_indefinicao]

            if simbolo in self.__producoes[outro_estado]:
                transicao_outro_estado = self.__producoes[outro_estado][simbolo]
            else:
                transicao_outro_estado = [estado_indefinicao]

            ce_estado = self.__get_ce_respectivo(ce, transicao_estado[0])
            ce_outro_estado = self.__get_ce_respectivo(ce, transicao_outro_estado[0])
            if ce_estado != ce_outro_estado:
                return False

        return True

    '''
        Identifica os estados inacessíveis do autômato, ou seja, estados em que não é possível chegar a partir do estado inicial.
        \:return o conjunto de estados inacessíveis.
    '''
    def estados_inacessiveis(self):
        estados_alcancados = set()
        estados_alcancados.add(self.__estado_inicial)
        estados_a_visitar = estados_alcancados

        while len(estados_a_visitar) != 0:
            estados_com_transicao = set()
            for estado in estados_a_visitar:
                for simbolo in self.__producoes[estado]:
                    transicoes = self.__producoes[estado][simbolo]
                    for t in transicoes:
                        estados_com_transicao.add(t)
            estados_alcancados = estados_alcancados.union(estados_com_transicao)
            estados_a_visitar = estados_com_transicao

        return set(self.__producoes.keys() - estados_alcancados)

    '''
        Identifica os estados mortos do autômato, ou seja, estados que não têm caminho que levem a um estado final a partir deles.
        \:return o conjunto de estados mortos.
    '''

    def estados_mortos(self):
        vivos_atuais = self.__estados_finais
        vivos_anteriores = set()

        while vivos_atuais != vivos_anteriores:
            vivos_anteriores = vivos_atuais
            estados_com_transicao = set()
            for estado in self.__producoes.keys() - vivos_atuais:
                for simbolo in self.__producoes[estado]:
                    transicoes = self.__producoes[estado][simbolo]
                    for t in transicoes:
                        if t in vivos_anteriores:
                            estados_com_transicao.add(estado)
            vivos_atuais = vivos_anteriores.union(estados_com_transicao)

        return set(self.__producoes.keys() - vivos_atuais)

    '''
        Verifica se o autômato é um autômato finito não determinístico (AFND).
        \:return True se o autômato for um AFND ou False caso contrário.
    '''
    def isAFND(self):

        if self.__deterministico != None:
            return not self.__deterministico

        self.__deterministico = True
        for estado in self.__producoes:
            transicoes = self.__producoes[estado]
            for t in transicoes:
                if len(transicoes[t]) > 1: # Se tem mais de uma transição para um símbolo
                    self.__deterministico = False
                if t == "&" and len(transicoes.keys()) > 1 and estado != self.__estado_inicial: # Se tem &-transição e mais outras transições através de outros símbolos
                    self.__deterministico = False
        return not self.__deterministico

    '''
        Verifica se o autômato é completo, ou seja, contém transições para todos os símbolos em cada estado.
        \:return True se o autômato for completo ou False caso contrário.
    '''
    def isComplete(self):
        # TODO
        return True

    '''
        Gera um novo símbolo não terminal que não pertence à gramática.
        \:return um símbolo não terminal que não pertence à gramática.
    '''
    def novo_estado(self):
        simbolo_novo = None
        for letra in ascii_uppercase:
            if Estado(letra) not in self.__producoes:
                simbolo_novo = letra
                break
        # Se todas as letras do alfabeto já fazem parte do conjunto de símbolos terminais,
        # então o símbolo novo recebe a concatenação de duas letras (que não exista no conjunto)
        if simbolo_novo == None:
            found = False
            for l1 in ascii_uppercase:
                for l2 in ascii_uppercase:
                    letras = l1 + l2
                    if Estado(letras) not in self.__producoes:
                        simbolo_novo = letras
                        found = True
                        break
                if found:
                    break
        return Estado(simbolo_novo)

    '''
        Transforma o autômato em uma matriz de strings.
        A primeira linha é composta pelos símbolos terminais do autômato e as linhas seguintes representam as transições para cada símbolo não terminal.
        \:return uma matriz de strings.
    '''
    def to_matrix(self):
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
            simb_inicial = self.__estado_inicial == Estado(simbolo)
            simb_final = p in self.__estados_finais

            if self.__determinizado:
                simbolo = ','.join(simbolo)
                simbolo = "[" + simbolo + "]"
            else:
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
                        if not self.__determinizado:
                            lista_estados.append(estado.to_string())
                        else:
                            lista_estados.append(estado.to_string_com_virgula())
                    linha.append(", ".join(lista_estados))
                else:
                    estado = "-"
                    linha.append(estado)
            if simb_inicial:
                primeira_prod = linha
            else:
                matriz.append(linha)

        matriz.insert(1, primeira_prod)
        return matriz

    def to_string(self):
        matriz = self.to_matrix()
        string = []

        maior_estado = self.__maior_estado_na_coluna(matriz, 0)
        for i in range(0, len(matriz)):
            estado = matriz[i][0]
            nome_estado = (" "*(maior_estado-len(estado))) + estado
            string.append(nome_estado)
        if self.__determinizado:
            string[0] += " "

        for i in range(1, len(matriz[0])):
            maior_estado_coluna = self.__maior_estado_na_coluna(matriz, i)
            s = matriz[0][i]
            if self.__determinizado:
                s = " " + s + " "
            string[0] += "   " + (" "*(maior_estado_coluna-len(s))) + s
            for j in range(1, len(matriz)):
                estado = matriz[j][i]
                if self.__determinizado:
                    estado = "[" + estado + "]"
                string[j] += " | " + (" "*(maior_estado_coluna-len(estado))) + estado

        string_final = ""
        for linha in string:
            string_final += linha + "\n"
        return string_final

    def __maior_estado_na_coluna(self, matriz_de_strings, coluna):
        maior_estado = 0
        for i in range(0, len(matriz_de_strings)):
            estado = matriz_de_strings[i][coluna]
            if self.__determinizado:
                estado = "[" + estado + "]"
            if len(estado) > maior_estado:
                maior_estado = len(estado)
        return maior_estado

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