from enum import Enum

class Operacao(Enum):
    UNIAO = "|"
    CONCAT = "."
    FECHO = "*"
    OPCIONAL = "?"

__prioridade = {
    Operacao.UNIAO: 2,
    Operacao.CONCAT: 1,
    Operacao.FECHO: 0,
    Operacao.OPCIONAL: 0
}
def Prioridade(operacao):
    return __prioridade[operacao]
