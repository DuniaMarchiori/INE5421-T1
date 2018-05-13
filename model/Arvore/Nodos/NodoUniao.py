from model.Arvore.Nodo import Nodo
from model.Constants import *


class NodoUniao(Nodo):

    def __init__(self):
        super(NodoUniao, self).__init__(Operacao.UNIAO.value, prioridade=prioridade(Operacao.UNIAO))

    def descer(self, composicao):
        composicao = self.get_filho_esquerdo().descer(composicao)
        composicao = self.get_filho_direito().descer(composicao)
        return composicao

    def subir(self, composicao):
        # TODO é isso mesmo? (faz sentido se o getCostura de quem não tem costura é a costura do filho direito acho)
        composicao = self.get_filho_direito().get_costura().subir(composicao)
        return composicao
