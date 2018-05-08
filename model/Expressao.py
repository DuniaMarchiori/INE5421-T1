from model.Arvore.Arvore import Arvore
from model.Arvore.Nodo import Nodo
from model.Arvore.Nodos.NodoUniao import NodoUniao
from model.Arvore.Nodos.NodoConcat import NodoConcat
from model.Arvore.Nodos.NodoFecho import NodoFecho
from model.Arvore.Nodos.NodoOpcional import NodoOpcional
from enum import Enum

class Expressao:

    arvore = None
    numero = 1

    def salvar(self, texto):
        nome_arquivo = "expressao_" + str(self.numero) + ".txt"
        file = open(nome_arquivo, "w")
        file.write(texto)
        file.close()
        self.numero += 1
        return nome_arquivo

    def abrir(self, nome_arquivo):
        file = open(nome_arquivo, "r")
        texto = file.read()
        file.close()
        print(texto)
        return texto

    def gerarArvore(self, expressao):
        arvore = Arvore()
        if self.verificaValidade(expressao):
            expressao.replace(" ", "") # remove espaços
            arvore.setNodoRaiz(self.gerarNodo(expressao))

    def verificaValidade(self, expressao):
        # TODO verificar se a expressao contem apenas caracteres do alfabeto, operadores ou espaços em branco
        # TODO verificar se não tem coisas como "|*" ou "((( bla bla )"
        if True:
            return True
        #else:
            # raise ("Caracter desconhecido X na posição Y")
            #pass

    def gerarNodo(self, expressao):
        subexpressao = expressao
        temParenteses = True
        while (temParenteses):
            if subexpressao[0] == "(" and subexpressao[len(subexpressao)] == ")":
                subexpressao = subexpressao[1:-1]
            else:
                temParenteses = False

        if len(subexpressao) == 1:
            # TODO verificar se expressão é realmente um caracter terminal
            return Nodo(subexpressao)
        else:
            operadorDiv = None
            prioridadeDiv = -1
            posicaoDiv = None

            parentesesAbertos = 0
            for i in range(0, len(subexpressao)):
                char = subexpressao[i]
                if char == "(":
                    parentesesAbertos += 1
                elif char == ")":
                    parentesesAbertos -= 1
                elif parentesesAbertos == 0:
                    if char == "|" and prioridadeDiv < 2:
                        operadorDiv = Operacao.UNIAO
                        prioridadeDiv = 2
                        posicaoDiv = i
                        #break TODO ja encontrei o primeiro "|" mais pra esquerda, nem preciso ver o resto, talvez dê pra dar break
                    if char == "." and prioridadeDiv < 0:
                        operadorDiv = Operacao.CONCAT
                        prioridadeDiv = 1
                        posicaoDiv = i
                    if char == "*" and prioridadeDiv < 0:
                        operadorDiv = Operacao.FECHO
                        prioridadeDiv = 0
                        posicaoDiv = i
                    if char == "?" and prioridadeDiv < 0:
                        operadorDiv = Operacao.OPCIONAL
                        prioridadeDiv = 0
                        posicaoDiv = i

            if operadorDiv == Operacao.UNIAO:
                nodo = NodoUniao()
                nodo.setFilhoEsquerdo(self.gerarNodo(subexpressao[0:posicaoDiv]))
                nodo.setFilhoDireito(self.gerarNodo(subexpressao[posicaoDiv+1:]))

            if operadorDiv == Operacao.CONCAT:
                nodo = NodoConcat()
                nodo.setFilhoEsquerdo(self.gerarNodo(subexpressao[0:posicaoDiv]))
                nodo.setFilhoDireito(self.gerarNodo(subexpressao[posicaoDiv+1:]))

            if operadorDiv == Operacao.FECHO:
                nodo = NodoFecho()
                nodo.setFilhoEsquerdo(self.gerarNodo(subexpressao))

            if operadorDiv == Operacao.OPCIONAL:
                nodo = NodoOpcional()
                nodo.setFilhoEsquerdo(self.gerarNodo(subexpressao))


class Operacao(Enum):
    UNIAO = "|"  # 2
    CONCAT = "."  # 1
    FECHO = "*"  # 0
    OPCIONAL = "?"  # 0