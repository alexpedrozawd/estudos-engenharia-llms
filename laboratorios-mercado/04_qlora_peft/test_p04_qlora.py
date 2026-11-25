"""Smoke-tests offline do projeto 04 (sem torch/peft: receita, divisão, manifesto e portão por fatia)."""
import json
import os
import tempfile
import unittest

import qlora_receita as qr
import treinar_qlora as tq


class TestDados(unittest.TestCase):
    def setUp(self):
        self.exemplos = qr.carregar_jsonl(tq.DADOS)

    def test_dataset_balanceado(self):
        self.assertEqual(len(self.exemplos), 36)
        fatias = {(e["fatia"], e["categoria"]) for e in self.exemplos}
        self.assertEqual(len(fatias), 12)

    def test_divisao_estratificada_e_estavel(self):
        tr1, te1 = qr.dividir(self.exemplos, 0.34, "aurora-v1")
        tr2, te2 = qr.dividir(list(reversed(self.exemplos)), 0.34, "aurora-v1")
        self.assertEqual([e["id"] for e in te1], [e["id"] for e in te2])
        self.assertEqual((len(tr1), len(te1)), (24, 12))
        self.assertFalse({e["id"] for e in tr1} & {e["id"] for e in te1})
        self.assertEqual(len({(e["fatia"], e["categoria"]) for e in te1}), 12)
        _, te3 = qr.dividir(self.exemplos, 0.34, "outra-semente")
        self.assertNotEqual([e["id"] for e in te1], [e["id"] for e in te3])

    def test_validacao_de_linhas(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                f.write(json.dumps({"id": "1", "fatia": "a", "categoria": "inexistente", "texto": "t"}) + "\n")
            with self.assertRaises(ValueError):
                qr.carregar_jsonl(p)


class TestReceita(unittest.TestCase):
    def test_conversa_e_extracao(self):
        conv = qr.para_conversa({"texto": "esqueci a senha", "categoria": "acesso"})
        self.assertEqual([m["role"] for m in conv["messages"]], ["system", "user", "assistant"])
        self.assertEqual(qr.extrair_categoria(conv["messages"][2]["content"]), ("acesso", True))
        self.assertEqual(qr.extrair_categoria("A categoria é financeiro."), ("financeiro", False))
        self.assertEqual(qr.extrair_categoria("financeiro ou acesso"), (None, False))
        self.assertEqual(qr.extrair_categoria('{"categoria": "outra"}'), (None, False))

    def test_config_invalida(self):
        with self.assertRaises(ValueError):
            qr.ConfigQLoRA(lora_dropout=1.0).validar()
        with self.assertRaises(ValueError):
            qr.ConfigQLoRA(quant_tipo="int8").validar()
        with self.assertRaises(ValueError):
            qr.ConfigQLoRA(dtype_computo="int4").validar()
        qr.ConfigQLoRA(quant_4bit=False, dtype_computo="bfloat16").validar()

    def test_manifesto_reproduzivel(self):
        cfg = qr.ConfigQLoRA()
        ex = qr.carregar_jsonl(tq.DADOS)
        tr, te = qr.dividir(ex, cfg.fracao_teste, cfg.semente_divisao)
        m1 = qr.manifesto(cfg, tq.DADOS, tr, te, {"peft": "x"})
        m2 = qr.manifesto(qr.ConfigQLoRA(), tq.DADOS, tr, te, {"peft": "x"})
        self.assertEqual(m1, m2)
        m3 = qr.manifesto(qr.ConfigQLoRA(lora_r=8), tq.DADOS, tr, te, {"peft": "x"})
        self.assertNotEqual(m1["sha256_configuracao"], m3["sha256_configuracao"])
        self.assertEqual(m1["configuracao"]["quant_tipo"], "nf4")


class TestAvaliacaoPorFatia(unittest.TestCase):
    def setUp(self):
        cfg = qr.ConfigQLoRA()
        _, self.teste = qr.dividir(qr.carregar_jsonl(tq.DADOS), cfg.fracao_teste, cfg.semente_divisao)
        self.gabarito = {e["texto"]: e for e in self.teste}

    def _modelo(self, erra_fatia=(), sem_json=False):
        erra = {erra_fatia} if isinstance(erra_fatia, str) else set(erra_fatia)

        def prever(texto):
            ex = self.gabarito[texto]
            cat = "financeiro" if ex["fatia"] in erra and ex["categoria"] != "financeiro" else ex["categoria"]
            return cat if sem_json else json.dumps({"categoria": cat})
        return prever

    def test_portao_bloqueia_regressao_em_fatia(self):
        antes = qr.avaliar(self.teste, self._modelo(erra_fatia="com_ruido", sem_json=True))
        self.assertEqual(antes["por_fatia"]["com_ruido"]["acuracia"], 0.25)
        self.assertEqual(antes["taxa_formato"], 0.0)
        melhor = qr.avaliar(self.teste, self._modelo())
        r = qr.comparar(antes, melhor)
        self.assertTrue(r["aprovado"])
        self.assertEqual(r["delta_por_fatia"]["com_ruido"], 0.75)
        # Média sobe (0,50 -> 0,75), mas a fatia "formal" cai de 1,00 para 0,25: portão reprova.
        antes2 = qr.avaliar(self.teste, self._modelo(erra_fatia=("informal", "com_ruido")))
        pior_em_formal = qr.avaliar(self.teste, self._modelo(erra_fatia="formal"))
        r2 = qr.comparar(antes2, pior_em_formal)
        self.assertEqual(r2["delta_global"], 0.25)
        self.assertFalse(r2["aprovado"])
        self.assertTrue(any(x.startswith("formal") for x in r2["regressoes"]))

    def test_cli_comparar_codigo_de_saida(self):
        antes = qr.avaliar(self.teste, self._modelo(erra_fatia="informal"))
        depois = qr.avaliar(self.teste, self._modelo())
        with tempfile.TemporaryDirectory() as d:
            pa, pd = os.path.join(d, "a.json"), os.path.join(d, "d.json")
            for p, obj in ((pa, antes), (pd, depois)):
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(obj, f)
            from contextlib import redirect_stdout
            import io
            with redirect_stdout(io.StringIO()):
                self.assertEqual(tq.main(["comparar", pa, pd]), 0)
                self.assertEqual(tq.main(["comparar", pd, pa]), 2)

    def test_filtrar_kwargs_por_assinatura(self):
        class Fake:
            def __init__(self, output_dir, max_length=1):
                pass
        self.assertEqual(tq._filtrar_kwargs(Fake, {"output_dir": "x", "max_seq_length": 2, "max_length": 3}),
                         {"output_dir": "x", "max_length": 3})

    def test_detectar_acelerador_cuda_rocm_e_cpu(self):
        from types import SimpleNamespace

        torch_cpu = SimpleNamespace(cuda=SimpleNamespace(is_available=lambda: False))
        self.assertEqual(tq.detectar_acelerador(torch_cpu)["backend"], "cpu")

        torch_rocm = SimpleNamespace(
            version=SimpleNamespace(hip="7.14.0-abc", cuda=None),
            cuda=SimpleNamespace(is_available=lambda: True, get_device_name=lambda _i: "AMD Radeon RX 9070 XT"),
        )
        acel_rocm = tq.detectar_acelerador(torch_rocm)
        self.assertEqual(acel_rocm, {
            "disponivel": True,
            "backend": "rocm",
            "dispositivo": "AMD Radeon RX 9070 XT",
            "versao_runtime": "7.14.0-abc",
        })

        torch_cuda = SimpleNamespace(
            version=SimpleNamespace(hip=None, cuda="12.6"),
            cuda=SimpleNamespace(is_available=lambda: True, get_device_name=lambda _i: "NVIDIA L4"),
        )
        self.assertEqual(tq.detectar_acelerador(torch_cuda)["backend"], "cuda")

    def test_avaliar_http_sem_base_url_retorna_erro_cli(self):
        from contextlib import redirect_stdout
        import io

        with redirect_stdout(io.StringIO()):
            rc = tq.main(["avaliar", "--modelo", "m", "--saida", "x.json"])
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
