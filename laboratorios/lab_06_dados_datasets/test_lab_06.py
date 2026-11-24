"""Testes offline do Laboratório 06."""
import unittest
from collections import Counter

from lab_06_dados_datasets.curadoria import (
    amostra_estratificada, deduplicar_exatas, detectar_vazamento, dividir_por_grupo,
    jaccard, manifesto, reservatorio, validar_jsonl,
)


def casos():
    tipos = ["geral"] * 60 + ["prazo"] * 30 + ["recusa"] * 10
    return [{"id": i, "aluno": f"A{i % 25:02d}", "tipo": t, "pergunta": f"pergunta {t} número {i}"}
            for i, t in enumerate(tipos)]


class TestLab06Dados(unittest.TestCase):
    def test_validar_jsonl_recusa_linhas_ruins(self):
        linhas = ['{"pergunta": "prazo?", "tipo": "prazo"}', '{"pergunta": ""}', 'nao-json', '[1, 2]', '']
        validos, erros = validar_jsonl(linhas, ["pergunta", "tipo"])
        self.assertEqual(len(validos), 1)
        self.assertEqual(len(erros), 3)
        self.assertIn("linha 3: JSON inválido", erros[1])

    def test_deduplicacao_exata_e_quase_duplicata(self):
        itens = [{"pergunta": "Qual o prazo de cancelamento?"},
                 {"pergunta": "qual o prazo  de cancelamento?!"},
                 {"pergunta": "Como emitir o certificado do curso de dados?"}]
        unicos, removidos = deduplicar_exatas(itens)
        self.assertEqual((len(unicos), removidos), (2, 1))
        nota = jaccard("Como emitir o certificado do curso de dados no portal?",
                       "Como emitir o certificado do curso de dados?")
        self.assertAlmostEqual(nota, 0.75)

    def test_estratificada_preserva_raro_e_reservatorio(self):
        amostra = amostra_estratificada(casos(), "tipo", 0.10)
        self.assertEqual(Counter(c["tipo"] for c in amostra), Counter({"geral": 6, "prazo": 3, "recusa": 1}))
        res = reservatorio(range(1000), 50, semente=3)
        self.assertEqual(len(res), 50)
        self.assertEqual(len(set(res)), 50)
        self.assertEqual(res, reservatorio(range(1000), 50, semente=3))

    def test_divisao_por_grupo_sem_vazamento(self):
        treino, teste = dividir_por_grupo(casos(), "aluno", 0.2)
        self.assertFalse({c["aluno"] for c in treino} & {c["aluno"] for c in teste})
        self.assertEqual(len(treino) + len(teste), 100)
        ajuste = [{"pergunta": "Como emitir o certificado do curso de dados?"}]
        t = [{"pergunta": "Como emitir o certificado do curso de dados no portal?"},
             {"pergunta": "Quem aprova bolsas de estudo?"}]
        achados = detectar_vazamento(ajuste, t)
        self.assertEqual(len(achados), 1)
        self.assertEqual(achados[0][2], 0.75)

    def test_manifesto_conta_estratos_e_sinteticos(self):
        itens = casos()[:5] + [{"id": 99, "tipo": "recusa", "pergunta": "x", "origem": "sintetico"}]
        m = manifesto(itens, "aval-v3", "conversas mai-out", "tipo", "coordenação")
        self.assertEqual(m["total"], 6)
        self.assertEqual(m["sinteticos"], 1)
        self.assertEqual(m["por_estrato"], {"geral": 5, "recusa": 1})
        self.assertEqual(len(m["sha256"]), 16)
        self.assertEqual(m, manifesto(itens, "aval-v3", "conversas mai-out", "tipo", "coordenação"))


if __name__ == "__main__":
    unittest.main()
