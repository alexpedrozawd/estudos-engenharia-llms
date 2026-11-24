"""Runner determinístico dos laboratórios e testes práticos (só biblioteca padrão).

Uso:
    python3 -I -W error::ResourceWarning laboratorios/executar_labs.py [--alvo SUBPASTA]
"""
import argparse
import os
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alvo", help="subpasta específica dentro de laboratorios/ (ex.: comum, lab_01)")
    args = parser.parse_args()

    inicio = os.path.join(AQUI, args.alvo) if args.alvo else AQUI
    if not os.path.isdir(inicio):
        print(f"FALHA pasta de laboratório não encontrada: {inicio}")
        return 1

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=inicio, pattern="test_*.py", top_level_dir=AQUI)
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
