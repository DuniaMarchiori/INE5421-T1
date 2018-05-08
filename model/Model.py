from model.Expressao import Expressao
from model.Gramatica import Gramatica
from model.exception.FormatError import FormatError


class Model:
    atributo1 = None

    def salvar_gramatica(self, texto):
        g = Gramatica()
        try:
            arquivo = g.salvar(texto)
        except:
            print("ERRO: Erro ao salvar a gramática.")
            return None
        return arquivo

    def abrir_gramatica(self, nome_arquivo):
        g = Gramatica()
        try:
            g.abrir(nome_arquivo)
            return g
        except FormatError as err:
            print(err.get_message())
            return None
        except FileNotFoundError:
            print("ERRO: Arquivo não encontrado.")
            return None
        except:
            print("ERRO: Erro ao ler o arquivo.")
            return None

    def salvar_expressao(self, texto):
        e = Expressao()
        try:
            arquivo = e.salvar(texto)
        except:
            print("ERRO: Erro ao salvar a expressão.")
            return None
        return arquivo

    def abrir_expressao(self, nome_arquivo):
        e = Expressao()
        # TODO - botar um try-except aqui
        texto = e.abrir(nome_arquivo)
        return texto

    def transformar_GR_em_AF(self, gramatica):
        if gramatica == None:
            print("ERRO: A gramática a ser transformada em autômato está vazia.")
        else:
            return gramatica.transformar_em_AF()

    def transformar_AF_em_GR(self, af):
        if af == None:
            print("ERRO: O autômato finito a ser transformado em gramática está vazio.")
        else:
            return af.transforma_em_GR()