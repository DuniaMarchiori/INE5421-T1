# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]

from model.AF.Estado import Estado
from model.exception.FormatError import FormatError
from string import ascii_uppercase
import re

'''
    Classe que representa uma gramática regular.
'''
class Gramatica:
    __numero = 1 # id do arquivo salvo

    '''
        Método construtor.
    '''
    def __init__(self):
        self.__producoes = {}
        self.__texto = None
        self.__simbolo_inicial = None
        self.__vt = set() # conjunto de símbolos terminais
        self.__vn_dir = set() # conjunto de símbolos não-terminais que aparecem na parte direita das produções

    '''
        Modifica o símbolo inicial da gramática.
        \:param simbolo é o novo símbolo inicial.
    '''
    def set_simbolo_inicial(self, simbolo):
        self.__simbolo_inicial = simbolo

    '''
        Adiciona uma nova produção.
        \:param chave é o símbolo não-terminal.
        \:param producao é uma lista de tuplas no formato (símbolo terminal, símbolo não-terminal)
    '''
    def adiciona_producao(self, chave, producao):
        self.__producoes[chave] = producao

    '''
        Retorna o conjunto de produções da gramática.
        \:return um dicionário onde a chave é um não-terminal e os dados são tuplas no formato (símbolo terminal, símbolo não-terminal)
    '''
    def get_producoes(self):
        return self.__producoes

    '''
        Modifica o conjunto de símbolos terminais da gramática.
        \:param vt é o novo conjunto de símbolos terminais.
    '''
    def set_vt(self, vt):
        self.__vt = vt

    '''
        Retorna o conjunto de símbolos terminais da gramática.
        \:return o conjunto de símbolos terminais da gramática.
    '''
    def get_vt(self):
        return self.__vt

    '''
        Salva a gramática em um arquivo .txt.
        \:param texto é a string da gramática a ser salva.
        \:return o nome do arquivo .txt salvo
    '''
    def salvar(self, texto):
        nome_arquivo = "gramatica_" + str(self.__numero) + ".txt"
        file = open(nome_arquivo, "w")
        file.write(texto)
        file.close()
        self.__numero += 1
        self.__texto = texto
        return nome_arquivo

    '''
        Gera a estrutura da gramática a partir do texto escrito pelo usuário.
        \:param texto é o texto informado pelo usuário.
        \:return True caso a estrutura seja gerada com sucesso e False caso contrário.
    '''
    def parse(self, texto):
        self.__texto = texto.replace(" ", "") # Retira todos os espaços em branco
        linhas = self.__texto.splitlines()
        self.__gera_estrutura_producoes(linhas)
        return True

    '''
        Gera a estrutura da gramática a partir do texto informado pelo usuário.
        \:param lista é a lista de produções da gramática em texto
    '''
    def __gera_estrutura_producoes(self, linhas):
        i = 0
        RE_D = re.compile('\d')

        for linha in linhas:
            if linha.__contains__("->"):
                l = linha.split("->") # Separa entre o lado esquerdo e direito do "->"
                if len(l) <= 2:
                    chave = l[0] # Símbolo não terminal do lado esquerdo
                    if i == 0:
                        self.__simbolo_inicial = chave # Define o símbolo inicial
                        i += 1
                    producoes = []
                    prod = l[1].split("|") # Separa as produções
                    for p in prod:
                        if len(p) == 1:
                            if (p.islower() or p == "&" or self.is_int(p)): # Produção é um símbolo terminal
                                producoes.append((p, "&"))
                                if p != "&":
                                    self.__vt.add(p)
                            else:
                                raise FormatError(FormatError.FORMAT_ERROR + str(linhas.index(linha)+1) + ": as produções regulares devem seguir o formato aB, onde a é um símbolo terminal e B um símbolo não terminal.")
                        elif len(p) != 0:
                            chars = list(p)
                            terminal = chars[0] # caractere terminal
                            nao_terminal = chars[1:len(chars)] # caracteres não-terminais
                            all_upper = True if True in [s.isupper() for s in nao_terminal] else False # Todos os caracteres do símbolo não-terminal são maiúsculos
                            all_letters = True # Não há números no símbolo
                            for s in nao_terminal:
                                search = RE_D.search(s) # pesquisa através de expressão regular
                                all_letters &= (search == None) # se search == None então não há números no símbolo

                            # Produção é um símbolo terminal seguido de um não-terminal (que pode ter tamanho maior que um, mas todos os caracteres maíusculos)
                            if (( terminal.islower() or self.is_int(terminal)) and all_upper and all_letters):
                                simbolo_nt = ''.join(nao_terminal)
                                producoes.append((terminal, simbolo_nt))
                                self.__vt.add(terminal)
                                self.__vn_dir.add(simbolo_nt)
                            else:
                                raise FormatError(FormatError.FORMAT_ERROR + str(linhas.index(linha)+1) + ": as produções regulares devem seguir o formato aB, onde a é um símbolo terminal e B um símbolo não terminal.")
                else:
                    raise FormatError(FormatError.FORMAT_ERROR + str(linhas.index(linha)+1) + ": ocorre mais de um símbolo '->' por produção. Cada produção deve estar em uma linha.")

                self.__producoes[chave] = producoes
            else:
                raise FormatError(FormatError.FORMAT_ERROR + str(linhas.index(linha)+1) + ": produção não apresenta o símbolo '->'")

        # Símbolo não-terminal referenciado não tem produções
        for vn in self.__vn_dir:
            if vn not in self.__producoes:
                raise FormatError("A gramática referencia símbolos não terminais com produções não definidas: " + vn)

    '''
        Transforma a gramática em um autômato finito.
        \:return o autômato finito que reconhece a mesma linguagem que a gramática gera.
    '''
    def transformar_em_AF(self):
        from model.AF.AutomatoFinito import AutomatoFinito

        af = AutomatoFinito()
        af.set_vt(self.__vt)
        af.set_estado_inicial(Estado(self.__simbolo_inicial))

        # Gera um símbolo novo
        simbolo_novo = self.novo_simbolo()

        if simbolo_novo != None:
            # Construção do conjunto de símbolos finais
            simbolos_finais = []
            simbolos_finais.append(Estado(simbolo_novo))
            # S -> & pertence à P
            producoes_iniciais = self.__producoes[self.__simbolo_inicial]
            for p in producoes_iniciais:
                if p[0] == "&":
                    simbolos_finais.append(Estado(self.__simbolo_inicial))
            af.set_estados_finais(simbolos_finais)

            # Construção das produções
            # chave é um Estado
            #produção: é um dicionario: chave -> terminal, value -> Estado

            for k in self.__producoes.keys():
                b = Estado(k)

                producoes_g = self.__producoes[k]
                for p in producoes_g:
                    a = p[0]
                    c = p[1]
                    if a != "&":
                        if c == "&":
                            e = Estado(simbolo_novo)
                        else:
                            e = Estado(c)
                        af.adiciona_transicao(b, a, e)

            # Transições indefinidas para o símbolo novo
            chave = Estado(simbolo_novo)
            af.adiciona_estado(chave)

            return af
        else:
            pass #não tem mais letras no alfabeto possiveis pra ser o novo simbolo

    '''
        Verifica se a string representa um número inteiro.
        \:param str é a string a ser verificada
        \:return True se a string representar um número inteiro e False caso contrário.
    '''
    def is_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    '''
        Gera um novo símbolo não terminal que não pertence à gramática.
        \:return um símbolo não terminal que não pertence à gramática.
    '''
    def novo_simbolo(self):
        simbolo_novo = None
        for letra in ascii_uppercase:
            if letra not in self.__producoes:
                simbolo_novo = letra
                break
        # Se todas as letras do alfabeto já fazem parte do conjunto de símbolos terminais,
        # então o símbolo novo recebe a concatenação de duas letras (que não exista no conjunto)
        if simbolo_novo == None:
            found = False
            for l1 in ascii_uppercase:
                for l2 in ascii_uppercase:
                    letras = l1 + l2
                    if letras not in self.__producoes:
                        simbolo_novo = letras
                        found = True
                        break
                if found:
                    break
        return simbolo_novo

    '''
        Transforma a gramática em texto.
        \:return uma string que representa a gramática.
    '''
    def to_string(self):
        if self.__texto != None:
            return self.__texto
        else:
            gramatica = ""
            producao_inicial = ""
            outras_producoes = ""

            for s in self.__producoes.keys():
                texto = ""
                texto += s + " -> "
                producoes_s = self.__producoes[s]
                for i in range(len(producoes_s)):
                    if i > 0:
                        texto += " | "

                    prod = producoes_s[i]
                    if prod[1] != "&":
                        texto = texto + ''.join(prod)
                    else:
                        texto = texto + prod[0]
                if s == self.__simbolo_inicial:
                    producao_inicial += texto
                else:
                    outras_producoes += texto + "\n"

            gramatica += producao_inicial + "\n" + outras_producoes
            return gramatica

    '''
        Exibe as estruturas da gramática no console.
    '''
    def printa(self):
        print("VT:")
        for x in self.__vt:
            print(x)

        print("-------")
        print("VNT:")
        for x in self.__vn_dir:
            print(x)

        print("-------")
        print("Produções:")
        for k in self.__producoes.keys():
            print(k)
            print(self.__producoes[k])

        print("xxxxxxx")
        print()