from model.Elemento import Elemento
from model.ListaElementos import ListaElementos
from model.Expressao import Expressao
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
        gr = Elemento(None, nome)
        self.__lista_de_elementos.adiciona_elemento(gr)

    '''
        Método que recebe um nome e a entrada de uma expressão e a adiciona no sistema.
        \:param nome é o nome da expressão que será criada.
        \:param entrada é a representação textual da expressão.
    '''
    def criar_expressao(self, nome, entrada):
        # er = Expressao(nome, entrada)
        er = Elemento(None, nome)
        self.__lista_de_elementos.adiciona_elemento(er)

    '''
        Método que recebe um índice e remove esse objeto da lista.
        \:param indice é o índice do elemento na lista.
    '''
    def remover_elemento(self, indice):
        self.__lista_de_elementos.remove_elemento(indice)

    '''
        Salva uma gramática em um arquivo.
        \:param texto é a gramática a ser salva, em formato de texto.
        \:return o nome do arquivo salvo em caso de sucesso. Em caso de erro, retorna nulo.
    '''
    def salvar_gramatica(self, texto):
        g = Gramatica()
        try:
            arquivo = g.salvar(texto)
        except:
            print("ERRO: Erro ao salvar a gramática.")
            return None
        return arquivo

    '''
        Lê uma gramática de um arquivo.
        \:param nome_arquivo é o nome do arquivo a ser lido.
        \:return True se a leitura ocorreu com sucesso. Em caso de erro, retorna nulo.
    '''
    def abrir_gramatica(self, nome_arquivo):
        g = Gramatica()
        try:
            g.abrir(nome_arquivo)
            return g
        except FormatError as err:
            print(err.get_message())
            return None
        except FileNotFoundError:
            print("ERRO: Arquivo não encontrado.")
            return None
        except:
            print("ERRO: Erro ao ler o arquivo.")
            return None

    '''
        Salva uma expressão em um arquivo.
        \:param texto é a expressão a ser salva, em formato de texto.
        \:return o nome do arquivo salvo em caso de sucesso. Em caso de erro, retorna nulo.
    '''
    def salvar_expressao(self, texto):
        e = Expressao()
        try:
            arquivo = e.salvar(texto)
        except:
            print("ERRO: Erro ao salvar a expressão.")
            return None
        return arquivo

    '''
        Lê uma expressão de um arquivo.
        \:param nome_arquivo é o nome do arquivo a ser lido.
        \:return True se a leitura ocorreu com sucesso. EM caso de erro, retorna nulo.
    '''
    def abrir_expressao(self, nome_arquivo):
        e = Expressao()
        # TODO - botar um try-except aqui
        texto = e.abrir(nome_arquivo)
        return texto

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