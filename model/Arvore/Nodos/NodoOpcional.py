from model.Arvore.Nodo import Nodo
from model.Constants import *


class NodoOpcional(Nodo):

    def __init__(self):
        super(NodoOpcional, self).__init__(Operacao.OPCIONAL.value, prioridade=prioridade(Operacao.OPCIONAL))

    def descer(self):
        self.get_filho_esquerdo().descer()
        self.get_costura().subir() # TODO subir ou descer?

    def subir(self):
        self.get_costura().subir() # TODO subir ou descer?
