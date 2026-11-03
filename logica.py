"""Algoritmos da atividade: região ordenada + cauda não ordenada."""

import random


def busca_binaria(valores, chave):
    """Busca somente numa lista ordenada; devolve índice e passos."""
    # O intervalo começa abrangendo toda a região ordenada.
    esquerda, direita = 0, len(valores) - 1
    passos = []

    while esquerda <= direita:
        # Comparamos apenas o elemento central a cada iteração.
        meio = (esquerda + direita) // 2
        passos.append((meio, valores[meio]))

        if valores[meio] == chave:
            return meio, passos
        # Descartamos a metade que não pode conter a chave.
        if chave < valores[meio]:
            direita = meio - 1
        else:
            esquerda = meio + 1

    return None, passos


def busca_sequencial(valores, chave):
    """Percorre a cauda do início ao fim; devolve índice e passos."""
    passos = []

    # Na cauda não ordenada, verificamos elemento por elemento.
    for indice, valor in enumerate(valores):
        passos.append((indice, valor))
        if valor == chave:
            return indice, passos

    return None, passos


class ListaHibrida:
    def __init__(self, semente=42):
        # A mesma semente produz sempre a mesma lista inicial.
        gerador = random.Random(semente)
        # sample evita repetição; sorted põe os 1.024 valores em ordem.
        self.ordenada = sorted(gerador.sample(range(1, 10001), 1024))
        self.cauda = []

    def buscar(self, chave):
        # A busca começa na região ordenada.
        indice, passos_bin = busca_binaria(self.ordenada, chave)
        passos_seq = []
        local = "Não encontrada"

        if indice is not None:
            local = "Região ordenada"
        else:
            # Só procura na cauda se a busca binária não encontrar.
            indice, passos_seq = busca_sequencial(self.cauda, chave)
            if indice is not None:
                local = "Cauda não ordenada"

        return {
            "local": local,
            "indice": indice,
            "binaria": len(passos_bin),
            "sequencial": len(passos_seq),
            "total": len(passos_bin) + len(passos_seq),
            "passos_binaria": passos_bin,
            "passos_sequencial": passos_seq,
        }

    def inserir(self, chave):
        # Reutiliza a busca para impedir duplicatas nas duas regiões.
        if self.buscar(chave)["local"] != "Não encontrada":
            return False, f"A chave {chave} já existe. Inserção rejeitada."

        self.cauda.append(chave)
        # A décima chave dispara a intercalação automática.
        if len(self.cauda) == 10:
            self.intercalar()
            return True, "10ª inserção! A cauda foi ordenada, intercalada e esvaziada."

        return True, f"Chave {chave} inserida no fim da cauda."

    def intercalar(self):
        """Ordena a cauda e une duas regiões já ordenadas."""
        # Ordena só os 10 valores novos, não a região inteira.
        self.cauda.sort()
        resultado = []
        i = j = 0

        # Compara os próximos valores de ambas as regiões ordenadas.
        while i < len(self.ordenada) and j < len(self.cauda):
            if self.ordenada[i] < self.cauda[j]:
                resultado.append(self.ordenada[i])
                i += 1
            else:
                resultado.append(self.cauda[j])
                j += 1

        # Inclui os elementos restantes e deixa a cauda pronta para reuso.
        resultado.extend(self.ordenada[i:])
        resultado.extend(self.cauda[j:])
        self.ordenada = resultado
        self.cauda = []
