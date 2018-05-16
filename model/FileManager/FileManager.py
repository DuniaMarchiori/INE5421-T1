import os.path

'''
    Classe responsável por salvar e carregar arquivos.
'''
class FileManager:
    
    '''
        Salva um texto em um arquivo .txt.
        \:param nome é o nome do arquivo a ser salvo.
        \:param conteudo é a string contendo o texto que se quer salvar.
    '''
    def salvar(self, nome, conteudo):
        pasta_destino = os.path.abspath("../../ElementosSalvos")
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        nome_arquivo = nome + ".txt"
        caminho = pasta_destino + "/" + nome_arquivo

        num = 1
        while os.path.isfile(caminho):
            nome_arquivo = nome + " (" + str(num) + ").txt"
            caminho = pasta_destino + "/" + nome_arquivo
            num += 1
        
        file = open(caminho, "w")
        file.write(conteudo)
        file.close()

    '''
        Carrega o texto de um arquivo.
        \:param nome_arquivo é o caminho do arquivo a ser lido.
        \:return o conteúdo do arquivo
    '''
    def abrir(self, nome_arquivo):
        file = open(nome_arquivo, "r")
        texto = file.read()
        file.close()
        return texto

