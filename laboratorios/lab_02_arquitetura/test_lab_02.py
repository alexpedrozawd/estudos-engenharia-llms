"""Testes offline do Laboratório 02."""
import unittest
from unittest.mock import MagicMock

from lab_02_arquitetura.cliente_resiliente import (
    ClienteResiliente,
    ErroPermanente,
    ErroTransitorio,
    analisar_eventos_sse,
)


class TestLab02Arquitetura(unittest.TestCase):
    def test_backoff_jitter_e_idempotencia(self):
        transporte = MagicMock(
            side_effect=[
                ErroTransitorio("503 overloaded"),
                ErroTransitorio("429 rate limit"),
                {"texto": "Parcela quitada.", "stop_reason": "end_turn"},
            ]
        )
        cli = ClienteResiliente(max_tentativas=3, semente_jitter=7)
        payload = {"mensagem": "Status da parcela"}

        r1 = cli.executar("req-001", payload, transporte)
        r2 = cli.executar("req-001", payload, transporte)

        self.assertEqual(r1.tentativas, 3)
        self.assertEqual(len(cli.esperas_registradas), 2)
        self.assertTrue(r2.de_cache_idempotencia)
        self.assertEqual(transporte.call_count, 3)

    def test_rejeita_reuso_de_chave_com_payload_diferente_e_erro_permanente(self):
        cli = ClienteResiliente()
        cli.executar("req-002", {"a": 1}, lambda p: {"texto": "ok", "stop_reason": "end_turn"})
        with self.assertRaises(ValueError):
            cli.executar("req-002", {"a": 2}, lambda p: {"texto": "ok"})
        with self.assertRaises(ErroPermanente):
            cli.executar("req-003", {"a": 3}, MagicMock(side_effect=ErroPermanente("400 bad request")))

    def test_recusa_controlada_e_sse_cortado(self):
        cli = ClienteResiliente(max_em_fila=1)
        cli.em_andamento = 1
        with self.assertRaises(ErroTransitorio):
            cli.executar("req-004", {"a": 1}, lambda p: {"texto": "ok"})

        sse = analisar_eventos_sse(
            [
                'data: {"delta": "Faltam "}',
                'data: {"delta": "R$ 229,50", "stop_reason": "max_tokens"}',
            ]
        )
        self.assertEqual(sse["texto"], "Faltam R$ 229,50")
        self.assertEqual(sse["motivo_parada"], "max_tokens")


if __name__ == "__main__":
    unittest.main()
