class Arvore:

    __nodoRaiz = None

    def __init__(self):
        pass

    def setNodoRaiz(self, novoNodoRaiz):
        self.__nodoRaiz = novoNodoRaiz

    def getNodoRaiz(self):
        return self.__nodoRaiz

    def getEmOrdem(self):
        return self.__nodoRaiz.emOrdem("")
