"""Testes offline do Laboratório 13."""
import unittest

from lab_13_autodestrutivos.incidentes import Disjuntor, Trava, Transacao, proporcionalidade, simular_incidente


class TestLab13Autodestrutivos(unittest.TestCase):
    def test_trava_reproduz_o_bloco_do_capitulo(self):
        t = Trava()
        seq = [("ler_arquivo", "notas.csv"), ("apagar_pasta", "/dados"), ("ler_arquivo", "notas.csv"),
               ("gravar_relatorio", "rel.md"), ("listar_pasta", "docs"), ("ler_arquivo", "plano.md")]
        saidas = [t.autorizar(a, b) for a, b in seq]
        self.assertEqual(saidas, ["executar", "bloqueado: fora da lista de permissão", "bloqueado: repetição idêntica",
                                  "simulado (dry-run): nada gravado", "executar",
                                  "parar: orçamento de tentativas esgotado"])

    def test_disjuntor_abre_espera_e_testa(self):
        agora = [0.0]
        d = Disjuntor(limite=3, espera=30, relogio=lambda: agora[0])
        r = simular_incidente(lambda: False, tentativas=20, disjuntor=d)
        self.assertEqual(r, {"chamadas": 3, "barradas": 17})
        self.assertEqual(simular_incidente(lambda: False, tentativas=20), {"chamadas": 20, "barradas": 0})
        agora[0] = 31
        self.assertTrue(d.permitir())
        self.assertEqual(d.estado, "meio-aberto")
        d.registrar(False)
        self.assertEqual(d.estado, "aberto")
        agora[0] = 62
        d.permitir()
        d.registrar(True)
        self.assertEqual(d.estado, "fechado")

    def test_reversao_quando_invariante_quebra(self):
        notas = {"ana": 8.0, "bia": 6.5}
        tx = Transacao(notas, invariante=lambda e: all(0 <= v <= 10 for v in e.values()))
        self.assertTrue(tx.aplicar(lambda e: e.update(ana=9.0)))
        self.assertFalse(tx.aplicar(lambda e: e.update(bia=65.0)))   # erro de escala: revertido na hora
        self.assertEqual(notas, {"ana": 9.0, "bia": 6.5})
        self.assertTrue(tx.desfazer())
        self.assertEqual(notas, {"ana": 8.0, "bia": 6.5})
        self.assertFalse(tx.desfazer())

    def test_proporcionalidade_prefere_script_quando_ganho_nao_paga(self):
        r = proporcionalidade(0.92, 3.0, 0.90, 0.1, valor_acerto=10, custo_erro=20)
        self.assertEqual(r["escolha"], "script")
        r = proporcionalidade(0.95, 1.0, 0.60, 0.1, valor_acerto=10, custo_erro=20)
        self.assertEqual(r["escolha"], "agente")


if __name__ == "__main__":
    unittest.main()
