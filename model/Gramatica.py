from model.exception.FormatError import FormatError
from string import ascii_uppercase


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
        Salva um novo símbolo inicial.
        \param novo símbolo inicial
    '''
    def set_simbolo_inicial(self, simbolo):
        self.__simbolo_inicial = simbolo

    '''
        Adiciona uma nova produção.
        \param chave é o símbolo não-terminal.
        \param producao é uma lista de tuplas no formato (símbolo terminal, símbolo não-terminal)
    '''
    def adiciona_producao(self, chave, producao):
        self.__producoes[chave] = producao

    '''
        
    '''
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
        self.__texto = texto
        return nome_arquivo

    def abrir(self, nome_arquivo):
        file = open(nome_arquivo, "r")
        self.__texto = file.read()
        file.close()
        self.__texto = self.__texto.replace(" ", "") # Retira todos os espaços em branco
        lista = self.__texto.splitlines()
        self.gera_estrutura_producoes(lista)
        return True

    def gera_estrutura_producoes(self, lista):
        i = 0

        for linha in lista:
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
                                raise FormatError(FormatError.FORMAT_ERROR + "as produções regulares devem seguir o formato aB, onde a é um símbolo terminal e B um símbolo não terminal.")
                        else:
                            chars = list(p)
                            terminal = chars[0] # caractere terminal
                            nao_terminal = chars[1:len(chars)] # caracteres não-terminais
                            all_upper = True if True in [s.isupper() for s in nao_terminal] else False # Todos os caracteres do símbolo não-terminal são maiúsculos
                            # Produção é um símbolo terminal seguido de um não-terminal (que pode ter tamanho maior que um, mas todos os caracteres maíusculos)
                            if (( terminal.islower() or self.is_int(terminal)) and all_upper):
                                simbolo_nt = ''.join(nao_terminal)
                                producoes.append((terminal, simbolo_nt))
                                self.__vt.add(terminal)
                                self.__vn_dir.add(simbolo_nt)
                            else:
                                raise FormatError(FormatError.FORMAT_ERROR + "as produções regulares devem seguir o formato aB, onde a é um símbolo terminal e B um símbolo não terminal.")
                else:
                    raise FormatError(FormatError.FORMAT_ERROR + "ocorre mais de um símbolo '->' por produção.")

                self.__producoes[chave] = producoes
            else:
                raise FormatError(FormatError.FORMAT_ERROR + "produção não apresenta o símbolo '->'")

        # Símbolo não-terminal referenciado não tem produções
        for vn in self.__vn_dir:
            if not(self.__producoes.keys().__contains__(vn)):
                raise FormatError("A gramática referencia símbolos não terminais com produções não definidas: " + vn)

    def transformar_em_AF(self):
        from model.AutomatoFinito import AutomatoFinito

        af = AutomatoFinito()
        af.set_vt(self.__vt)

        simbolo_novo = None
        # TODO pode ter mais de um símbolo
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
                b = frozenset([k])
                producoes_af = {}

                producoes_g = self.__producoes[k]
                for p in producoes_g:
                    a = p[0]
                    c = p[1]
                    if a != "&" and c == "&":
                        producoes_af[a] = frozenset([simbolo_novo])
                    else:
                        producoes_af[a] = frozenset([c])

                af.adiciona_producao(b, producoes_af)

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

    def toString(self):
        if self.__texto != None:
            return self.__texto
        else:
            gramatica = ""

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

                gramatica += texto + "\n"
            return gramatica

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