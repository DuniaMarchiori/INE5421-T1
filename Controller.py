from model.Model import Model

class Controller:
    __model = Model()

    def salvar_gramatica(self, texto):
        return self.__model.salvar_gramatica(texto)

    def abrir_gramatica(self, nome_arquivo):
        return self.__model.abrir_gramatica(nome_arquivo)

    def salvar_expressao(self, texto):
        return self.__model.salvar_expressao(texto)

    def abrir_expressao(self, nome_arquivo):
        return self.__model.abrir_expressao(nome_arquivo)

    def transformar_GR_em_AF(self, gramatica):
        return self.__model.transformar_GR_em_AF(gramatica)