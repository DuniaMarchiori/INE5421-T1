'''
    Classe que representa um autômato finito.
'''
class AutomatoFinito:

    '''
        Método construtor.
    '''
    def __init__(self):
        self.__producoes = {} # conjunto de produções
        self.__simbolos_inicial = None
        self.__simbolos_finais = []
        self.__vt = set() # conjunto de símbolos terminais

    '''
        Adiciona uma nova produção.
        \:param chave é o símbolo não-terminal (ou um conjunto deles).
        \:param producao é dicionário onde a chave é um símbolo terminal e os dados são um conjunto de símbolos não-terminais.
    '''
    def adiciona_producao(self, chave, producao):
        self.__producoes[chave] = producao

    '''
        Retorna o conjunto de produções do autômato.
        \:return um dicionário onde a chave é um conjunto de símbolos não-terminais e os dados são 
            um dicionário onde a chave é um símbolo não terminal e os dados são um conjunto de símbolos não-terminais.
    '''
    def get_producoes(self):
        return self.__producoes

    '''
        Modifica o símbolo inicial do autômato.
        \:param simbolo é o novo símbolo inicial.
    '''
    def set_simbolo_inicial(self, simbolo):
        self.__simbolos_inicial = simbolo

    '''
        Modifica o conjunto de símbolos finais do autômato.
        \:param lista é a lista de novos símbolos finais.
    '''
    def set_simbolos_finais(self, lista):
        self.__simbolos_finais = lista

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
            print(k)
            print(self.__producoes[k])

        print("-------")
        print("Simbolos finais:")
        for y in self.__simbolos_finais:
            print(y)

        print("xxxxxxx")
        print()