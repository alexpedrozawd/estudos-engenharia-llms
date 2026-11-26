"""Smoke-tests offline dos manifests Kubernetes (Etapa 6a): sem cluster, sem rede.

Conferem o que o `executar_k8s_local.py validar` exercita no kind, para o CI pegar regressões nos YAML:
probes, limites, contexto de segurança, segredos fora do Git, Services ligados aos pods e rollout seguro.
"""
import importlib
import os
import sys
import unittest

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
MANIFESTS = os.path.join(AQUI, "manifests")
sys.path.insert(0, AQUI)
import executar_k8s_local as ek  # noqa: E402
from mercado_base.seguranca_http import carregar_seguranca_de_ambiente  # noqa: E402

PALAVRAS_SECRETAS = ("SENHA", "PASSWORD", "KEY", "CHAVE", "DSN", "TOKEN", "SECRET")


def carregar_documentos():
    with open(os.path.join(MANIFESTS, "kustomization.yaml"), encoding="utf-8") as f:
        kust = yaml.safe_load(f)
    docs = []
    for nome in kust["resources"]:
        with open(os.path.join(MANIFESTS, nome), encoding="utf-8") as f:
            docs += [d for d in yaml.safe_load_all(f) if d]
    return kust, docs


class TestManifestsK8s(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kust, cls.docs = carregar_documentos()
        cls.cargas = [d for d in cls.docs if d["kind"] in ("Deployment", "StatefulSet")]

    def por_tipo(self, tipo):
        return [d for d in self.docs if d["kind"] == tipo]

    def test_kustomization_lista_todos_os_yaml_e_nenhum_secret(self):
        arquivos = sorted(f for f in os.listdir(MANIFESTS) if f.endswith(".yaml") and f != "kustomization.yaml")
        self.assertEqual(sorted(self.kust["resources"]), arquivos)
        self.assertEqual(self.kust["namespace"], ek.NS)
        self.assertEqual(self.por_tipo("Secret"), [], "Secret é gerado pelo script, nunca versionado")
        self.assertEqual({d["metadata"]["name"] for d in self.cargas}, {"postgres", "api-llmops", "integrador"})

    def test_namespace_restricted(self):
        (ns,) = self.por_tipo("Namespace")
        self.assertEqual(ns["metadata"]["labels"]["pod-security.kubernetes.io/enforce"], "restricted")

    def test_seguranca_probes_e_limites_em_todo_container(self):
        for carga in self.cargas:
            spec = carga["spec"]["template"]["spec"]
            with self.subTest(carga=carga["metadata"]["name"]):
                self.assertIs(spec["automountServiceAccountToken"], False)
                self.assertIs(spec["securityContext"]["runAsNonRoot"], True)
                self.assertEqual(spec["securityContext"]["seccompProfile"]["type"], "RuntimeDefault")
                for c in spec["containers"]:
                    self.assertIs(c["securityContext"]["allowPrivilegeEscalation"], False)
                    self.assertEqual(c["securityContext"]["capabilities"]["drop"], ["ALL"])
                    self.assertIn("readinessProbe", c)
                    self.assertIn("livenessProbe", c)
                    for tipo in ("requests", "limits"):
                        self.assertTrue({"cpu", "memory"} <= set(c["resources"][tipo]))

    def test_deployments_com_rollout_sem_indisponibilidade(self):
        for dep in self.por_tipo("Deployment"):
            with self.subTest(dep=dep["metadata"]["name"]):
                self.assertGreaterEqual(dep["spec"]["replicas"], 2)
                self.assertEqual(dep["spec"]["strategy"]["rollingUpdate"]["maxUnavailable"], 0)
                (c,) = dep["spec"]["template"]["spec"]["containers"]
                self.assertGreater(c["lifecycle"]["preStop"]["sleep"]["seconds"], 0)
                self.assertIs(c["securityContext"]["readOnlyRootFilesystem"], True)
                self.assertIn({"name": "tmp", "mountPath": "/tmp"}, c["volumeMounts"])
                self.assertEqual(c["image"], ek.IMAGEM_V1)
                self.assertEqual(c["imagePullPolicy"], "Never")

    def test_comando_aponta_para_fabrica_existente(self):
        for dep in self.por_tipo("Deployment"):
            (c,) = dep["spec"]["template"]["spec"]["containers"]
            modulo, fabrica = c["command"][c["command"].index("--factory") + 1].split(":")
            self.assertTrue(callable(getattr(importlib.import_module(modulo), fabrica)))
            porta = int(c["command"][c["command"].index("--port") + 1])
            self.assertEqual(c["ports"][0]["containerPort"], porta)

    def test_segredos_so_por_secretkeyref_e_chaves_geradas_pelo_script(self):
        gerado = ek.gerar_segredo()
        for carga in self.cargas:
            for c in carga["spec"]["template"]["spec"]["containers"]:
                for var in c.get("env", []):
                    if any(p in var["name"] for p in PALAVRAS_SECRETAS):
                        ref = var["valueFrom"]["secretKeyRef"]
                        self.assertEqual(ref["name"], "aurora-segredos")
                        self.assertIn(ref["key"], gerado)
        for cm in self.por_tipo("ConfigMap"):
            for nome in cm["data"]:
                self.assertFalse(any(p in nome for p in PALAVRAS_SECRETAS), nome)

    def test_services_selecionam_pods_e_portas_nomeadas(self):
        rotulos = {d["metadata"]["name"]: d["spec"]["template"]["metadata"]["labels"] for d in self.cargas}
        portas = {d["metadata"]["name"]: {p["name"] for c in d["spec"]["template"]["spec"]["containers"]
                                          for p in c["ports"]} for d in self.cargas}
        for svc in self.por_tipo("Service"):
            nome = svc["metadata"]["name"]
            with self.subTest(svc=nome):
                self.assertTrue(svc["spec"]["selector"].items() <= rotulos[nome].items())
                for p in svc["spec"]["ports"]:
                    self.assertIn(p["targetPort"], portas[nome])

    def test_networkpolicy_banco_so_do_integrador(self):
        (np,) = self.por_tipo("NetworkPolicy")
        self.assertEqual(np["spec"]["podSelector"]["matchLabels"], {"app.kubernetes.io/name": "postgres"})
        (regra,) = np["spec"]["ingress"]
        self.assertEqual(regra["from"], [{"podSelector": {"matchLabels": {"app.kubernetes.io/name": "integrador"}}}])
        self.assertEqual(regra["ports"], [{"protocol": "TCP", "port": 5432}])


class TestSegredoGerado(unittest.TestCase):
    def test_segredo_aleatorio_coerente_com_o_carregador_do_p06(self):
        a, b = ek.gerar_segredo(), ek.gerar_segredo()
        self.assertNotEqual(a, b)
        self.assertIn(f":{a['PG_SENHA']}@postgres:5432/rag", a["PGVECTOR_DSN"])
        ambiente = {"INTEGRADOR_PERFIS_CHAVES": a["INTEGRADOR_PERFIS_CHAVES"]}
        antigo = {k: os.environ.pop(k, None) for k in ("INTEGRADOR_PERFIS_CHAVES", "AURORA_PERFIS_CHAVES",
                                                       "INTEGRADOR_API_KEYS", "AURORA_API_KEYS")}
        try:
            os.environ.update(ambiente)
            seg = carregar_seguranca_de_ambiente("INTEGRADOR_")
        finally:
            os.environ.pop("INTEGRADOR_PERFIS_CHAVES", None)
            os.environ.update({k: v for k, v in antigo.items() if v is not None})
        self.assertEqual(sorted(seg["perfis_por_chave"].values()), ["admin", "aluno"])
        self.assertEqual(len(seg["api_keys"]), 2)


if __name__ == "__main__":
    unittest.main()
