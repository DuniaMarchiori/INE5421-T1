from model.Arvore.Nodo import Nodo
from model.Constants import *

class NodoOpcional(Nodo):

    def __init__(self):
        super(NodoOpcional, self).__init__(Operacao.OPCIONAL.value, prioridade=Prioridade(Operacao.OPCIONAL))

    def descer(self):
        self.getFilhoEsquerdo().descer()
        self.getCostura().subir() # TODO subir ou descer?

    def subir(self):
        self.getCostura().subir() # TODO subir ou descer?

