# Autores: Dúnia Marchiori e Vinicius Steffani Schweitzer [2018]
from model.Model import Model
from view.View import View

from model.exception.FormatError import FormatError
from model.exception.ExpressionParsingError import ExpressionParsingError

'''
    Controller do padrão MVC.
'''
class Controller:

    __model = None  # Fachada do modelo
    __view = None  # Tela principal da aplicação

    '''
       Método construtor.
    '''
    def __init__(self):
        self.__model = Model()  # Fachada do modelo
        self.__view = View(self)  # Tela principal da aplicação
        self.__view.start()

    '''
        Transforma uma gramática em um autômato finito.
        \:param gramatica é a gramática a ser transformada.
        \:return o autômato finito que reconhece a mesma linguagem que a gramática gera.
    '''
    def __transformar_GR_em_AF(self, gramatica):
        return self.__model.transformar_GR_em_AF(gramatica)

    '''
        Transforma um autômato finito em uma gramática.
        \:param af é o autômato finito a ser transformado.
        \:return a gramática que gera a mesma linguagem que o autômato reconhece.
    '''
    def __transformar_AF_em_GR(self, af):
        return self.__model.transformar_AF_em_GR(af)

    # Callbacks da interface

    '''
        Método que recebe um nome e a entrada de uma gramática e a adiciona no sistema, mostrando erro caso aconteça.
        \:param nome é o nome da gramática que será criada.
        \:param entrada é a representação textual da gramática.
        \:return True se a operação foi bem sucedida, False caso contrário.
    '''
    def cb_nova_gramatica(self, nome, entrada):
        try:
            self.__model.criar_gramatica(nome, entrada)
            self.__view.adicionar_elemento_na_lista(nome, "GR")
            return True
        except FormatError as e:
            self.__view.mostrar_aviso(e.get_message())
            return False

    '''
        Método que recebe um nome e a entrada de uma expressão e a adiciona no sistema, mostrando erro caso aconteça.
        \:param nome é o nome da expressão que será criada.
        \:param entrada é a representação textual da expressão.
        \:return True se a operação foi bem sucedida, False caso contrário.
    '''
    def cb_nova_expressao(self, nome, entrada):
        try:
            self.__model.criar_expressao(nome, entrada)
            self.__view.adicionar_elemento_na_lista(nome, "ER")
            return True
        except ExpressionParsingError as e:
            self.__view.mostrar_aviso(e.get_message())
            return False

    '''
        Método que recebe um índice e remove esse objeto da lista.
        \:param indice é o índice do elemento na lista.
    '''
    def cb_remover_elemento(self, indice):
        self.__model.remover_elemento(indice)
        self.__view.remover_elemento_da_lista(indice)

    '''
        Método que é chamado ao alterar o elemento selecionado na lista.
        \:param indice é o índice do elemento na lista.
    '''
    def cb_alterar_elemento_selecionado(self, indice):
        elemento = None
        if indice is not None:
            elemento = self.__model.obter_elemento_por_indice(indice)
        self.__view.atualiza_elemento_selecionado(indice, elemento)

    # TODO
    '''
        Callbacks:
        
            Transformações:
                OK ER -> AF
                
                OK GR -> AF
                OK AF -> GR
                
            Operações sobre Linguagem
                L intersec L -> AF
                L diferença L -> AF
                L reverso -> AF
                Onde, L pode ser GR, ER ou AF
        
            Operações sobre AF
                TODO Determinizar AF
                TODO Minimizar AF
        
            Operações sobre GR
                GR união GR
                GR concat GR
                GR fecho
    '''
