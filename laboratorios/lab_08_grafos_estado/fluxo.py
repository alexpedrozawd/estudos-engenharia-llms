"""Máquina de estados de reembolso com checkpoint em SQLite (Cap. 8).

Cada nó é uma função pura sobre o estado; após cada nó o próximo passo é gravado.
Efeitos externos usam chave de idempotência, então a retomada após falha não
duplica o pagamento. Inclui um modelo simples de custo com e sem subagentes.
"""
import json
import sqlite3
from typing import Callable, Dict, List, Optional


class FalhaSimulada(RuntimeError):
    pass


class FluxoReembolso:
    LIMITE_APROVACAO = 500

    def __init__(self, caminho: str = ":memory:", falhar_em: Optional[str] = None):
        self.db = sqlite3.connect(caminho)
        self.db.execute("CREATE TABLE IF NOT EXISTS checkpoint (fluxo TEXT PRIMARY KEY, no TEXT, estado TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS efeitos (chave TEXT PRIMARY KEY, valor INTEGER)")
        self.falhar_em = falhar_em
        self.visitas: List[str] = []
        self.nos: Dict[str, Callable[[Dict], str]] = {
            "ler_pedido": self._ler,
            "conferir_regras": self._conferir,
            "aguardar_aprovacao": self._aguardar,
            "gravar_pagamento": self._gravar,
            "recusar": lambda e: "fim",
        }

    def fechar(self) -> None:
        self.db.close()

    # --- nós
    def _ler(self, e: Dict) -> str:
        e["valor"] = int(e["valor"])
        return "conferir_regras"

    def _conferir(self, e: Dict) -> str:
        if e["dias_desde_matricula"] > 7:
            e["motivo"] = "fora do prazo de 7 dias (POL-01)"
            return "recusar"
        return "aguardar_aprovacao" if e["valor"] > self.LIMITE_APROVACAO else "gravar_pagamento"

    def _aguardar(self, e: Dict) -> str:
        return "gravar_pagamento" if e.get("aprovado") else "PAUSA"

    def _gravar(self, e: Dict) -> str:
        self.db.execute("INSERT OR IGNORE INTO efeitos VALUES (?, ?)", (e["chave"], e["valor"]))
        if self.falhar_em == "apos_gravar":
            self.falhar_em = None
            raise FalhaSimulada("queda depois do efeito e antes do checkpoint")
        return "fim"

    # --- motor
    def _salvar(self, fluxo: str, no: str, estado: Dict) -> None:
        self.db.execute("INSERT OR REPLACE INTO checkpoint VALUES (?, ?, ?)", (fluxo, no, json.dumps(estado, sort_keys=True)))

    def executar(self, fluxo: str, pedido: Optional[Dict] = None, aprovado: bool = False) -> Dict[str, object]:
        linha = self.db.execute("SELECT no, estado FROM checkpoint WHERE fluxo = ?", (fluxo,)).fetchone()
        if linha:
            no, estado = linha[0], json.loads(linha[1])
        else:
            no, estado = "ler_pedido", dict(pedido or {})
        if aprovado:
            estado["aprovado"] = True
        while no != "fim":
            self.visitas.append(no)
            proximo = self.nos[no](estado)
            if proximo == "PAUSA":
                self._salvar(fluxo, no, estado)
                return {"status": "pausado", "no": no}
            no = proximo
            self._salvar(fluxo, no, estado)
        return {"status": "concluido", "motivo": estado.get("motivo", "ok")}

    def pagamentos(self) -> List[tuple]:
        return self.db.execute("SELECT chave, valor FROM efeitos ORDER BY chave").fetchall()


def custo_tokens(subtarefas: int, contexto_base: int, por_subtarefa: int, resumo: int, com_subagentes: bool) -> int:
    """Modelo didático: sem subagentes, cada subtarefa relê o contexto acumulado;
    com subagentes, cada uma parte do contexto base e devolve só um resumo."""
    if com_subagentes:
        return subtarefas * (contexto_base + por_subtarefa) + contexto_base + subtarefas * resumo
    total, acumulado = 0, contexto_base
    for _ in range(subtarefas):
        total += acumulado + por_subtarefa
        acumulado += por_subtarefa
    return total
