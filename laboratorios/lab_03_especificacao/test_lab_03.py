"""Testes offline de aceite do Laboratório 03."""
import unittest

from lab_03_especificacao.contrato_aurora import (
    carregar_politicas,
    classificar_escopo_pedido,
    validar_contrato_saida,
)


class TestLab03Especificacao(unittest.TestCase):
    def setUp(self):
        self.politicas = carregar_politicas()

    def test_classificacao_de_escopo_e_politicas(self):
        self.assertEqual(len(self.politicas), 3)
        self.assertEqual(classificar_escopo_pedido("Qual o prazo de cancelamento?"), "permitido")
        self.assertEqual(classificar_escopo_pedido("Pode confirmar matrícula agora?"), "fora_escopo_proibido")
        self.assertEqual(classificar_escopo_pedido("Enviei meu CPF aqui"), "sensivel_exige_triagem")

    def test_contrato_aceita_citacao_valida_e_reprova_acao_proibida(self):
        ok = validar_contrato_saida(
            "Conforme POL-01, o cancelamento pode ser pedido em até 7 dias corridos.",
            self.politicas,
        )
        self.assertTrue(ok["aceito"])
        self.assertEqual(ok["citacoes"], ["POL-01"])

        proib = validar_contrato_saida("Conforme POL-01, sua matrícula confirmada já vale.", self.politicas)
        self.assertFalse(proib["aceito"])
        self.assertEqual(proib["motivo"], "reprovacao_automatica_acao_proibida")

    def test_smooth_failing_por_latencia_ou_fonte_inventada(self):
        lento = validar_contrato_saida("POL-01 ok", self.politicas, tempo_ms=2200.0)
        self.assertEqual(lento["motivo"], "fallback_latencia")

        sem_fonte = validar_contrato_saida("Conforme POL-99, o prazo é 30 dias.", self.politicas)
        self.assertFalse(sem_fonte["aceito"])
        self.assertEqual(sem_fonte["motivo"], "sem_fonte_valida")


if __name__ == "__main__":
    unittest.main()
