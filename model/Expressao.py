from model.Arvore.Arvore import Arvore
from model.Arvore.Nodos.NodoUniao import NodoUniao
from model.Arvore.Nodos.NodoConcat import NodoConcat
from model.Arvore.Nodos.NodoFecho import NodoFecho
from model.Arvore.Nodos.NodoOpcional import NodoOpcional
from model.Arvore.Nodos.NodoFolha import NodoFolha
from model.Constants import Operacao, prioridade


'''
    Classe que representa uma expressão regular.
'''
class Expressao:

    __arvore = None

    '''
        Método construtor.
        \:param expressao é a representação textual da expressão regular.
    '''
    def __init__(self, expressao):
        self.__gerar_arvore(expressao)

    '''
        Retorna a representação textual da expressão regular.
        \:return a representação textual da expressão regular.
    '''
    def to_string(self):
        return self.__arvore.get_em_ordem()

    '''
        Metodo utilizado para gerar a arvore a partir da representação textual da expressão regular.
        \:param expressao é a representação textual da expressão regular.
    '''
    def __gerar_arvore(self, expressao):
        self.__arvore = Arvore()
        if self.__verifica_validade(expressao):
            expressao = self.__preparar_expressao(expressao)
            self.__arvore.set_nodo_raiz(self.__gerar_nodo(expressao))
        self.__arvore.costura_arvore()
        self.__arvore.numera_folhas()

    '''
        Algorítmo recursivo que gera a arvore/sub-arvore a partir da expressão/sub-expressão regular dada.

        Ele percorre a expressão encontrando o operador de menor prioridade na expressão atual, criando um nodo na
        arvore para este operador, e então chama recursivamente o algoritmo para gerar as sub-arvores passando como
        parametro a sub-expressão do novo ramo.

        \:param expressao é a representação textual da expressão regular.
        \:return o nodo raíz da árvore obtida a partir da expressão dada.
    '''
    def __gerar_nodo(self, expressao):
        subexpressao = self.__remover_parenteses_externos(expressao)

        if len(subexpressao) == 1:
            return NodoFolha(subexpressao)
        else:
            operador_div = None
            prioridade_div = -1
            posicao_div = None

            parenteses_abertos = 0
            for i in range(0, len(subexpressao)):
                char = subexpressao[i]
                if char == "(":
                    parenteses_abertos += 1
                elif char == ")":
                    parenteses_abertos -= 1
                elif parenteses_abertos == 0:
                    if char == "|" and prioridade_div < 2:
                        operador_div = Operacao.UNIAO
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "." and prioridade_div < 1:
                        operador_div = Operacao.CONCAT
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "*" and prioridade_div < 0:
                        operador_div = Operacao.FECHO
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "?" and prioridade_div < 0:
                        operador_div = Operacao.OPCIONAL
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i

            nodo = None
            if operador_div == Operacao.UNIAO:
                nodo = NodoUniao()
                nodo.set_filho_esquerdo(self.__gerar_nodo(subexpressao[0:posicao_div]))
                nodo.set_filho_direito(self.__gerar_nodo(subexpressao[posicao_div + 1:]))

            elif operador_div == Operacao.CONCAT:
                nodo = NodoConcat()
                nodo.set_filho_esquerdo(self.__gerar_nodo(subexpressao[0:posicao_div]))
                nodo.set_filho_direito(self.__gerar_nodo(subexpressao[posicao_div + 1:]))

            elif operador_div == Operacao.FECHO:
                nodo = NodoFecho()
                nodo.set_filho_esquerdo(self.__gerar_nodo(subexpressao[0:posicao_div]))

            else:  # operadorDiv == Operacao.OPCIONAL:
                nodo = NodoOpcional()
                nodo.set_filho_esquerdo(self.__gerar_nodo(subexpressao[0:posicao_div]))

            return nodo

    '''
        Verifica se uma expressão representada em texto possui apenas caracteres válidos em uma posição válida.
        \:param expressao é a representação textual da expressão regular.
        \:return True caso a expressão seja válida
    '''
    def __verifica_validade(self, expressao):
        # TODO verificar se a expressao contem apenas caracteres do alfabeto, operadores ou espaços em branco
        # TODO verificar se não tem coisas como "|*" ou "((( bla bla )"
        if True:
            return True
        #else:
            # raise ("Caracter desconhecido X na posição Y")
            #pass

    '''
        Prepara a expressão para o alogorítmo de construção da arvore, eliminando espaços e expondo concatenações
        implicitas.
        \:param expressao é a representação textual da expressão regular.
        \:return a expressão preparada para o algoritmo de geração de arvore.
    '''
    def __preparar_expressao(self, expressao):
        # Remove espaços em branco
        expressao = "".join(expressao.split())
        # Adiciona concatenações impricitas
        expressao = self.__expor_concatenacoes_implicitas(expressao)
        return expressao

    '''
        Expõe concatenações implícitas na expressão regular dada.
        \:param expressao é a representação textual da expressão regular.
        \:return a expressão com suas concatenações implicitas reveladas.
    '''
    def __expor_concatenacoes_implicitas(self, expressao):
        nova_expressao = expressao
        char_anterior = " "
        concats_adicionadas = 0
        for i in range(0, len(expressao)):
            char = expressao[i]
            if (char_anterior.isalnum() or (char_anterior in ")*?")) and (char.isalnum() or char == "("):
                nova_expressao = nova_expressao[:i+concats_adicionadas] + '.' + nova_expressao[i+concats_adicionadas:]
                concats_adicionadas += 1
            char_anterior = char

        return nova_expressao

    '''
        Remove parenteses redundantes nas extremidades de uma expressão.
        \:param expressao é a representação textual da expressão regular.
        \:return a expressão sem parenteses reundantes nas extremidades.
    '''
    def __remover_parenteses_externos(self, expressao):
        parenteses_encontrados = 0
        nivel = 0
        inicio = True
        i = 0
        comprimento_expr = len(expressao)
        while i < comprimento_expr - parenteses_encontrados:
            char = expressao[i]
            if char == "(":
                nivel += 1
                if inicio:
                    parenteses_encontrados = nivel
            else:
                inicio = False
                if char == ")":
                    nivel -= 1
                    parenteses_encontrados = min(parenteses_encontrados, nivel)
            i += 1
        return expressao[parenteses_encontrados:comprimento_expr - parenteses_encontrados]
