from model.Arvore.Nodo import Nodo

class Arvore:

    __nodoRaiz = None
    __folhas = []

    def __init__(self):
        pass

    def setNodoRaiz(self, novoNodoRaiz):
        self.__nodoRaiz = novoNodoRaiz

    def getNodoRaiz(self):
        return self.__nodoRaiz

    def getEmOrdem(self):
        return self.__nodoRaiz.emOrdem("")

    def costuraArvore(self):
        stack = []
        stack.append(Nodo("$"))
        self.__nodoRaiz.costuraNodo(stack)
