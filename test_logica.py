"""Testes automatizados. Execute: python -m unittest -v"""

import unittest
from logica import ListaHibrida, busca_binaria, busca_sequencial


class TesteListaHibrida(unittest.TestCase):
    def setUp(self):
        self.lista = ListaHibrida(semente=42)

    def test_geracao_reprodutivel_ordenada_sem_repeticao(self):
        a = self.lista.ordenada
        self.assertEqual(len(a), 1024)
        self.assertEqual(a, sorted(a))
        self.assertEqual(len(set(a)), 1024)
        self.assertEqual(a, ListaHibrida(semente=42).ordenada)

    def test_busca_binaria_na_regiao_ordenada(self):
        chave = self.lista.ordenada[0]
        resultado = self.lista.buscar(chave)
        self.assertEqual(resultado["local"], "Região ordenada")
        self.assertGreater(resultado["binaria"], 0)
        self.assertEqual(resultado["sequencial"], 0)

    def test_busca_sequencial_na_cauda(self):
        for chave in (-10, -20, -30):
            self.lista.inserir(chave)
        resultado = self.lista.buscar(-30)
        self.assertEqual(resultado["local"], "Cauda não ordenada")
        self.assertEqual(resultado["indice"], 2)
        self.assertEqual(resultado["sequencial"], 3)
        self.assertEqual(resultado["total"], resultado["binaria"] + 3)

    def test_chave_ausente(self):
        self.lista.inserir(-10)
        resultado = self.lista.buscar(-99)
        self.assertEqual(resultado["local"], "Não encontrada")
        self.assertIsNone(resultado["indice"])
        self.assertEqual(resultado["sequencial"], 1)

    def test_rejeita_repetidas_nas_duas_regioes(self):
        existente = self.lista.ordenada[3]
        self.assertFalse(self.lista.inserir(existente)[0])
        self.assertTrue(self.lista.inserir(-1)[0])
        self.assertFalse(self.lista.inserir(-1)[0])
        self.assertEqual(self.lista.cauda, [-1])

    def test_decima_insercao_intercala_e_esvazia(self):
        for chave in (-3, -1, -9, -5, -8, -2, -10, -7, -4, -6):
            self.lista.inserir(chave)
        self.assertEqual(self.lista.cauda, [])
        self.assertEqual(len(self.lista.ordenada), 1034)
        self.assertEqual(self.lista.ordenada, sorted(self.lista.ordenada))
        self.assertEqual(len(set(self.lista.ordenada)), 1034)
        self.assertEqual(self.lista.buscar(-9)["local"], "Região ordenada")

    def test_nova_insercao_apos_intercalacao(self):
        for chave in range(-1, -11, -1):
            self.lista.inserir(chave)
        self.assertTrue(self.lista.inserir(-11)[0])
        self.assertEqual(self.lista.cauda, [-11])
        self.assertEqual(self.lista.buscar(-11)["local"], "Cauda não ordenada")

    def test_funcoes_de_busca_em_listas_simples(self):
        self.assertEqual(busca_binaria([2, 4, 6], 4)[0], 1)
        self.assertIsNone(busca_binaria([2, 4, 6], 5)[0])
        self.assertEqual(busca_sequencial([7, 1, 9], 9)[0], 2)
        self.assertIsNone(busca_sequencial([], 7)[0])


if __name__ == "__main__":
    unittest.main()
