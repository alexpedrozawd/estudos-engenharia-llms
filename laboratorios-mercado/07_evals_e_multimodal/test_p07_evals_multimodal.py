"""Smoke-tests offline do Projeto 07: evals (kappa, inversão A/B, bootstrap) e multimodal (pdftoppm + Pydantic)."""
import json
import unittest

import eval_pipeline as ep
import extracao_multimodal as em
from mercado_base.cliente_openai import ClienteChatFalso, RespostaChat


def _resp_json(obj: dict) -> RespostaChat:
    return RespostaChat(conteudo=json.dumps(obj, ensure_ascii=False), tokens_entrada=20, tokens_saida=10)


class TestEvals(unittest.TestCase):
    def test_cohen_kappa_exato_e_degenerado(self):
        self.assertEqual(ep.cohen_kappa(["A", "B", "empate", "A"], ["A", "B", "empate", "A"]), 1.0)
        self.assertEqual(ep.cohen_kappa(["A", "A"], ["A", "A"]), 1.0)
        k = ep.cohen_kappa(["A", "A", "B", "B"], ["A", "B", "B", "A"])
        self.assertEqual(k, 0.0)
        with self.assertRaises(ValueError):
            ep.cohen_kappa(["A"], ["A", "B"])

    def test_bootstrap_pareado_significativo_e_nao_significativo(self):
        sig = ep.bootstrap_pareado([2, 2, 3, 2, 2, 3], [5, 4, 5, 5, 4, 5], n_amostras=500, seed=7)
        self.assertTrue(sig["significativo"])
        self.assertGreater(sig["ic_inferior"], 0.0)
        ns = ep.bootstrap_pareado([3, 4, 3, 4], [3, 4, 3, 4], n_amostras=500, seed=7)
        self.assertFalse(ns["significativo"])

    def test_julgar_com_inversao_detecta_vies_de_posicao(self):
        # Na ordem direta vence A; na invertida também diz "A" (que na verdade é B) -> viés -> empate.
        juiz = ClienteChatFalso([
            _resp_json({"vencedor": "A", "nota_a": 5, "nota_b": 3, "justificativa": "Primeiro é melhor"}),
            _resp_json({"vencedor": "A", "nota_a": 5, "nota_b": 3, "justificativa": "Primeiro é melhor"}),
        ])
        res = ep.julgar_com_inversao(juiz, "P?", "Ref", "respA", "respB")
        self.assertTrue(res["vies_posicao"])
        self.assertEqual(res["vencedor"], "empate")
        self.assertEqual((res["nota_a"], res["nota_b"]), (4.0, 4.0))

    def test_portao_bloqueia_promocao_quando_kappa_abaixo_do_limiar(self):
        dados = {
            "pares_calibracao": [
                {"id": "c1", "pergunta": "p1", "referencia": "r1", "resposta_a": "a", "resposta_b": "b", "julgamento_humano": "B"},
                {"id": "c2", "pergunta": "p2", "referencia": "r2", "resposta_a": "a", "resposta_b": "b", "julgamento_humano": "A"},
            ],
            "casos_avaliacao": [
                {"id": "e1", "contexto": "ctx", "pergunta": "p1", "referencia": "r1"},
                {"id": "e2", "contexto": "ctx", "pergunta": "p2", "referencia": "r2"},
            ],
        }
        # Gerador: A ruim, B bom
        gerador = ClienteChatFalso([
            RespostaChat("ruim"), RespostaChat("bom [T1]"),
            RespostaChat("ruim"), RespostaChat("bom [T1]"),
        ])
        # Juiz na calibração erra de propósito (kappa <= 0), mas na avaliação dá nota maior para B
        juiz = ClienteChatFalso([
            _resp_json({"vencedor": "A", "nota_a": 4, "nota_b": 2, "justificativa": "x"}),
            _resp_json({"vencedor": "B", "nota_a": 2, "nota_b": 4, "justificativa": "x"}),
            _resp_json({"vencedor": "B", "nota_a": 2, "nota_b": 4, "justificativa": "x"}),
            _resp_json({"vencedor": "A", "nota_a": 4, "nota_b": 2, "justificativa": "x"}),
            # avaliação
            _resp_json({"vencedor": "B", "nota_a": 1, "nota_b": 5, "justificativa": "b"}),
            _resp_json({"vencedor": "A", "nota_a": 5, "nota_b": 1, "justificativa": "b"}),
            _resp_json({"vencedor": "B", "nota_a": 1, "nota_b": 5, "justificativa": "b"}),
            _resp_json({"vencedor": "A", "nota_a": 5, "nota_b": 1, "justificativa": "b"}),
        ])
        out = ep.avaliar_prompts(dados, gerador, juiz, limiar_kappa=0.60, n_bootstrap=200)
        self.assertFalse(out["calibracao"]["juiz_calibrado"])
        self.assertTrue(out["avaliacao"]["bootstrap"]["significativo"])
        self.assertFalse(out["promover_b"])

    def test_portao_promove_b_quando_calibrado_e_significativo(self):
        dados = ep.carregar_casos()
        subset = {
            "pares_calibracao": dados["pares_calibracao"][:4],
            "casos_avaliacao": dados["casos_avaliacao"][:4],
        }
        gerador = ClienteChatFalso([
            RespostaChat("r"), RespostaChat("r [T1]"),
            RespostaChat("r"), RespostaChat("r [T1]"),
            RespostaChat("r"), RespostaChat("r [T1]"),
            RespostaChat("r"), RespostaChat("r [T1]"),
        ])
        respostas_juiz = []
        for par in subset["pares_calibracao"]:
            jh = par["julgamento_humano"]
            respostas_juiz.append(_resp_json({"vencedor": jh, "nota_a": 4, "nota_b": 4, "justificativa": "ok"}))
            inv = "B" if jh == "A" else ("A" if jh == "B" else "empate")
            respostas_juiz.append(_resp_json({"vencedor": inv, "nota_a": 4, "nota_b": 4, "justificativa": "ok"}))
        for _ in subset["casos_avaliacao"]:
            respostas_juiz.append(_resp_json({"vencedor": "B", "nota_a": 2, "nota_b": 5, "justificativa": "melhor"}))
            respostas_juiz.append(_resp_json({"vencedor": "A", "nota_a": 5, "nota_b": 2, "justificativa": "melhor"}))
        out = ep.avaliar_prompts(subset, gerador, ClienteChatFalso(respostas_juiz), limiar_kappa=0.60, n_bootstrap=200)
        self.assertEqual(out["calibracao"]["kappa"], 1.0)
        self.assertTrue(out["promover_b"])

    def test_avaliar_prompts_executa_em_duas_fases_e_mede_latencia(self):
        dados = {
            "pares_calibracao": [
                {"id": "c1", "pergunta": "p1", "referencia": "r1", "resposta_a": "a", "resposta_b": "b", "julgamento_humano": "B"},
            ],
            "casos_avaliacao": [
                {"id": "e1", "contexto": "ctx", "pergunta": "p1", "referencia": "r1"},
                {"id": "e2", "contexto": "ctx", "pergunta": "p2", "referencia": "r2"},
            ],
        }
        gerador = ClienteChatFalso([
            RespostaChat("a1"), RespostaChat("b1 [T1]"),
            RespostaChat("a2"), RespostaChat("b2 [T1]"),
        ])
        juiz = ClienteChatFalso([
            _resp_json({"vencedor": "B", "nota_a": 2, "nota_b": 5, "justificativa": "ok"}),
            _resp_json({"vencedor": "A", "nota_a": 5, "nota_b": 2, "justificativa": "ok"}),
            _resp_json({"vencedor": "B", "nota_a": 2, "nota_b": 5, "justificativa": "ok"}),
            _resp_json({"vencedor": "A", "nota_a": 5, "nota_b": 2, "justificativa": "ok"}),
            _resp_json({"vencedor": "B", "nota_a": 2, "nota_b": 5, "justificativa": "ok"}),
            _resp_json({"vencedor": "A", "nota_a": 5, "nota_b": 2, "justificativa": "ok"}),
        ])
        observado = {}

        def ao_concluir():
            observado["chamadas_gerador"] = len(gerador.chamadas)
            observado["chamadas_juiz_antes"] = len(juiz.chamadas)

        out = ep.avaliar_prompts(dados, gerador, juiz, limiar_kappa=0.60, n_bootstrap=50, ao_concluir_geracao=ao_concluir)
        self.assertEqual(observado, {"chamadas_gerador": 4, "chamadas_juiz_antes": 0})
        self.assertEqual(len(juiz.chamadas), 6)
        lat = out["avaliacao"]["latencia_ms"]
        self.assertIsNotNone(lat["gerador"]["p50"])
        self.assertIsNotNone(lat["juiz"]["p95"])

    def test_executar_evals_real_separa_gerador_e_juiz(self):
        from contextlib import redirect_stdout
        import io
        from unittest.mock import patch
        import executar_evals_real as eer

        captura = {}

        def fake_avaliar(dados, cli_gen, cli_juiz, **kwargs):
            captura["gen"] = (cli_gen.base_url, cli_gen.modelo, cli_gen.reasoning_effort)
            captura["juiz"] = (cli_juiz.base_url, cli_juiz.modelo, cli_juiz.reasoning_effort)
            return {
                "calibracao": {"pares": 1, "kappa": 1.0, "limiar_kappa": 0.6, "juiz_calibrado": True, "vieses_posicao": 0},
                "avaliacao": {"casos": 1, "placar": {"A": 0, "B": 1, "empate": 0}, "vieses_posicao": 0, "bootstrap": {"significativo": True}},
                "promover_b": True,
                "casos": [],
            }

        with patch.object(ep, "avaliar_prompts", side_effect=fake_avaliar), redirect_stdout(io.StringIO()) as buf:
            rc = eer.main([
                "--llm-base-url", "http://127.0.0.1:11434/v1",
                "--llm-modelo", "qwen3:4b-instruct",
                "--juiz-modelo", "qwen3.8:27b-ud-iq3_xxs",
                "--juiz-reasoning-effort", "none",
            ])
        self.assertEqual(rc, 0)
        self.assertEqual(captura["gen"], ("http://127.0.0.1:11434/v1", "qwen3:4b-instruct", None))
        self.assertEqual(captura["juiz"], ("http://127.0.0.1:11434/v1", "qwen3.8:27b-ud-iq3_xxs", "none"))
        saida = json.loads(buf.getvalue())
        self.assertEqual(saida["configuracao"]["juiz_modelo"], "qwen3.8:27b-ud-iq3_xxs")


class TestMultimodal(unittest.TestCase):
    def test_pdf_para_png_pdftoppm_payload_e_extracao_com_reparo(self):
        pdf = em.gerar_pdf_recibo_aurora()
        pngs = em.renderizar_pdf_pngs(pdf, dpi=100)
        self.assertEqual(len(pngs), 1)
        self.assertTrue(pngs[0].startswith(b"\x89PNG\r\n\x1a\n"))

        vlm = ClienteChatFalso([
            RespostaChat("{json invalido"),
            _resp_json({
                "documento": "REC-2026-0042",
                "data_emissao": "2026-11-24",
                "itens": [
                    {"descricao": "Segunda via de diploma", "quantidade": 1, "valor_unitario": 120.0, "subtotal": 120.0},
                    {"descricao": "Historico escolar", "quantidade": 2, "valor_unitario": 25.0, "subtotal": 50.0},
                    {"descricao": "Cartao biblioteca", "quantidade": 1, "valor_unitario": 18.0, "subtotal": 18.0},
                ],
                "total_informado": 188.0,
            }),
        ])
        out = em.extrair_fatura_de_pdf(pdf, vlm, dpi=100)
        self.assertEqual(out["metadados_llm"]["reparos"], 1)
        self.assertTrue(out["auditoria_totais"]["valido"])
        self.assertEqual(out["auditoria_totais"]["soma_calculada"], 188.0)
        parte_img = vlm.chamadas[0]["mensagens"][1]["content"][1]
        self.assertEqual(parte_img["type"], "image_url")
        self.assertTrue(parte_img["image_url"]["url"].startswith("data:image/png;base64,"))

    def test_auditoria_detecta_divergencia_aritmetica(self):
        f = em.FaturaExtraida(
            documento="REC-1",
            data_emissao="2026-11-24",
            itens=[em.ItemFatura(descricao="Taxa", quantidade=2, valor_unitario=25.0, subtotal=40.0)],
            total_informado=50.0,
        )
        aud = em.validar_totais_fatura(f)
        self.assertFalse(aud["valido"])
        self.assertEqual(len(aud["divergencias"]), 2)


if __name__ == "__main__":
    unittest.main()
