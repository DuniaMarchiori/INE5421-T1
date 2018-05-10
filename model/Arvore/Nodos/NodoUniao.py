from model.Arvore.Nodo import Nodo
from model.Constants import *


class NodoUniao(Nodo):

    def __init__(self):
        super(NodoUniao, self).__init__(Operacao.UNIAO.value, prioridade=prioridade(Operacao.UNIAO))

    def descer(self):
        self.get_filho_esquerdo().descer()
        self.get_filho_direito().descer()

    def subir(self):
        # TODO é isso mesmo? (faz sentido se o getCostura de quem não tem costura é a costura do filho direito acho)
        self.get_filho_direito().getCostura().subir()
