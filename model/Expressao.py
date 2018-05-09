class Expressao:
    __numero = 1

    def salvar(self, texto):
        nome_arquivo = "expressao_" + str(self.__numero) + ".txt"
        file = open(nome_arquivo, "w")
        file.write(texto)
        file.close()
        self.__numero += 1
        return nome_arquivo

    def abrir(self, nome_arquivo):
        file = open(nome_arquivo, "r")
        texto = file.read()
        file.close()
        #print(texto)
        return texto