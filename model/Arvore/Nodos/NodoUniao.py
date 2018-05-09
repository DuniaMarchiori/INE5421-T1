from model.Arvore.Nodo import Nodo
from model.Constants import *

class NodoUniao(Nodo):

    def __init__(self):
        super(NodoUniao, self).__init__(Operacao.UNIAO.value, prioridade=Prioridade(Operacao.UNIAO))

    def descer(self):
        self.getFilhoEsquerdo().descer()
        self.getFilhoDireito().descer()

    def subir(self):
        # TODO é isso mesmo? (faz sentido se o getCostura de quem não tem costura é a costura do filho direito acho)
        self.getFilhoDireito().getCostura().subir()

