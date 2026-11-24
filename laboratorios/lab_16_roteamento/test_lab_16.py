"""Testes offline do Laboratório 16."""
import json
import unittest

from lab_16_roteamento.gateway import custo_cascata, gateway_aurora, rotas, taxa_maxima_cascata

SIMPLES = {"texto": "prazo", "risco": "baixo", "passos": 1}
ALTO = {"texto": "contestar nota", "risco": "alto", "passos": 2}
FORA = {"texto": "poema", "fora_de_escopo": True}
LONGO = {"texto": "plano de estudos", "risco": "baixo", "passos": 5}


class TestLab16Roteamento(unittest.TestCase):
    def test_reproduz_o_bloco_do_capitulo(self):
        g = gateway_aurora(indisponiveis={"fronteira"})
        destinos = [g.atender(f"c{i}", p)["destino"] for i, p in enumerate([SIMPLES, ALTO, FORA, LONGO])]
        self.assertEqual([rotas(p)[0] for p in (SIMPLES, ALTO, FORA, LONGO)], ["rapido", "fronteira", "recusar", "fronteira"])
        self.assertEqual(destinos, ["rapido", "fila_humana", "recusar", "rapido"])

    def test_cascata_e_ponto_de_equilibrio(self):
        self.assertAlmostEqual(custo_cascata(1, 12, 0.20), 3.4)
        self.assertAlmostEqual(taxa_maxima_cascata(1, 12), 11 / 12)
        self.assertGreater(custo_cascata(1, 12, 0.95), 12)

    def test_conversa_estavel_e_troca_registrada(self):
        g = gateway_aurora()
        self.assertEqual(g.atender("c1", SIMPLES)["destino"], "rapido")
        self.assertEqual(g.atender("c1", LONGO)["destino"], "rapido")       # fixado: não troca por tamanho
        r = g.atender("c1", ALTO)                                         # risco alto não aceita o rápido
        self.assertEqual((r["destino"], r["nova_sessao"]), ("fronteira", True))
        self.assertEqual(g.atender("c1", SIMPLES)["destino"], "fronteira")
        self.assertEqual(g.atender("c1", FORA)["destino"], "recusar")       # escopo vale mesmo com fixação
        linhas = [json.loads(x) for x in g.registro]
        self.assertEqual([x["motivo"] for x in linhas], ["regra", "conversa fixada", "regra", "conversa fixada", "regra"])
        self.assertEqual(linhas[0]["esforco"], "low")
        self.assertEqual(g.custo_total(), 1 + 1 + 12 + 12)

    def test_contingencia_quando_rota_cai(self):
        g = gateway_aurora()
        g.atender("c2", LONGO)
        g.indisponiveis.add("fronteira")
        r = g.atender("c2", LONGO)
        self.assertEqual((r["destino"], r["nova_sessao"]), ("rapido", True))
        self.assertEqual(json.loads(g.registro[-1])["motivo"], "contingência")
        self.assertEqual(g.atender("c3", ALTO)["destino"], "fila_humana")   # alto risco nunca é rebaixado


if __name__ == "__main__":
    unittest.main()
