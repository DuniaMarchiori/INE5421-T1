from model.AutomatoFinito import AutomatoFinito
from model.exception.FormatError import FormatError
from string import ascii_uppercase


class Gramatica:
    __numero = 1

    def __init__(self):
        self.__producoes = {}
        self.__texto = None
        self.__simbolo_inicial = None
        self.__simbolos_finais = []
        self.__vt = set()

    def set_simbolo_inicial(self, simbolo):
        self.__simbolo_inicial = simbolo

    def adiciona_producao(self, chave, producao):
        self.__producoes[chave] = producao

    def get_producoes(self):
        return self.__producoes

    def get_texto(self):
        return self.__texto

    def set_vt(self, vt):
        self.__vt = vt

    def get_vt(self):
        return self.__vt

    def salvar(self, texto):
        nome_arquivo = "gramatica_" + str(self.__numero) + ".txt"
        file = open(nome_arquivo, "w")
        file.write(texto)
        file.close()
        self.__numero += 1
        return nome_arquivo

    def abrir(self, nome_arquivo):
        file = open(nome_arquivo, "r")
        self.__texto = file.read()
        file.close()
        g = self.ler(self.__texto)
        self.gera_estrutura_producoes(g)
        return g

    def ler(self, texto):
        return texto.splitlines()

    def gera_estrutura_producoes(self, lista):
        i = 0

        for linha in lista:
            if linha.__contains__("->"):
                l = linha.split("->") # Separa entre o lado esquerdo e direito do "->"
                chave = l[0].strip() # Símbolo não terminal do lado esquerdo (.strip() tira os espaços)
                if i == 0:
                    self.__simbolo_inicial = chave
                    i += 1
                producoes = []
                prod = l[1].split("|") # Separa as produções
                for p in prod:
                    p = p.strip()
                    if len(p) == 1:
                        if (p.islower() or p == "&" or self.is_int(p)): # Produção é um símbolo terminal
                            producoes.append((p, "&"))
                            if p != "&":
                                self.__vt.add(p)
                        else:
                            raise FormatError("A gramática não segue o formato padrão de produções.")
                    elif len(p) == 2:
                        chars = list(p)
                        if (( chars[0].islower() or self.is_int(chars[0])) and chars[1].isupper()): # Produção é um símbolo terminal seguido de um não-terminal
                            producoes.append((chars[0], chars[1]))
                            self.__vt.add(chars[0])
                        else:
                            raise FormatError("A gramática não segue o formato padrão de produções.")
                    else:
                        raise FormatError("A gramática não segue o formato padrão de produções.")
                self.__producoes[chave] = producoes
            else:
                raise FormatError("A gramática não segue o formato padrão de produções.")

    def transformar_em_AF(self):
        af = AutomatoFinito()
        af.set_vt(self.__vt)

        simbolo_novo = None
        for letra in ascii_uppercase:
            if not(self.__producoes.keys().__contains__(letra)):
                simbolo_novo = letra
                break

        if letra != None:
            simbolos_finais = []
            simbolos_finais.append(simbolo_novo)
            # S -> & pertence à P
            producoes_iniciais = self.__producoes[self.__simbolo_inicial]
            for p in producoes_iniciais:
                if p[0] == "&":
                    simbolos_finais.append(self.__simbolo_inicial)
            af.set_simbolos_finais(simbolos_finais)

            # Construção das produções
            # chave é um frozen set
            #produção: é um dicionario: chave -> letrinha, value -> frozen set

            for k in self.__producoes.keys():
                chave = frozenset([k])
                producoes_af = {}

                producoes_g = self.__producoes[k]
                for p in producoes_g:
                    if p[0] != "&" and p[1] == "&":
                        producoes_af[p[0]] = frozenset([simbolo_novo])
                    else:
                        producoes_af[p[0]] = frozenset([p[1]])

                af.adiciona_producao(chave, producoes_af)

            # Transições indefinidas para o símbolo novo
            chave = frozenset([simbolo_novo])
            producoes_af = {}
            for x in self.__vt:
                producoes_af[x] = frozenset(["-"])
            af.adiciona_producao(chave, producoes_af)

            return af
        else:
            pass #não tem mais letras no alfabeto possiveis pra ser o novo simbolo

    def is_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False