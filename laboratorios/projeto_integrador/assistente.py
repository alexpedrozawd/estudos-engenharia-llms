"""Projeto integrador: esqueleto do assistente acadêmico da Aurora Educação (Cap. 18, estudo de caso final).

Reúne peças dos laboratórios, cada uma com a decisão do capítulo de origem:
- guardrails de entrada/saída e máscara de dados pessoais (lab 12, Cap. 12);
- RAG híbrido com citação conferida contra o recuperado (lab 07, Cap. 7);
- ferramenta de escrita com aprovação e idempotência (lab 10, Cap. 10);
- roteamento pelo risco com contingência e conversa estável (lab 16, Cap. 16);
- rastros com atributos GenAI (lab 17, Cap. 17);
- custo por sessão e orçamento mensal (lab 18, Cap. 18);
- portão de versão por intervalo de Wilson num conjunto versionado (lab 05, Caps. 5 e 6).

Tudo offline com clientes simulados; para produção, troque os clientes por
adaptadores reais e mantenha estes testes como regressão do contrato.
"""
import itertools
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from comum.cliente_llm import ClienteMockDeterministico
from lab_05_avaliacao.pipeline_avaliacao import intervalo_wilson
from lab_07_rag_hibrido.rag import buscar_hibrido, carregar_documentos
from lab_10_ferramentas_mcp.registro import registro_aurora
from lab_12_guardrails.guardrails import desmascarar, guardrail_entrada, guardrail_saida, mascarar
from lab_16_roteamento.gateway import Gateway
from lab_17_llmops.operacao import Rastreador
from lab_18_economia.custos import orcamento_mensal

SISTEMA = "Assistente acadêmico da Aurora. Responda só com base nos trechos e cite-os entre colchetes."
SINAIS_RISCO_ALTO = ("contestar", "recurso", "cancelar minha matrícula", "excluir meus dados")


def classificar(pergunta: str) -> Dict[str, object]:
    baixo = pergunta.lower()
    risco = "alto" if any(s in baixo for s in SINAIS_RISCO_ALTO) else "baixo"
    return {"risco": risco, "passos": 4 if " e " in baixo and "?" in baixo else 1}


def respostas_simuladas() -> Dict[str, str]:
    """Roteiro do modelo simulado: a chave é um trecho do prompt; o valor, a resposta."""
    return {
        "reembolso": "O cancelamento integral vale até 7 dias corridos após a matrícula [POL-01]. Confirmo para [EMAIL_1].",
        "monitoria": "O tutor explica passo a passo e cita a aula, sem entregar gabaritos [POL-03].",
        "contestar": "Encaminhei seu pedido de revisão à coordenação [POL-09].",
    }


class ModeloSimulado(ClienteMockDeterministico):
    """Casa o roteiro só com a linha da pergunta, para os trechos recuperados não dispararem respostas erradas."""

    def completar(self, prompt: str, **kwargs):
        linha = next((l for l in prompt.splitlines() if l.startswith("Pergunta:")), prompt)
        resp = super().completar(linha, **kwargs)
        self.chamadas[-1]["prompt"] = prompt
        return resp


def gateway_integrador() -> Gateway:
    roteiro = respostas_simuladas()
    return Gateway(modelos={"rapido": ModeloSimulado(roteiro, fallback="Não encontrei nos trechos.", modelo="local-rapido"),
                            "fronteira": ModeloSimulado(roteiro, fallback="Não encontrei nos trechos.", modelo="fronteira")},
                   custos={"rapido": 1.0, "fronteira": 12.0})


@dataclass
class Assistente:
    gateway: Gateway = field(default_factory=gateway_integrador)
    docs: Dict[str, str] = field(default_factory=carregar_documentos)
    rastreador: Rastreador = field(default_factory=lambda: Rastreador(relogio=itertools.count(0.0, 0.01).__next__))
    ferramentas: object = field(default_factory=registro_aurora)
    custo_acumulado: float = 0.0
    atendimentos: int = 0

    def responder(self, conversa: str, pergunta: str) -> Dict[str, object]:
        trace = f"{conversa}-{self.atendimentos + 1}"
        self.atendimentos += 1
        with self.rastreador.span("atender", trace) as raiz:
            ok, motivo = guardrail_entrada(pergunta)
            if not ok:
                raiz["attributes"]["aurora.resultado"] = "bloqueado_entrada"
                return {"status": "bloqueado", "motivo": motivo, "texto": "Não posso ajudar com isso por aqui."}
            seguro, reverso = mascarar(pergunta)
            with self.rastreador.span("recuperar", trace) as s:
                ids = buscar_hibrido(seguro, self.docs, top=2)
                s["attributes"]["aurora.recuperados"] = ",".join(ids)
            contexto = "\n".join(f"[{d}] {self.docs[d]}" for d in ids)
            pedido = {"texto": f"{SISTEMA}\nPergunta: {seguro}\nTrechos:\n{contexto}", **classificar(pergunta)}
            with self.rastreador.span("chat", trace, **{"gen_ai.operation.name": "chat"}) as s:
                r = self.gateway.atender(conversa, pedido)
                s["attributes"]["gen_ai.request.model"] = r["destino"]
            self.custo_acumulado += r["custo"]
            if r["destino"] == "fila_humana":
                raiz["attributes"]["aurora.resultado"] = "fila_humana"
                return {"status": "fila_humana", "texto": "Um atendente vai responder.", "destino": r["destino"]}
            texto = r["texto"] or ""
            citados = re.findall(r"\[(POL-\d+)\]", texto)
            if not citados or not set(citados) <= set(ids):
                raiz["attributes"]["aurora.resultado"] = "sem_fonte"
                return {"status": "sem_fonte", "texto": "Não encontrei base nas políticas; encaminhei a um atendente.",
                        "destino": r["destino"]}
            ok, motivo = guardrail_saida(texto, [SISTEMA])
            if not ok:
                raiz["attributes"]["aurora.resultado"] = "retido_saida"
                return {"status": "retido", "motivo": motivo, "texto": "Resposta retida para revisão.", "destino": r["destino"]}
            raiz["attributes"]["aurora.resultado"] = "respondido"
            return {"status": "respondido", "texto": desmascarar(texto, reverso), "citados": citados,
                    "destino": r["destino"], "enviado_ao_modelo": seguro}

    def abrir_chamado(self, assunto: str, aprovado: bool, chave: Optional[str]) -> Dict[str, object]:
        """Escrita só com aprovação humana e chave de idempotência (repetir não duplica)."""
        return self.ferramentas.chamar("abrir_chamado", {"assunto": assunto, "prioridade": 2},
                                       aprovado=aprovado, chave_idempotencia=chave)

    def custo_medio(self) -> float:
        return self.custo_acumulado / self.atendimentos if self.atendimentos else 0.0


def conjunto_avaliacao() -> List[Dict[str, str]]:
    """Conjunto versionado e pequeno (proposta didática): pergunta e política que deve ser citada."""
    return [
        {"id": "AV-01", "pergunta": "Qual o prazo de reembolso? Meu e-mail é ana@exemplo.com.", "esperado": "POL-01"},
        {"id": "AV-02", "pergunta": "Como funciona a monitoria por IA no curso?", "esperado": "POL-03"},
        {"id": "AV-03", "pergunta": "Até quando posso pedir reembolso da matrícula?", "esperado": "POL-01"},
        {"id": "AV-04", "pergunta": "A monitoria do curso entrega gabarito?", "esperado": "POL-03"},
    ]


def avaliar_versao(assistente: Assistente, casos: Sequence[Dict[str, str]], limiar_inferior: float) -> Dict[str, object]:
    """Libera a versão só se o limite inferior de Wilson do acerto passar do limiar."""
    acertos = 0
    for c in casos:
        r = assistente.responder(f"aval-{c['id']}", c["pergunta"])
        acertos += int(r["status"] == "respondido" and c["esperado"] in r.get("citados", []))
    inf, sup = intervalo_wilson(acertos, len(casos))
    return {"acertos": acertos, "total": len(casos), "wilson": (round(inf, 3), round(sup, 3)),
            "liberar": inf >= limiar_inferior}


def relatorio_custo(assistente: Assistente, sessoes_dia: int, tokens_por_unidade: float, preco_por_milhao: float,
                    limite_mensal: float) -> Dict[str, object]:
    """Projeta o mês a partir do custo médio observado (unidades do gateway convertidas em tokens)."""
    mensal = orcamento_mensal(sessoes_dia, assistente.custo_medio() * tokens_por_unidade, preco_por_milhao)
    return {"custo_medio_unidades": round(assistente.custo_medio(), 2), "mensal": mensal,
            "dentro_do_orcamento": mensal <= limite_mensal}


def exportar_rastros(assistente: Assistente) -> str:
    return "\n".join(json.dumps(s, ensure_ascii=False, sort_keys=True) for s in assistente.rastreador.spans)
