"""Testes offline do Laboratório 10."""
import json
import unittest

from lab_10_ferramentas_mcp.registro import Ferramenta, registro_aurora, servidor


def chamada(nome, args, meta=None, rid=1):
    params = {"name": nome, "arguments": args}
    if meta:
        params["_meta"] = meta
    return json.dumps({"jsonrpc": "2.0", "id": rid, "method": "tools/call", "params": params})


class TestLab10Ferramentas(unittest.TestCase):
    def setUp(self):
        self.r = registro_aurora()

    def test_listar_expoe_schema_estrito(self):
        resp = json.loads(servidor(self.r, '{"jsonrpc": "2.0", "id": 7, "method": "tools/list"}'))
        nomes = [t["name"] for t in resp["result"]["tools"]]
        self.assertEqual(nomes, ["abrir_chamado", "consultar_prazo"])
        schema = resp["result"]["tools"][0]["inputSchema"]
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["prioridade"], {"type": "integer"})

    def test_validacao_recusa_com_erro_legivel(self):
        casos = [("apagar_aluno", {"id": 9}, "inexistente"),
                 ("abrir_chamado", {"assunto": "boleto", "prioridade": "alta"}, "deve ser integer"),
                 ("abrir_chamado", {"assunto": "b", "prioridade": 2, "copiar_para": "x@y"}, "extras=['copiar_para']")]
        for nome, args, trecho in casos:
            res = json.loads(servidor(self.r, chamada(nome, args)))["result"]
            self.assertTrue(res["isError"], nome)
            self.assertIn(trecho, res["content"][0]["text"])

    def test_escrita_exige_aprovacao_e_e_idempotente(self):
        args = {"assunto": "boleto", "prioridade": 2}
        self.assertIn("aprovação", self.r.chamar("abrir_chamado", args)["content"][0]["text"])
        self.assertTrue(self.r.chamar("abrir_chamado", args, aprovado=True)["isError"])
        r1 = self.r.chamar("abrir_chamado", args, aprovado=True, chave_idempotencia="k-1")
        r2 = self.r.chamar("abrir_chamado", args, aprovado=True, chave_idempotencia="k-1")
        self.assertEqual(r1, r2)
        self.assertEqual(r1["content"][0]["text"], "CH-0001 (boleto, p2)")
        r3 = self.r.chamar("abrir_chamado", args, aprovado=True, chave_idempotencia="k-2")
        self.assertEqual(r3["content"][0]["text"], "CH-0002 (boleto, p2)")

    def test_leitura_metodo_desconhecido_e_duplicata(self):
        ok = json.loads(servidor(self.r, chamada("consultar_prazo", {"politica": "POL-01"})))
        self.assertEqual(ok["result"]["content"][0]["text"], "7")
        err = json.loads(servidor(self.r, '{"jsonrpc": "2.0", "id": 3, "method": "tools/apagar"}'))
        self.assertEqual(err["error"]["code"], -32601)
        self.assertEqual(json.loads(servidor(self.r, "{quebrado"))["error"]["code"], -32700)
        with self.assertRaises(ValueError):
            self.r.registrar(Ferramenta("consultar_prazo", "dup", {}, lambda: None))


if __name__ == "__main__":
    unittest.main()
