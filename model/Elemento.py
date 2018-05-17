from enum import Enum

class Elemento:

    __nome = None
    __tipo = None

    def __init__(self, tipo, nome):
        self.__tipo = tipo
        self.__nome = nome

    def get_nome(self):
        return self.__nome

    def get_tipo(self):
        return self.__tipo

    def parse(self, expressao):
        pass

    def to_string(self):
        return ""


class TipoElemento(Enum):
    GR = 0
    ER = 1
    AF = 2
