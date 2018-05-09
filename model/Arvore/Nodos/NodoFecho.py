from model.Arvore.Nodo import Nodo
from model.Constants import *

class NodoFecho(Nodo):

    def __init__(self):
        super(NodoFecho, self).__init__(Operacao.FECHO.value, prioridade=Prioridade(Operacao.FECHO))

    def descer(self):
        self.getFilhoEsquerdo().descer()
        self.getCostura().subir() # TODO subir ou descer?

    def subir(self):
        self.getFilhoEsquerdo().descer()
        self.getCostura().subir() # TODO subir ou descer?

