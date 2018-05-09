class Nodo:

    __valor = None
    __prioridadeOperador = None
    __filhoEsquerdo = None
    __filhoDireito = None
    __costura = None

    def __init__(self, valor, prioridade=0):
        self.__valor = valor
        self.__prioridadeOperador = prioridade

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

    def emOrdem(self, expressao):
        if (self.__filhoEsquerdo != None):
            if (self.__filhoEsquerdo.__prioridadeOperador > self.__prioridadeOperador):
                expressao += "("
            expressao = self.__filhoEsquerdo.emOrdem(expressao)
            if (self.__filhoEsquerdo.__prioridadeOperador > self.__prioridadeOperador):
                expressao += ")"
        if self.__valor != ".":
            expressao += self.__valor
        if (self.__filhoDireito != None):
            if (self.__filhoDireito.__prioridadeOperador > self.__prioridadeOperador):
                expressao += "("
            expressao = self.__filhoDireito.emOrdem(expressao)
            if (self.__filhoDireito.__prioridadeOperador > self.__prioridadeOperador):
                expressao += ")"
        return expressao

    def descer(self):
        pass

    def subir(self):
        pass


