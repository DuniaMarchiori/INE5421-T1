from model.Arvore.Nodo import Nodo
from model.Constants import *


class NodoConcat(Nodo):

    def __init__(self):
        super(NodoConcat, self).__init__(Operacao.CONCAT.value, prioridade=prioridade(Operacao.CONCAT))

    def descer(self):
        self.get_filho_esquerdo().descer()

    def subir(self):
        self.get_filho_direito().descer()
