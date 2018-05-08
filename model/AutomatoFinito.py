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

    def transforma_em_GR(self):
        from model.Gramatica import Gramatica

        gramatica = Gramatica()
        gramatica.set_vt(self.__vt)
        gramatica.set_simbolo_inicial(self.__simbolos_inicial)

        #item a e b
        for b in self.__producoes.keys():
            producoes_af = self.__producoes[b]
            producoes_g = []
            for a in producoes_af.keys():
                c = list(producoes_af[a])
                c = ', '.join(c)
                producoes_g.append((a, c))
                if self.__simbolos_finais.__contains__(c):
                    producoes_g.append((a, "&"))
            b = ', '.join(list(b))
            gramatica.adiciona_producao(b, producoes_g)

        # item c
        if self.__simbolos_finais.__contains__(self.__simbolos_inicial):
            #TODO - não precisa verificar se o simbolo inicial aparece do lado direito das produções
            pass

        return gramatica


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
        print()