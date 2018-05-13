from Controller import Controller
from model.AF.Estado import Estado


def main():
    c = Controller()
    texto = "S - > 0B| 0S| 1  B|  & \n  B->0"
    arquivo = c.salvar_gramatica(texto)
    g = c.abrir_gramatica(arquivo)
    #g.printa()
    #print(g.to_string())
    af = c.transformar_GR_em_AF(g)
    #af.adiciona_producao('T', '0', ['A','B'])
    #af.printa()
    af.adiciona_estado(Estado("I"))
    for l in af.to_string():
        print(l)
    g2 = c.transformar_AF_em_GR(af)
    g2.printa()
    print(g2.to_string())

    texto = "a*"
    arquivo = c.salvar_expressao(texto)
    c.abrir_expressao(arquivo)

main()