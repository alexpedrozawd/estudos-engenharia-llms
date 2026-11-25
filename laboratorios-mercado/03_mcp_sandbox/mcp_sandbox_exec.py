"""Execução isolada de código em container restrito (projeto 03).

Cada execução cria um container descartável sem rede, com sistema de arquivos só leitura,
sem capabilities, sem escalada de privilégio, usuário sem privilégios e limites de memória,
CPU, processos e tempo. O código vai como argumento (`python -I -c`), nunca por shell.

Motor: `podman` (padrão) ou `docker`, escolhido por `MCP_SANDBOX_MOTOR` ou pelo PATH.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from typing import Callable, List, Optional

IMAGEM_PADRAO = os.environ.get("MCP_SANDBOX_IMAGEM", "docker.io/library/python:3.13-alpine")
LIMITE_SAIDA = 4000


@dataclass(frozen=True)
class ResultadoExecucao:
    codigo_saida: int
    saida: str
    erro: str
    expirou: bool
    comando: tuple


def escolher_motor(env=None, which: Callable[[str], Optional[str]] = shutil.which) -> str:
    # EXERCICIO-INICIO: respeite MCP_SANDBOX_MOTOR (só podman ou docker); senão o primeiro disponível no PATH; nenhum = erro.
    env = os.environ if env is None else env
    preferido = env.get("MCP_SANDBOX_MOTOR", "").strip()
    if preferido:
        if preferido not in ("podman", "docker"):
            raise ValueError("MCP_SANDBOX_MOTOR deve ser podman ou docker")
        return preferido
    for motor in ("podman", "docker"):
        if which(motor):
            return motor
    raise RuntimeError("nenhum motor de containers (podman/docker) encontrado")
    # EXERCICIO-FIM


def montar_comando(codigo: str, *, motor: str = "podman", imagem: str = IMAGEM_PADRAO, nome: str = "",
                   memoria: str = "128m", cpus: str = "0.5", pids: int = 64) -> List[str]:
    # EXERCICIO-INICIO: contêiner descartável sem rede, só leitura, sem capabilities, no-new-privileges e com limites de pids, memória e CPU.
    if motor not in ("podman", "docker"):
        raise ValueError("motor inválido")
    return [
        motor, "run", "--rm",
        *([f"--name={nome}"] if nome else []),
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        f"--pids-limit={pids}",
        f"--memory={memoria}",
        f"--cpus={cpus}",
        "--user=65534:65534",
        "--tmpfs=/tmp:rw,noexec,nosuid,size=16m",
        "--env=PYTHONDONTWRITEBYTECODE=1",
        imagem, "python", "-I", "-c", codigo,
    ]
    # EXERCICIO-FIM


def _cortar(texto: str) -> str:
    return texto if len(texto) <= LIMITE_SAIDA else texto[:LIMITE_SAIDA] + "\n[saída truncada]"


class ExecutorConteiner:
    """Executor real (subprocess). `executar_processo` é injetável para testes."""

    def __init__(self, motor: Optional[str] = None, imagem: str = IMAGEM_PADRAO, tempo_limite_s: float = 20.0,
                 executar_processo: Callable[..., subprocess.CompletedProcess] = subprocess.run):
        self.motor = motor or escolher_motor()
        self.imagem = imagem
        self.tempo_limite_s = tempo_limite_s
        self._run = executar_processo

    def executar(self, codigo: str) -> ResultadoExecucao:
        nome = f"mcp-sandbox-{uuid.uuid4().hex[:12]}"
        comando = montar_comando(codigo, motor=self.motor, imagem=self.imagem, nome=nome)
        try:
            p = self._run(comando, capture_output=True, text=True, timeout=self.tempo_limite_s,
                          stdin=subprocess.DEVNULL, check=False)
        except subprocess.TimeoutExpired as exc:
            # Matar o cliente não garante parar o container: remove pelo nome.
            self._run([self.motor, "rm", "-f", nome], capture_output=True, text=True, timeout=30, check=False)
            saida = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            return ResultadoExecucao(-1, _cortar(saida), "tempo limite excedido", True, tuple(comando))
        return ResultadoExecucao(p.returncode, _cortar(p.stdout), _cortar(p.stderr), False, tuple(comando))
