from model.Arvore.Nodo import Nodo
from model.Constants import *

class NodoConcat(Nodo):

    def __init__(self):
        super(NodoConcat, self).__init__(Operacao.CONCAT.value, prioridade=Prioridade(Operacao.CONCAT))

    def descer(self):
        self.getFilhoEsquerdo().descer()

    def subir(self):
        self.getFilhoDireito().descer()

