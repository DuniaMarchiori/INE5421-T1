class FormatError(Exception):
    FORMAT_ERROR = "A gramática não segue o formato padrão de produções regulares: "

    def __init__(self, message):
        self.__message = "ERRO: " + message

    def get_message(self):
        return self.__message