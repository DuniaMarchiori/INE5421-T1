class Gramatica:
    numero = 1

    def salvar(self, texto):
        nome_arquivo = "gramatica_" + str(self.numero) + ".txt"
        file = open(nome_arquivo, "w")
        file.write(texto)
        file.close()
        self.numero += 1
        return nome_arquivo

    def abrir(self, nome_arquivo):
        file = open(nome_arquivo, "r")
        texto = file.read()
        file.close()
        g = self.ler(texto)
        for i in g:
            print(i)
        return g

    def ler(self, texto):
        return texto.splitlines()
