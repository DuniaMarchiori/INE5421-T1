class AutomatoFinito:

    def __init__(self):
        self.__producoes = {}
        self.__simbolos_inicial = None
        self.__simbolos_finais = []
        self.__vt = set()

    def adiciona_producao(self, chave, producao):
        self.__producoes[chave] = producao

    '''
    def set_producoes(self, producoes):
        self.__producoes = producoes
    '''

    def get_producoes(self):
        return self.__producoes

    def set_simbolo_inicial(self, simbolo):
        self.__simbolos_inicial = simbolo

    def set_simbolos_finais(self, lista):
        self.__simbolos_finais = lista

    def set_vt(self, vt):
        self.__vt = vt

    def get_vt(self):
        return self.__vt

    def printa(self):
        print("VT:")
        for x in self.__vt:
            print(x)

        print("-------")
        print("Produções:")
        for k in self.__producoes.keys():
            print(k)
            print(self.__producoes[k])

        print("-------")
        print("Simbolos finais:")
        for y in self.__simbolos_finais:
            print(y)

        print("xxxxxxx")