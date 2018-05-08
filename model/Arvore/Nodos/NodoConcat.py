from model.Arvore.Nodo import Nodo

class NodoConcat(Nodo):

    def __init__(self):
        super(NodoConcat, self).__init__(".")

    def descer(self):
        self.getFilhoEsquerdo().descer()

    def subir(self):
        self.getFilhoDireito().descer()

