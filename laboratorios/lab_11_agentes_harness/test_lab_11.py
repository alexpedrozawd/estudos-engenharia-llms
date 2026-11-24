"""Testes offline do Laboratório 11."""
import json
import unittest

from comum.cliente_llm import ClienteMockDeterministico
from lab_11_agentes_harness.agente import Harness, erro_composto, ferramentas_aurora, roteiro_aurora


class TestLab11Agentes(unittest.TestCase):
    def novo(self, teto=5, respostas=None, fallback="{}"):
        cli = ClienteMockDeterministico(respostas if respostas is not None else roteiro_aurora(), fallback=fallback)
        return Harness(cli, ferramentas_aurora(), teto=teto)

    def test_responde_em_tres_passos_com_registro(self):
        h = self.novo()
        r = h.executar("Ainda posso pedir reembolso?")
        self.assertEqual(r["status"], "respondido")
        self.assertIn("POL-01", r["resposta"])
        self.assertEqual(r["estado"]["passo"], 3)
        linhas = [json.loads(x) for x in h.registro]
        self.assertEqual([x["acao"] for x in linhas], ["buscar", "buscar", "responder"])

    def test_teto_para_e_retomada_continua(self):
        h = self.novo(teto=2)
        r = h.executar("Ainda posso pedir reembolso?")
        self.assertEqual(r["status"], "teto")
        self.assertIn("teto de passos", h.registro[-1])
        h.teto = 5
        r2 = h.executar("Ainda posso pedir reembolso?", estado=r["estado"])
        self.assertEqual(r2["status"], "respondido")
        self.assertEqual(r2["estado"]["passo"], 3)

    def test_contrato_do_modelo_e_ferramenta_inexistente(self):
        self.assertEqual(self.novo(respostas={}, fallback="texto livre").executar("x")["motivo"], "resposta do modelo não é JSON")
        self.assertEqual(self.novo(respostas={}, fallback='{"acao": "voar"}').executar("x")["motivo"], "resposta do modelo fora do contrato")
        ruim = {"OBS: inicio": json.dumps({"acao": "buscar", "argumento": "bolsas"})}
        r = self.novo(respostas=ruim).executar("x")
        self.assertEqual(r["status"], "escalonar")

    def test_erro_composto(self):
        self.assertAlmostEqual(erro_composto(0.95, 10), 0.5987, places=4)
        self.assertLess(erro_composto(0.95, 100), 0.01)


if __name__ == "__main__":
    unittest.main()
