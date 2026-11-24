"""Testes offline do Laboratório 08."""
import unittest

from lab_08_grafos_estado.fluxo import FalhaSimulada, FluxoReembolso, custo_tokens


class TestLab08Grafos(unittest.TestCase):
    def test_valor_baixo_passa_direto(self):
        f = FluxoReembolso()
        r = f.executar("f1", {"chave": "r-1", "valor": "120", "dias_desde_matricula": 3})
        self.assertEqual(r["status"], "concluido")
        self.assertEqual(f.pagamentos(), [("r-1", 120)])
        f.fechar()

    def test_fora_do_prazo_recusa_sem_efeito(self):
        f = FluxoReembolso()
        r = f.executar("f2", {"chave": "r-2", "valor": 90, "dias_desde_matricula": 12})
        self.assertIn("POL-01", r["motivo"])
        self.assertEqual(f.pagamentos(), [])
        f.fechar()

    def test_pausa_aprovacao_e_retoma_do_ponto(self):
        f = FluxoReembolso()
        r1 = f.executar("f3", {"chave": "r-3", "valor": 900, "dias_desde_matricula": 2})
        self.assertEqual(r1, {"status": "pausado", "no": "aguardar_aprovacao"})
        f.visitas.clear()
        r2 = f.executar("f3", aprovado=True)
        self.assertEqual(r2["status"], "concluido")
        self.assertEqual(f.visitas, ["aguardar_aprovacao", "gravar_pagamento"])
        self.assertEqual(f.pagamentos(), [("r-3", 900)])
        f.fechar()

    def test_falha_apos_efeito_nao_duplica(self):
        f = FluxoReembolso(falhar_em="apos_gravar")
        with self.assertRaises(FalhaSimulada):
            f.executar("f4", {"chave": "r-4", "valor": 200, "dias_desde_matricula": 1})
        r = f.executar("f4")  # retomada reexecuta o nó gravar_pagamento
        self.assertEqual(r["status"], "concluido")
        self.assertEqual(f.pagamentos(), [("r-4", 200)])
        self.assertEqual(f.executar("f4")["status"], "concluido")
        self.assertEqual(f.pagamentos(), [("r-4", 200)])
        f.fechar()

    def test_custo_com_e_sem_subagentes(self):
        sem = custo_tokens(5, 2000, 3000, 300, com_subagentes=False)
        com = custo_tokens(5, 2000, 3000, 300, com_subagentes=True)
        self.assertEqual(sem, 5 * 2000 + 3000 * (1 + 2 + 3 + 4 + 5))
        self.assertEqual(com, 5 * 5000 + 2000 + 1500)
        self.assertLess(com, sem)
        self.assertGreater(custo_tokens(1, 2000, 3000, 300, True), custo_tokens(1, 2000, 3000, 300, False))


if __name__ == "__main__":
    unittest.main()
