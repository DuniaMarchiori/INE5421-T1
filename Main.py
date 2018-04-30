from Controller import Controller

def main():
    c = Controller()
    texto = "S -> aS| aB\nB -> b"
    arquivo = c.salvar_gramatica(texto)
    c.abrir_gramatica(arquivo)

    texto = "a*"
    arquivo = c.salvar_expressao(texto)
    c.abrir_expressao(arquivo)

main()