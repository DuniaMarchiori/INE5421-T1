from Controller import Controller

def main():
    c = Controller()
    texto = "S - > 0B|1BA \n BA-> 0 \n B->0"
    arquivo = c.salvar_gramatica(texto)
    g = c.abrir_gramatica(arquivo)
    #g.printa()
    #print(g.toString())
    af = c.transformar_GR_em_AF(g)
    #af.printa()
    g2 = c.transformar_AF_em_GR(af)
    #g2.printa()

    texto = "a*"
    arquivo = c.salvar_expressao(texto)
    c.abrir_expressao(arquivo)

main()