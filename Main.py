from Controller import Controller

def main():
    c = Controller()
    texto = "S -> 0S| 1B | &\nB -> &"
    arquivo = c.salvar_gramatica(texto)
    g = c.abrir_gramatica(arquivo)
    af = c.transformar_GR_em_AF(g)
    af.printa()

    texto = "a*"
    arquivo = c.salvar_expressao(texto)
    c.abrir_expressao(arquivo)

main()