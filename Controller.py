from model.Model import Model
from view.View import View

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

    def cb_nova_gramatica(self, valor):
        print("GR: " + valor)

    def cb_nova_expressao(self, valor):
        print("ER: " + valor)

    '''
        Salva uma gramática em um arquivo.
        \:param texto é a gramática a ser salva, em formato de texto.
        \:return o nome do arquivo salvo.
    '''
    def salvar_gramatica(self, texto):
        return self.__model.salvar_gramatica(texto)

    '''
        Lê uma gramática de um arquivo.
        \:param nome_arquivo é o nome do arquivo a ser lido.
        \:return True se a leitura ocorreu com sucesso.
    '''
    def abrir_gramatica(self, nome_arquivo):
        return self.__model.abrir_gramatica(nome_arquivo)

    '''
        Salva uma expressão em um arquivo.
        \:param texto é a expressão a ser salva, em formato de texto.
        \:return o nome do arquivo salvo.
    '''
    def salvar_expressao(self, texto):
        return self.__model.salvar_expressao(texto)

    '''
        Lê uma expressão de um arquivo.
        \:param nome_arquivo é o nome do arquivo a ser lido.
        \:return True se a leitura ocorreu com sucesso.
    '''
    def abrir_expressao(self, nome_arquivo):
        return self.__model.abrir_expressao(nome_arquivo)

    '''
        Transforma uma gramática em um autômato finito.
        \:param gramatica é a gramática a ser transformada.
        \:return o autômato finito que reconhece a mesma linguagem que a gramática gera.
    '''
    def transformar_GR_em_AF(self, gramatica):
        return self.__model.transformar_GR_em_AF(gramatica)

    '''
        Transforma um autômato finito em uma gramática.
        \:param af é o autômato finito a ser transformado.
        \:return a gramática que gera a mesma linguagem que o autômato reconhece.
    '''
    def transformar_AF_em_GR(self, af):
        return self.__model.transformar_AF_em_GR(af)