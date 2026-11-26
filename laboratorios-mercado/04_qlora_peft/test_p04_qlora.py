"""Smoke-tests offline do projeto 04 (sem torch/peft: receita, divisão, manifesto e portão por fatia)."""
import json
import os
import tempfile
import unittest
from collections import Counter

import qlora_receita as qr
import treinar_qlora as tq


class TestDadosSinteticos(unittest.TestCase):
    def test_normalizacao_e_quase_duplicata(self):
        from mercado_base import dados_sinteticos as ds
        self.assertEqual(ds.normalizar("  Olá,   MUNDO! "), "ola mundo")
        mantidos, desc = ds.deduplicar(["Boleto não chegou", "boleto nao chegou!", "boleto nao chegou ainda",
                                        "senha do AVA", ""], limiar=0.6, existentes=["Senha do ava."])
        self.assertEqual(mantidos, [0])
        self.assertEqual([d["motivo"] for d in desc], ["exata", "quase_duplicata", "exata", "vazio"])
        with self.assertRaises(ValueError):
            ds.deduplicar(["x"], limiar=0)

    def test_agrupamento_transitivo(self):
        from mercado_base import dados_sinteticos as ds
        vet = [[1, 0], [1, 0.1], [1, 0.2], [0, 1]]
        rot = ds.agrupar(4, lambda i, j: ds.cosseno(vet[i], vet[j]), 0.99)
        self.assertEqual(rot, [0, 0, 0, 3])
        self.assertEqual(ds.cosseno([0, 0], [1, 0]), 0.0)
        with self.assertRaises(ValueError):
            ds.cosseno([1], [1, 0])

    def test_divisao_por_grupo_sem_vazamento(self):
        ex = [{"id": f"x{i:02d}", "fatia": "f", "categoria": "acesso", "texto": str(i), "grupo": f"g{i // 3}"}
              for i in range(12)]
        tr, va, te = qr.dividir_com_validacao(ex, 0.25, 0.25, "s")
        grupos = [{e["grupo"] for e in c} for c in (tr, va, te)]
        self.assertFalse(grupos[0] & grupos[1] or grupos[0] & grupos[2] or grupos[1] & grupos[2])
        self.assertEqual(sum(map(len, (tr, va, te))), 12)


class TestCicloQLoRA(unittest.TestCase):
    def test_escolha_de_epocas_na_validacao(self):
        import executar_ciclo_qlora as ciclo
        self.assertEqual(ciclo.escolher_epocas({1: {"acuracia": 0.8}, 3: {"acuracia": 0.9}, 6: {"acuracia": 0.9}}), 3)
        self.assertEqual(ciclo.escolher_epocas({1: {"acuracia": 0.95}, 6: {"acuracia": 0.9}}), 1)

    def test_ciclo_recusa_pasta_de_outros_dados(self):
        import executar_ciclo_qlora as ciclo
        from contextlib import redirect_stdout
        import io
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "impressao.json"), "w", encoding="utf-8") as f:
                f.write("{}")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(ciclo.main(["--pasta", d, "--sem-registro"]), 3)

    def test_registro_real_do_ciclo(self):
        import glob
        regs = sorted(glob.glob(os.path.join(tq.AQUI, "..", "execucoes", "p04-qlora-ciclo-*.json")))
        self.assertTrue(regs)
        with open(regs[-1], encoding="utf-8") as f:
            r = json.load(f)
        import executar_ciclo_qlora as ciclo
        val = {int(k[2:]): v for k, v in r["validacao"].items() if k != "base"}
        self.assertEqual(r["epocas_escolhidas"], ciclo.escolher_epocas(val))
        self.assertEqual(set(r["teste"]), {"base", f"ep{r['epocas_escolhidas']}"})
        par = r["portao"]["pareado"]
        base, adapt = r["acertos_por_caso"]["base"], r["acertos_por_caso"][f"ep{r['epocas_escolhidas']}"]
        self.assertEqual(par["ganhos"], sum(1 for i in base if not base[i] and adapt[i]))
        self.assertEqual(par["perdas"], sum(1 for i in base if base[i] and not adapt[i]))
        self.assertEqual(r["portao"]["veredito"], "aprovado")


class TestDados(unittest.TestCase):
    def setUp(self):
        self.exemplos = qr.carregar_jsonl(tq.DADOS)

    def test_dataset_balanceado(self):
        self.assertEqual(len(self.exemplos), 360)
        estratos = Counter((e["fatia"], e["categoria"]) for e in self.exemplos)
        self.assertEqual(len(estratos), 12)
        self.assertEqual(set(estratos.values()), {30})
        manuais = [e for e in self.exemplos if e["origem"] == "manual"]
        self.assertEqual([e["id"] for e in manuais], [f"c{i:02d}" for i in range(1, 37)])
        self.assertEqual({e["origem"] for e in self.exemplos}, {"manual", "sintetico-llm"})

    def test_dados_sem_pii_nem_duplicata(self):
        from mercado_base import dados_sinteticos as ds
        from mercado_base.pii import detectar_pii
        textos = [e["texto"] for e in self.exemplos]
        self.assertEqual([t for t in textos if detectar_pii(t)], [])
        mantidos, descartes = ds.deduplicar(textos, limiar=0.6)
        self.assertEqual(descartes, [])
        self.assertEqual(len(mantidos), len(textos))

    def test_grupos_nunca_se_dividem(self):
        tr, va, te = qr.dividir_com_validacao(self.exemplos, 0.2, 0.34, "aurora-v1")
        self.assertEqual((len(tr), len(va), len(te)), (163, 74, 123))
        lado = {}
        for nome, conj in (("treino", tr), ("validacao", va), ("teste", te)):
            for e in conj:
                lado.setdefault(e["grupo"], set()).add(nome)
        self.assertTrue(all(len(v) == 1 for v in lado.values()))
        self.assertGreater(sum(1 for e in self.exemplos if e["grupo"] != e["id"]), 0)

    def test_divisao_estratificada_e_estavel(self):
        tr1, te1 = qr.dividir(self.exemplos, 0.34, "aurora-v1")
        tr2, te2 = qr.dividir(list(reversed(self.exemplos)), 0.34, "aurora-v1")
        self.assertEqual([e["id"] for e in te1], [e["id"] for e in te2])
        self.assertEqual((len(tr1), len(te1)), (237, 123))
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
        # Só os 36 manuais (12 casos de teste): o portão mostra o limite de amostras pequenas.
        cfg = qr.ConfigQLoRA()
        manuais = [e for e in qr.carregar_jsonl(tq.DADOS) if e["origem"] == "manual"]
        _, self.teste = qr.dividir(manuais, cfg.fracao_teste, cfg.semente_divisao)
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
        # Só 3 casos mudaram (todos ganhos): McNemar exato p = 0,25, então não se promove.
        self.assertFalse(r["aprovado"])
        self.assertEqual(r["veredito"], "inconclusivo")
        self.assertEqual(r["pareado"], {"ganhos": 3, "perdas": 0, "p_valor_mcnemar_exato": 0.25})
        self.assertEqual(r["delta_por_fatia"]["com_ruido"], 0.75)
        # Com 6 ganhos e 0 perdas (p = 0,03125 < 0,05), o mesmo portão aprova.
        antes_duas = qr.avaliar(self.teste, self._modelo(erra_fatia=("informal", "com_ruido")))
        r_sig = qr.comparar(antes_duas, melhor)
        self.assertTrue(r_sig["aprovado"])
        self.assertEqual(r_sig["veredito"], "aprovado")
        # Média sobe (0,50 -> 0,75), mas a fatia "formal" cai de 1,00 para 0,25: portão reprova.
        antes2 = qr.avaliar(self.teste, self._modelo(erra_fatia=("informal", "com_ruido")))
        pior_em_formal = qr.avaliar(self.teste, self._modelo(erra_fatia="formal"))
        r2 = qr.comparar(antes2, pior_em_formal)
        self.assertEqual(r2["delta_global"], 0.25)
        self.assertFalse(r2["aprovado"])
        self.assertEqual(r2["veredito"], "reprovado")
        self.assertTrue(any(x.startswith("formal") for x in r2["regressoes"]))

    def test_sem_detalhes_por_caso_e_inconclusivo(self):
        antes = qr.avaliar(self.teste, self._modelo(erra_fatia=("informal", "com_ruido")))
        depois = qr.avaliar(self.teste, self._modelo())
        for r in (antes, depois):
            r.pop("detalhes")
        out = qr.comparar(antes, depois)
        self.assertEqual(out["veredito"], "inconclusivo")
        self.assertIsNone(out["pareado"])

    def test_cli_comparar_codigo_de_saida(self):
        antes = qr.avaliar(self.teste, self._modelo(erra_fatia=("informal", "com_ruido")))
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

    def test_cli_recusa_conjuntos_diferentes(self):
        antes = qr.avaliar(self.teste, self._modelo(erra_fatia=("informal", "com_ruido")))
        depois = dict(qr.avaliar(self.teste, self._modelo()), conjunto="validacao")
        with tempfile.TemporaryDirectory() as d:
            pa, pd = os.path.join(d, "a.json"), os.path.join(d, "d.json")
            for p, obj in ((pa, antes), (pd, depois)):
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(obj, f)
            from contextlib import redirect_stdout
            import io
            with redirect_stdout(io.StringIO()):
                self.assertEqual(tq.main(["comparar", pa, pd]), 2)

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

class TestEstatisticaEValidacao(unittest.TestCase):
    def test_wilson_registro_rocm(self):
        # Registro de 25/11/2026: 8/12 antes e 11/12 depois; as faixas de 95% se sobrepõem.
        self.assertEqual(qr.wilson(8, 12), (0.3906, 0.8619))
        self.assertEqual(qr.wilson(11, 12), (0.6461, 0.9851))
        self.assertEqual(qr.wilson(0, 0), (0.0, 1.0))

    def test_mcnemar_exato(self):
        self.assertEqual(qr.mcnemar_exato(3, 0), 0.25)
        self.assertEqual(qr.mcnemar_exato(6, 0), 0.03125)
        self.assertEqual(qr.mcnemar_exato(0, 0), 1.0)
        self.assertEqual(qr.mcnemar_exato(2, 2), 1.0)

    def test_validacao_separada_preserva_teste(self):
        ex = qr.carregar_jsonl(tq.DADOS)
        tr0, te0 = qr.dividir(ex, 0.34, "aurora-v1")
        tr, va, te = qr.dividir_com_validacao(ex, 0.2, 0.34, "aurora-v1")
        self.assertEqual(te, te0)
        self.assertEqual(len(va), 74)
        ids = [e["id"] for e in tr + va + te]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(sorted(ids), sorted(e["id"] for e in ex))
        self.assertEqual(qr.dividir_com_validacao(ex, 0.0, 0.34, "aurora-v1"), (tr0, [], te0))
        m = qr.manifesto(qr.ConfigQLoRA(fracao_validacao=0.2), tq.DADOS, tr, te, {}, validacao=va)
        self.assertEqual(len(m["ids_validacao"]), 74)
        with self.assertRaises(ValueError):
            qr.ConfigQLoRA(fracao_validacao=0.7).validar()

    def test_cli_avaliar_validacao_vazia(self):
        from contextlib import redirect_stdout
        import io
        with redirect_stdout(io.StringIO()):
            self.assertEqual(tq.main(["avaliar", "--backend", "http", "--base-url", "http://127.0.0.1:9/v1",
                                      "--modelo", "x", "--conjunto", "validacao", "--saida", os.devnull]), 2)


if __name__ == "__main__":
    unittest.main()
