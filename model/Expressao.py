from model.Arvore.Arvore import Arvore
from model.Arvore.Nodo import Nodo
from model.Arvore.Nodos.NodoUniao import NodoUniao
from model.Arvore.Nodos.NodoConcat import NodoConcat
from model.Arvore.Nodos.NodoFecho import NodoFecho
from model.Arvore.Nodos.NodoOpcional import NodoOpcional
from enum import Enum
import string

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
        self.arvore = Arvore()
        if self.verificaValidade(expressao):
            #expressao.replace(" ", "") # Remove espaços da expressao inteira
            expressao = "".join(expressao.split()) # Remove espaços da expressao inteira
            self.arvore.setNodoRaiz(self.gerarNodo(expressao))

    def verificaValidade(self, expressao):
        # TODO verificar se a expressao contem apenas caracteres do alfabeto, operadores ou espaços em branco
        # TODO verificar se não tem coisas como "|*" ou "((( bla bla )"
        if True:
            return True
        #else:
            # raise ("Caracter desconhecido X na posição Y")
            #pass

    def gerarNodo(self, expressao):
        subexpressao = self.__removerParentesesExternos(expressao)
        subexpressao = self.__exporConcatenacoesOcultas(subexpressao)

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

            nodo = None
            if operadorDiv == Operacao.UNIAO:
                nodo = NodoUniao()
                nodo.setFilhoEsquerdo(self.gerarNodo(subexpressao[0:posicaoDiv]))
                nodo.setFilhoDireito(self.gerarNodo(subexpressao[posicaoDiv+1:]))

            elif operadorDiv == Operacao.CONCAT:
                nodo = NodoConcat()
                nodo.setFilhoEsquerdo(self.gerarNodo(subexpressao[0:posicaoDiv]))
                nodo.setFilhoDireito(self.gerarNodo(subexpressao[posicaoDiv+1:]))

            elif operadorDiv == Operacao.FECHO:
                nodo = NodoFecho()
                nodo.setFilhoEsquerdo(self.gerarNodo(subexpressao))

            else: # operadorDiv == Operacao.OPCIONAL:
                nodo = NodoOpcional()
                nodo.setFilhoEsquerdo(self.gerarNodo(subexpressao))

            return nodo

    def __removerParentesesExternos(self, expressao):
        temParenteses = True
        while (temParenteses):
            if expressao[0] == "(" and expressao[-1] == ")":
                expressao = expressao[1:-1]
            else:
                temParenteses = False
        return expressao

    def __exporConcatenacoesOcultas(self, expressao):
        novaExpressao = expressao
        charAnterior = ""
        concatsAdicionadas = 0
        for i in range(0, len(expressao)):
            char = expressao[i]
            if self.__charPertenceAConcatenacao(charAnterior) and self.__charPertenceAConcatenacao(char):
                novaExpressao = novaExpressao[:i+concatsAdicionadas] + '.' + novaExpressao[i+concatsAdicionadas:]
                concatsAdicionadas += 1
            charAnterior = char

        return novaExpressao

    def __charPertenceAConcatenacao(self, char):
        return char == ("(" or ")" or "*" or "?") or char.isalnum()


class Operacao(Enum):
    UNIAO = "|"  # 2
    CONCAT = "."  # 1
    FECHO = "*"  # 0
    OPCIONAL = "?"  # 0