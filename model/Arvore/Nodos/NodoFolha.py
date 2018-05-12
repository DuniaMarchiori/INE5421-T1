from model.Arvore.Nodo import Nodo


class NodoFolha(Nodo):

    def __init__(self, valor):
        super(NodoFolha, self).__init__(valor, folha=True)

    def descer(self):
        pass

    def subir(self):
        self.get_costura().subir()
