"""Kubernetes local (Etapa 6a): sobe P05, P06 e pgvector no kind com Podman, valida e registra.

Pré-requisitos no host (fora da imagem base): `kind` e `kubectl` (Homebrew) e Podman rootless com
delegação de cgroup (cpu, memory, io, pids). Imagem `localhost/laboratorios-mercado:dev` construída:
    podman build -f laboratorios-mercado/Containerfile -t localhost/laboratorios-mercado:dev .

Uso (a partir da raiz do repositório):
    .venv-mercado/bin/python -I laboratorios-mercado/k8s/executar_k8s_local.py subir
    .venv-mercado/bin/python -I laboratorios-mercado/k8s/executar_k8s_local.py validar   # grava em execucoes/
    .venv-mercado/bin/python -I laboratorios-mercado/k8s/executar_k8s_local.py remover

Segredos: gerados aleatoriamente no `subir`, enviados ao cluster por stdin (nunca por argumento de linha de
comando), lidos de volta só em memória no `validar` e nunca impressos nem gravados no registro.
"""
import argparse
import base64
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from typing import Dict, List, Optional, Tuple

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import mercado_base  # noqa: E402

import httpx  # noqa: E402

CLUSTER = "aurora-lab"
CONTEXTO = f"kind-{CLUSTER}"
NS = "aurora"
MANIFESTS = os.path.join(AQUI, "manifests")
IMAGEM_BASE = "localhost/laboratorios-mercado:dev"
IMAGEM_V1 = "localhost/laboratorios-mercado:k8s-v1"
IMAGEM_V2 = "localhost/laboratorios-mercado:k8s-v2"
IMAGEM_QUEBRADA = "localhost/laboratorios-mercado:k8s-inexistente"
IMAGEM_PG = "docker.io/pgvector/pgvector:pg17"
AMBIENTE = {**os.environ, "KIND_EXPERIMENTAL_PROVIDER": "podman"}


def rodar(cmd: List[str], *, entrada: Optional[str] = None, checar: bool = True, timeout: float = 300) -> str:
    r = subprocess.run(cmd, input=entrada, capture_output=True, text=True, env=AMBIENTE, timeout=timeout)
    if checar and r.returncode != 0:
        raise RuntimeError(f"falhou ({r.returncode}): {' '.join(cmd[:4])}…\n{r.stderr.strip()[-800:]}")
    return r.stdout


def kubectl(*args: str, **kw) -> str:
    return rodar(["kubectl", "--context", CONTEXTO, "-n", NS, *args], **kw)


def exigir_ferramentas() -> None:
    faltando = [f for f in ("kind", "kubectl", "podman") if shutil.which(f) is None]
    if faltando:
        raise SystemExit(f"Ferramentas ausentes: {', '.join(faltando)} (instale kind e kubernetes-cli pelo Homebrew)")


def cluster_existe() -> bool:
    return CLUSTER in rodar(["kind", "get", "clusters"], checar=False).split()


# --------------------------------------------------------------------------------------------- subir

def gerar_segredo() -> Dict[str, str]:
    senha_pg = secrets.token_urlsafe(24)
    aluno, admin, llmops = (secrets.token_urlsafe(24) for _ in range(3))
    return {
        "PG_SENHA": senha_pg,
        "PGVECTOR_DSN": f"postgresql://aurora:{senha_pg}@postgres:5432/rag",
        "INTEGRADOR_PERFIS_CHAVES": f"{aluno}:aluno,{admin}:admin",
        "LLMOPS_API_KEYS": llmops,
    }


def aplicar_segredo_se_ausente() -> bool:
    if kubectl("get", "secret", "aurora-segredos", "--ignore-not-found", "-o", "name").strip():
        return False
    manifesto = {"apiVersion": "v1", "kind": "Secret", "metadata": {"name": "aurora-segredos", "namespace": NS},
                 "type": "Opaque", "stringData": gerar_segredo()}
    kubectl("apply", "-f", "-", entrada=json.dumps(manifesto))
    return True


def carregar_imagens() -> None:
    for tag in (IMAGEM_V1, IMAGEM_V2):
        rodar(["podman", "tag", IMAGEM_BASE, tag])
    imagens = [IMAGEM_V1, IMAGEM_V2]
    if subprocess.run(["podman", "image", "exists", IMAGEM_PG], env=AMBIENTE).returncode == 0:
        imagens.append(IMAGEM_PG)  # evita baixar de novo dentro do nó
    with tempfile.TemporaryDirectory() as pasta:
        arquivo = os.path.join(pasta, "imagens.tar")
        rodar(["podman", "save", "-m", "--format", "docker-archive", "-o", arquivo, *imagens], timeout=600)
        rodar(["kind", "load", "image-archive", arquivo, "--name", CLUSTER], timeout=600)


def subir() -> None:
    if not cluster_existe():
        rodar(["kind", "create", "cluster", "--name", CLUSTER, "--wait", "120s"], timeout=600)
    carregar_imagens()
    rodar(["kubectl", "--context", CONTEXTO, "apply", "-f", os.path.join(MANIFESTS, "namespace.yaml")])
    novo = aplicar_segredo_se_ausente()
    rodar(["kubectl", "--context", CONTEXTO, "apply", "-k", MANIFESTS])
    esperar_tudo_pronto()
    print(f"cluster {CLUSTER} pronto; segredo {'gerado' if novo else 'reaproveitado'} (valores não exibidos)")


def esperar_tudo_pronto(timeout: str = "240s") -> None:
    kubectl("rollout", "status", "statefulset/postgres", f"--timeout={timeout}", timeout=300)
    for dep in ("api-llmops", "integrador"):
        kubectl("rollout", "status", f"deployment/{dep}", f"--timeout={timeout}", timeout=300)


# ------------------------------------------------------------------------------------------- validar

def ler_segredo() -> Dict[str, str]:
    dados = json.loads(kubectl("get", "secret", "aurora-segredos", "-o", "json"))["data"]
    return {k: base64.b64decode(v).decode() for k, v in dados.items()}


def porta_livre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Encaminhamento:
    """`kubectl port-forward` em primeiro plano durante o `with`; encerra ao sair."""

    def __init__(self, servico: str, porta_remota: int):
        self.porta = porta_livre()
        self.cmd = ["kubectl", "--context", CONTEXTO, "-n", NS, "port-forward", f"svc/{servico}",
                    f"{self.porta}:{porta_remota}", "--address", "127.0.0.1"]
        self.proc: Optional[subprocess.Popen] = None

    def __enter__(self) -> str:
        self.proc = subprocess.Popen(self.cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=AMBIENTE)
        url = f"http://127.0.0.1:{self.porta}"
        for _ in range(60):
            try:
                httpx.get(url + "/saude", timeout=1.0)
                return url
            except httpx.HTTPError:
                time.sleep(0.5)
        raise RuntimeError(f"port-forward para {self.cmd[6]} não respondeu")

    def __exit__(self, *exc) -> None:
        if self.proc:
            self.proc.terminate()
            self.proc.wait(timeout=10)


def checar(registro: List[Dict[str, object]], nome: str, ok: bool, **detalhes) -> None:
    registro.append({"verificacao": nome, "ok": bool(ok), **detalhes})
    print(f"{'OK   ' if ok else 'FALHA'} {nome} {json.dumps(detalhes, ensure_ascii=False)}")


def pod_de(app: str) -> str:
    return kubectl("get", "pods", "-l", f"app.kubernetes.io/name={app}", "--field-selector=status.phase=Running",
                   "-o", "jsonpath={.items[0].metadata.name}").strip()


def tcp_de_dentro(app: str, host: str, porta: int) -> str:
    codigo = (f"import socket;s=socket.socket();s.settimeout(4)\n"
              f"try:\n s.connect(('{host}',{porta}));print('conectou')\n"
              f"except Exception as e:\n print('bloqueado:'+type(e).__name__)")
    return kubectl("exec", pod_de(app), "--", "python", "-c", codigo, checar=False, timeout=30).strip()


SONDA_DISPONIBILIDADE = (
    "import time,urllib.request\n"
    "ok=falha=0;fim=time.time()+{segundos}\n"
    "while time.time()<fim:\n"
    " try:\n"
    "  urllib.request.urlopen('http://integrador:8001/saude',timeout=2).read();ok+=1\n"
    " except Exception:\n"
    "  falha+=1\n"
    " time.sleep(0.25)\n"
    "print(ok,falha)"
)


def iniciar_sonda(segundos: int) -> subprocess.Popen:
    """Mede disponibilidade do Service `integrador` de dentro do cluster (a partir de um pod do P05)."""
    cmd = ["kubectl", "--context", CONTEXTO, "-n", NS, "exec", pod_de("api-llmops"), "--",
           "python", "-c", SONDA_DISPONIBILIDADE.format(segundos=segundos)]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, env=AMBIENTE)


def resultado_sonda(proc: subprocess.Popen) -> Tuple[int, int]:
    saida, _ = proc.communicate(timeout=300)
    ok, falha = (int(x) for x in saida.split())
    return ok, falha


def imagem_integrador() -> str:
    return kubectl("get", "deployment/integrador", "-o", "jsonpath={.spec.template.spec.containers[0].image}")


def validar() -> str:
    verif: List[Dict[str, object]] = []
    # Estado inicial reprodutível: integrador na v1.
    if imagem_integrador() != IMAGEM_V1:
        kubectl("set", "image", "deployment/integrador", f"integrador={IMAGEM_V1}")
    esperar_tudo_pronto()
    seg = ler_segredo()
    # Só a chave de aluno é usada; a de admin existe para o vínculo chave → perfil.
    aluno = seg["INTEGRADOR_PERFIS_CHAVES"].split(",")[0].split(":")[0]

    pods = json.loads(kubectl("get", "pods", "-o", "json"))["items"]
    resumo_pods = [{
        "app": p["metadata"]["labels"].get("app.kubernetes.io/name"),
        "pronto": all(c.get("ready") for c in p["status"].get("containerStatuses", [])),
        "reinicios": sum(c.get("restartCount", 0) for c in p["status"].get("containerStatuses", [])),
    } for p in pods]
    checar(verif, "pods_prontos", all(p["pronto"] for p in resumo_pods), pods=len(resumo_pods))
    ns_rotulos = json.loads(rodar(["kubectl", "--context", CONTEXTO, "get", "ns", NS, "-o", "json"]))
    checar(verif, "namespace_restricted",
           ns_rotulos["metadata"]["labels"].get("pod-security.kubernetes.io/enforce") == "restricted")

    with Encaminhamento("api-llmops", 8000) as url:
        r = httpx.get(url + "/saude", timeout=5)
        checar(verif, "p05_saude", r.status_code == 200, status=r.status_code)
        r = httpx.post(url + "/v1/respostas", json={"prompt": "oi"}, timeout=10)
        checar(verif, "p05_sem_chave_401", r.status_code == 401, status=r.status_code)

    with Encaminhamento("integrador", 8001) as url:
        r = httpx.get(url + "/saude", timeout=5)
        checar(verif, "p06_saude", r.status_code == 200, status=r.status_code)
        corpo = {"pergunta": "Qual o prazo de trancamento?", "perfil": "aluno"}
        r = httpx.post(url + "/v1/assistente", json=corpo, timeout=10)
        checar(verif, "p06_sem_chave_401", r.status_code == 401, status=r.status_code)
        r = httpx.post(url + "/v1/assistente", json={**corpo, "perfil": "admin"},
                       headers={"X-API-Key": aluno}, timeout=10)
        checar(verif, "p06_anti_bfla_403", r.status_code == 403, status=r.status_code)
        t0 = time.perf_counter()
        r = httpx.post(url + "/v1/assistente", json=corpo, headers={"X-API-Key": aluno}, timeout=240)
        checar(verif, "p06_backend_inalcancavel_503", r.status_code == 503 and "Retry-After" in r.headers,
               status=r.status_code, retry_after=r.headers.get("Retry-After"),
               segundos=round(time.perf_counter() - t0, 2))

    p05 = tcp_de_dentro("api-llmops", "postgres", 5432)
    p06 = tcp_de_dentro("integrador", "postgres", 5432)
    checar(verif, "networkpolicy_postgres", p05.startswith("bloqueado") and p06 == "conectou",
           de_p05=p05, de_p06=p06)

    # Persistência: marcador sobrevive à recriação do pod do banco (StatefulSet + PVC).
    psql = ["exec", "postgres-0", "--", "psql", "-h", "127.0.0.1", "-U", "aurora", "-d", "rag", "-tAc"]
    kubectl(*psql, "CREATE TABLE IF NOT EXISTS marcador_k8s (v text); TRUNCATE marcador_k8s; "
                   "INSERT INTO marcador_k8s VALUES ('persistiu')")
    kubectl("delete", "pod", "postgres-0", "--wait=true", timeout=120)
    time.sleep(2)
    kubectl("rollout", "status", "statefulset/postgres", "--timeout=180s", timeout=200)
    for _ in range(30):
        valor = kubectl(*psql, "SELECT v FROM marcador_k8s", checar=False).strip()
        if valor:
            break
        time.sleep(2)
    checar(verif, "pvc_persistencia", valor == "persistiu", valor=valor)

    # Rollout bem-sucedido v1 -> v2, com sonda de disponibilidade pelo Service.
    sonda = iniciar_sonda(45)
    time.sleep(3)
    t0 = time.perf_counter()
    kubectl("set", "image", "deployment/integrador", f"integrador={IMAGEM_V2}")
    kubectl("rollout", "status", "deployment/integrador", "--timeout=180s", timeout=200)
    dur = round(time.perf_counter() - t0, 1)
    ok, falha = resultado_sonda(sonda)
    checar(verif, "rollout_v2_sem_indisponibilidade", falha == 0 and imagem_integrador() == IMAGEM_V2,
           segundos=dur, sonda_ok=ok, sonda_falha=falha)

    # Rollout quebrado (imagem inexistente): trava sem derrubar o serviço; rollback devolve a v2.
    sonda = iniciar_sonda(60)
    time.sleep(3)
    kubectl("set", "image", "deployment/integrador", f"integrador={IMAGEM_QUEBRADA}")
    travou = subprocess.run(["kubectl", "--context", CONTEXTO, "-n", NS, "rollout", "status",
                             "deployment/integrador", "--timeout=25s"], capture_output=True, env=AMBIENTE,
                            timeout=60).returncode != 0
    motivos = kubectl("get", "pods", "-l", "app.kubernetes.io/name=integrador", "-o",
                      "jsonpath={range .items[*]}{.status.containerStatuses[0].state.waiting.reason}{' '}{end}")
    prontos = int(kubectl("get", "deployment/integrador", "-o", "jsonpath={.status.readyReplicas}") or 0)
    kubectl("rollout", "undo", "deployment/integrador")
    kubectl("rollout", "status", "deployment/integrador", "--timeout=180s", timeout=200)
    ok, falha = resultado_sonda(sonda)
    checar(verif, "rollout_quebrado_e_rollback",
           travou and prontos == 2 and falha == 0 and imagem_integrador() == IMAGEM_V2,
           rollout_travou=travou, replicas_prontas_durante=prontos,
           motivos_espera=sorted(set(motivos.split())), sonda_ok=ok, sonda_falha=falha)
    historico = kubectl("rollout", "history", "deployment/integrador").strip().splitlines()

    versoes = {
        "kind": rodar(["kind", "version"]).strip(),
        "kubectl_cliente": json.loads(rodar(["kubectl", "version", "--client", "-o", "json"]))["clientVersion"]["gitVersion"],
        "servidor": json.loads(rodar(["kubectl", "--context", CONTEXTO, "version", "-o", "json"]))["serverVersion"]["gitVersion"],
        "podman": rodar(["podman", "--version"]).strip(),
    }
    aprovado = all(v["ok"] for v in verif)
    caminho = mercado_base.registrar_execucao("k8s-local", {
        "cluster": CLUSTER, "namespace": NS, "versoes": versoes, "pods": resumo_pods,
        "verificacoes": verif, "historico_rollout_integrador": historico, "aprovado": aprovado,
        "limites": ["LLM e embeddings do host (Ollama em 127.0.0.1) não são alcançáveis do kind rootless; "
                    "o caminho real de resposta é validado fora do cluster (Etapa 2)."],
    })
    print(("APROVADO" if aprovado else "REPROVADO") + f" — registro em {os.path.relpath(caminho)}")
    return caminho if aprovado else ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("acao", choices=("subir", "validar", "remover"))
    args = ap.parse_args()
    exigir_ferramentas()
    if args.acao == "remover":
        if cluster_existe():
            rodar(["kind", "delete", "cluster", "--name", CLUSTER], timeout=300)
        print(f"cluster {CLUSTER} removido (imagens locais do Podman preservadas)")
        return 0
    if not cluster_existe() and args.acao == "validar":
        raise SystemExit("cluster ausente: rode `subir` antes")
    if args.acao == "subir":
        subir()
        return 0
    return 0 if validar() else 1


if __name__ == "__main__":
    sys.exit(main())
