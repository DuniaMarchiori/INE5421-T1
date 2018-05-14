class ListaElementos:

    __lista_de_elementos = None

    def __init__(self):
        self.__lista_de_elementos = []

    def adiciona_elemento(self, elemento):
        self.__lista_de_elementos.append(elemento)

    def remove_elemento(self, indice):
        self.__lista_de_elementos.pop(indice)