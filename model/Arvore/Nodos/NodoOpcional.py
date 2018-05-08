from model.Arvore.Nodo import Nodo

class NodoOpcional(Nodo):

    def __init__(self):
        super(NodoOpcional, self).__init__("*")

    def descer(self):
        self.getFilhoEsquerdo().descer()
        self.getCostura().subir() # TODO subir ou descer?

    def subir(self):
        self.getCostura().subir() # TODO subir ou descer?

