from model.Expressao import Expressao
from model.Gramatica import Gramatica

class Model:
    atributo1 = None

    def salvar_gramatica(self, texto):
        g = Gramatica()
        arquivo = g.salvar(texto)
        return arquivo

    def abrir_gramatica(self, nome_arquivo):
        g = Gramatica()
        texto = g.abrir(nome_arquivo)
        return texto

    def salvar_expressao(self, texto):
        e = Expressao()
        arquivo = e.salvar(texto)
        return arquivo

    def abrir_expressao(self, nome_arquivo):
        e = Expressao()
        texto = e.abrir(nome_arquivo)
        return texto