class Estado:

    '''
        Método construtor.
        \:param nomes é uma lista com o nome dos estados que representam este estado.
    '''
    def __init__(self, nomes):
        self.__lista = sorted(nomes, key=str.lower)
        self.__string = ''.join(self.__lista)
        self.__nome = frozenset(nomes)

    '''
        Retorna o estado em formato de lista.
        \:return uma lista com a composição do estado.
    '''
    def to_list(self):
        return self.__lista

    '''
        Retorna o estado em formato de texto.
        \:return uma string com a composição do estado.
    '''
    def to_string(self):
        return self.__string

    '''
        Retorna o estado em formato de conjunto.
        \:return um frozenset com a composição do estado.
    '''
    def get_nome(self):
        return self.__nome

    def __hash__(self):
        return hash(self.__nome)

    def __eq__(self, other):
        return self.__nome.__hash__() == other.get_nome().__hash__()