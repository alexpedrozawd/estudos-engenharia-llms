"""Runner dos smoke-tests offline da Camada 3 (laboratorios-mercado).

Não acessa rede, containers nem GPU: usa transportes falsos (httpx.MockTransport),
armazéns em memória, MCP em processo e relógios injetados.

Uso:
    .venv-mercado/bin/python -I -W error::ResourceWarning laboratorios-mercado/executar_smoke.py [--alvo 01_serving_local]
"""
import argparse
import os
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import mercado_base  # noqa: E402  (prepara sys.path dos projetos e de laboratorios/)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # `k8s` (Etapa 6a) não é projeto de laboratório: só os testes offline dos manifests Kubernetes.
    ap.add_argument("--alvo", choices=mercado_base.PROJETOS + ("k8s",), help="executa só um projeto")
    args = ap.parse_args()
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for projeto in [args.alvo] if args.alvo else mercado_base.PROJETOS + ("k8s",):
        pasta = os.path.join(AQUI, projeto)
        suite.addTests(loader.discover(start_dir=pasta, pattern="test_*.py", top_level_dir=pasta))
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    if resultado.testsRun == 0:
        print("FALHA nenhum teste encontrado")
        return 1
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
