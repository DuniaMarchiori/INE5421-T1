from Controller import Controller
from model.Gramatica import Gramatica
from model.exception.FormatError import FormatError


def main():
    c = Controller()
    texto = "S ->  0B|0S| 1  B| & \n  B->0"
    g = Gramatica()
    try:
        g.parse(texto)
    except FormatError as err:
        print(err.get_message())

    af = g.transformar_em_AF()
    for l in af.to_string():
        print(l)
    af2 = af.determiniza()
    #af2.printa()
    for l in af2.to_string():
        print(l)
    '''
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
    print(g2.to_string())'''

    '''texto = "(ab|ac)* a% | (ba?c)*"
    e = Expressao(texto)
    afe = e.obter_automato_finito_equivalente()
    afe.printa()'''

main()