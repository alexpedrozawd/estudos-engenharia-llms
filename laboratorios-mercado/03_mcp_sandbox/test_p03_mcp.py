"""Smoke-tests offline do projeto 03: MCP em processo (SDK real), executor falso e flags do container."""
import asyncio
import subprocess
import unittest

import mcp_cliente_aurora as cli
import mcp_ferramentas as srvmod
import mcp_sandbox_exec as sx
from mcp import Client


class ExecutorFalso:
    def __init__(self):
        self.codigos = []

    def executar(self, codigo):
        self.codigos.append(codigo)
        return sx.ResultadoExecucao(0, "ok\n", "", False, ("falso",))


def rodar(coro):
    return asyncio.run(coro)


class TestServidorMCP(unittest.TestCase):
    def test_demonstracao_com_aprovacao(self):
        exe, audit = ExecutorFalso(), []
        srv = srvmod.criar_servidor(executor=exe, auditoria=audit)
        out = rodar(cli.demonstrar(srv, cli.aprovador_automatico))
        self.assertEqual(out["ferramentas"]["consultar_prazo"], {"somente_leitura": True, "destrutiva": False})
        self.assertTrue(out["ferramentas"]["executar_python_isolado"]["destrutiva"])
        self.assertEqual(out["consultar_prazo"], srvmod.PRAZOS["rematricula"])
        self.assertEqual(out["calcular_media_ponderada"], {"media": 6.7, "aprovado": True, "regra": "aprovado se média >= 6,0"})
        self.assertTrue(out["validacao_rejeita_nota_11"])
        self.assertTrue(out["executar_python_isolado"]["executado"])
        self.assertEqual(out["executar_python_isolado"]["aprovado_por"], "demonstracao-automatica")
        self.assertEqual(exe.codigos, [cli.CODIGO_DEMO, cli.CODIGO_REDE])
        self.assertEqual(out["executar_python_isolado"]["sha256_codigo"], srvmod.sha_codigo(cli.CODIGO_DEMO))
        self.assertEqual([a["decisao"] for a in audit], ["aprovado", "aprovado"])

    def test_negacao_humana_nao_executa(self):
        exe, audit = ExecutorFalso(), []
        out = rodar(cli.demonstrar(srvmod.criar_servidor(executor=exe, auditoria=audit), cli.aprovador_negar))
        self.assertFalse(out["executar_python_isolado"]["executado"])
        self.assertEqual(exe.codigos, [])
        self.assertEqual(audit[0]["decisao"], "negado")

    def test_cliente_sem_elicitation_falha_fechado(self):
        exe = ExecutorFalso()
        srv = srvmod.criar_servidor(executor=exe)

        async def chamar():
            async with Client(srv, mode="legacy") as c:
                return (await c.call_tool("executar_python_isolado", {"codigo": "print(1)"})).structured_content

        r = rodar(chamar())
        self.assertFalse(r["executado"])
        self.assertIn("negado por padrão", r["motivo"])
        self.assertEqual(exe.codigos, [])

    def test_codigo_vazio_rejeitado_pela_validacao(self):
        async def chamar():
            async with Client(srvmod.criar_servidor(executor=ExecutorFalso()), mode="legacy",
                              elicitation_callback=cli.criar_callback(cli.aprovador_automatico)) as c:
                return await c.call_tool("executar_python_isolado", {"codigo": ""})

        self.assertTrue(rodar(chamar()).is_error)


class TestSandbox(unittest.TestCase):
    def test_flags_de_isolamento(self):
        cmd = sx.montar_comando("print(1)", motor="docker", imagem="img", nome="n1")
        for flag in ("--rm", "--name=n1", "--network=none", "--read-only", "--cap-drop=ALL",
                     "--security-opt=no-new-privileges", "--pids-limit=64", "--memory=128m", "--cpus=0.5",
                     "--user=65534:65534"):
            self.assertIn(flag, cmd)
        self.assertEqual(cmd[0], "docker")
        self.assertEqual(cmd[-5:], ["img", "python", "-I", "-c", "print(1)"])
        with self.assertRaises(ValueError):
            sx.montar_comando("x", motor="sh")

    def test_escolha_de_motor(self):
        self.assertEqual(sx.escolher_motor({"MCP_SANDBOX_MOTOR": "docker"}), "docker")
        self.assertEqual(sx.escolher_motor({}, which=lambda m: "/usr/bin/docker" if m == "docker" else None), "docker")
        with self.assertRaises(RuntimeError):
            sx.escolher_motor({}, which=lambda m: None)
        with self.assertRaises(ValueError):
            sx.escolher_motor({"MCP_SANDBOX_MOTOR": "bash"})

    def test_tempo_limite_remove_container(self):
        chamadas = []

        def run_falso(cmd, **kw):
            chamadas.append(cmd)
            if cmd[1] == "run":
                raise subprocess.TimeoutExpired(cmd, kw.get("timeout"), output="parcial")
            return subprocess.CompletedProcess(cmd, 0, "", "")

        r = sx.ExecutorConteiner(motor="podman", executar_processo=run_falso, tempo_limite_s=1).executar("while True: pass")
        self.assertTrue(r.expirou)
        self.assertEqual(r.saida, "parcial")
        self.assertEqual(chamadas[1][:3], ["podman", "rm", "-f"])
        self.assertTrue(chamadas[1][3].startswith("mcp-sandbox-"))

    def test_saida_truncada(self):
        def run_falso(cmd, **kw):
            return subprocess.CompletedProcess(cmd, 0, "x" * 5000, "")

        r = sx.ExecutorConteiner(motor="podman", executar_processo=run_falso).executar("print()")
        self.assertTrue(r.saida.endswith("[saída truncada]"))


if __name__ == "__main__":
    unittest.main()
