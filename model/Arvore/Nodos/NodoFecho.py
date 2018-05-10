from model.Arvore.Nodo import Nodo
from model.Constants import *


class NodoFecho(Nodo):

    def __init__(self):
        super(NodoFecho, self).__init__(Operacao.FECHO.value, prioridade=prioridade(Operacao.FECHO))

    def descer(self):
        self.get_filho_esquerdo().descer()
        self.get_costura().subir()  # TODO subir ou descer?

    def subir(self):
        self.get_filho_esquerdo().descer()
        self.get_costura().subir()  # TODO subir ou descer?
