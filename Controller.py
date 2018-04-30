from model.Model import Model

class Controller:
    model = Model()

    def salvar_gramatica(self, texto):
        return self.model.salvar_gramatica(texto)

    def abrir_gramatica(self, nome_arquivo):
        return self.model.abrir_gramatica(nome_arquivo)

    def salvar_expressao(self, texto):
        return self.model.salvar_expressao(texto)

    def abrir_expressao(self, nome_arquivo):
        return self.model.abrir_expressao(nome_arquivo)