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
        Salva uma gramática em um arquivo.
        \:param texto é a gramática a ser salva, em formato de texto.
        \:return o nome do arquivo salvo.
    '''
    def __salvar_gramatica(self, texto):
        return self.__model.salvar_gramatica(texto)

    '''
        Lê uma gramática de um arquivo.
        \:param nome_arquivo é o nome do arquivo a ser lido.
        \:return True se a leitura ocorreu com sucesso.
    '''
    def __abrir_gramatica(self, nome_arquivo):
        return self.__model.abrir_gramatica(nome_arquivo)

    '''
        Salva uma expressão em um arquivo.
        \:param texto é a expressão a ser salva, em formato de texto.
        \:return o nome do arquivo salvo.
    '''
    def __salvar_expressao(self, texto):
        return self.__model.salvar_expressao(texto)

    '''
        Lê uma expressão de um arquivo.
        \:param nome_arquivo é o nome do arquivo a ser lido.
        \:return True se a leitura ocorreu com sucesso.
    '''
    def __abrir_expressao(self, nome_arquivo):
        return self.__model.abrir_expressao(nome_arquivo)

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
    '''
    def cb_nova_gramatica(self, nome, entrada):
        try:
            self.__model.criar_gramatica(nome, entrada)
            self.__view.adicionar_elemento_na_lista(nome)
        except FormatError as e:
            self.__view.mostrar_aviso(e.get_message())

    '''
        Método que recebe um nome e a entrada de uma expressão e a adiciona no sistema, mostrando erro caso aconteça.
        \:param nome é o nome da expressão que será criada.
        \:param entrada é a representação textual da expressão.
    '''
    def cb_nova_expressao(self, nome, entrada):
        try:
            self.__model.criar_expressao(nome, entrada)
            self.__view.adicionar_elemento_na_lista(nome)
        except ExpressionParsingError as e:
            self.__view.mostrar_aviso(e.get_message())

    '''
        Método que recebe um índice e remove esse objeto da lista.
        \:param indice é o índice do elemento na lista.
    '''
    def cb_remover_elemento(self, indice):
        self.__model.remover_elemento(indice)
        self.__view.remover_elemento_da_lista(indice)
