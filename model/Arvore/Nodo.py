class Nodo:

    __valor = None
    __filhoEsquerdo = None
    __filhoDireito = None
    __costura = None

    def __init__(self, valor):
        self.__valor = valor

    def setValor(self, valor):
        self.__valor = valor

    def getValor(self):
        return self.__valor

    def setFilhoEsquerdo(self, novoFilhoEsquerdo):
        self.__filhoEsquerdo = novoFilhoEsquerdo

    def getFilhoEsquerdo(self):
        return self.__filhoEsquerdo

    def setFilhoDireito(self, novoFilhoDireito):
        self.__filhoDireito = novoFilhoDireito

    def getFilhoDireito(self):
        return self.__filhoDireito

    def setCostura(self, nodoCosturado):
        self.__costura = nodoCosturado

    def getCostura(self):
        if self.__costura != None:
            return self.__costura
        else:
            return self.__filhoDireito.getCostura()

    def descer(self):
        pass

    def subir(self):
        pass

