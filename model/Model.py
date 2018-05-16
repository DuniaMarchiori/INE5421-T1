from model.Elemento import *
from model.ListaElementos import ListaElementos
from model.ER.Expressao import Expressao
from model.Gramatica import Gramatica
from model.exception.FormatError import FormatError

'''
    Fachada do módulo model.
'''
class Model:

    __lista_de_elementos = None

    def __init__(self):
        self.__lista_de_elementos = ListaElementos()

    '''
        Método que recebe um nome e a entrada de uma gramática e a adiciona no sistema.
        \:param nome é o nome da gramática que será criada.
        \:param entrada é a representação textual da gramática.
    '''
    def criar_gramatica(self, nome, entrada):
        # gr = Gramatica(nome, entrada)
        gr = Elemento(TipoElemento.GR, nome)
        self.__lista_de_elementos.adiciona_elemento(gr)

    '''
        Método que recebe um nome e a entrada de uma expressão e a adiciona no sistema.
        \:param nome é o nome da expressão que será criada.
        \:param entrada é a representação textual da expressão.
    '''
    def criar_expressao(self, nome, entrada):
        # er = Expressao(nome, entrada)
        er = Elemento(TipoElemento.ER, nome)
        self.__lista_de_elementos.adiciona_elemento(er)

    '''
        Método que recebe um índice e remove esse objeto da lista.
        \:param indice é o índice do elemento na lista.
    '''
    def remover_elemento(self, indice):
        self.__lista_de_elementos.remove_elemento(indice)

    '''
        Transforma uma gramática em um autômato finito.
        \:param gramatica é a gramática a ser transformada.
        \:return o autômato finito que reconhece a mesma linguagem que a gramática gera.
    '''
    def transformar_GR_em_AF(self, gramatica):
        if gramatica == None:
            print("ERRO: A gramática a ser transformada em autômato está vazia.")
        else:
            return gramatica.transformar_em_AF()

    '''
        Transforma um autômato finito em uma gramática.
        \:param af é o autômato finito a ser transformado.
        \:return a gramática que gera a mesma linguagem que o autômato reconhece.
    '''
    def transformar_AF_em_GR(self, af):
        if af == None:
            print("ERRO: O autômato finito a ser transformado em gramática está vazio.")
        else:
            return af.transforma_em_GR()

    def obter_elemento_por_indice(self, indice):
        return self.__lista_de_elementos.get_elemento(indice)