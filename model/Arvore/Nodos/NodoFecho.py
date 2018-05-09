from model.Arvore.Nodo import Nodo

class NodoFecho(Nodo):

    def __init__(self):
        super(NodoFecho, self).__init__("*", prioridade=0)

    def descer(self):
        self.getFilhoEsquerdo().descer()
        self.getCostura().subir() # TODO subir ou descer?

    def subir(self):
        self.getFilhoEsquerdo().descer()
        self.getCostura().subir() # TODO subir ou descer?

