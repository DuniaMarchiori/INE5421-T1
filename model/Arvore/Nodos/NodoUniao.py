from model.Arvore.Nodo import Nodo

class NodoUniao(Nodo):

    def __init__(self):
        super(NodoUniao, self).__init__("|")

    def descer(self):
        self.getFilhoEsquerdo().descer()
        self.getFilhoDireito().descer()

    def subir(self):
        # TODO é isso mesmo? (faz sentido se o getCostura de quem não tem costura é a costura do filho direito acho)
        self.getFilhoDireito().getCostura().subir()

