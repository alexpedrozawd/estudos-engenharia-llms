"""Registro de ferramentas e servidor JSON-RPC mínimo no estilo MCP (Cap. 10).

Didático e local: não implementa o protocolo MCP completo (transporte,
inicialização, capacidades). Reproduz o essencial para o capítulo: listar
ferramentas com `inputSchema`, chamar com validação estrita, devolver erros
legíveis ao modelo, exigir aprovação para escrita e não repetir efeitos com a
mesma chave de idempotência.
"""
import json
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

TIPOS_JSON = {str: "string", int: "integer", bool: "boolean", float: "number"}


@dataclass
class Ferramenta:
    nome: str
    descricao: str
    parametros: Dict[str, type]
    fn: Callable[..., object]
    escrita: bool = False

    def schema(self) -> Dict[str, object]:
        # EXERCICIO-INICIO: JSON Schema de objeto: tipo JSON de cada parâmetro, todos obrigatórios (ordenados) e additionalProperties false.
        return {"type": "object",
                "properties": {k: {"type": TIPOS_JSON[t]} for k, t in self.parametros.items()},
                "required": sorted(self.parametros), "additionalProperties": False}
        # EXERCICIO-FIM


@dataclass
class Registro:
    ferramentas: Dict[str, Ferramenta] = field(default_factory=dict)
    efeitos: Dict[str, object] = field(default_factory=dict)
    auditoria: List[Dict[str, object]] = field(default_factory=list)

    def registrar(self, f: Ferramenta) -> None:
        if f.nome in self.ferramentas:
            raise ValueError(f"ferramenta duplicada: {f.nome}")
        self.ferramentas[f.nome] = f

    def listar(self) -> List[Dict[str, object]]:
        return [{"name": f.nome, "description": f.descricao, "inputSchema": f.schema()}
                for f in sorted(self.ferramentas.values(), key=lambda x: x.nome)]

    def chamar(self, nome: str, argumentos: Dict[str, object], aprovado: bool = False,
               chave_idempotencia: Optional[str] = None) -> Dict[str, object]:
        # EXERCICIO-INICIO: recuse ferramenta inexistente, argumentos fora do schema e tipos errados; registre auditoria; erro volta como isError, não como exceção.
        def erro(msg: str) -> Dict[str, object]:
            self.auditoria.append({"ferramenta": nome, "resultado": "erro", "detalhe": msg})
            return {"content": [{"type": "text", "text": msg}], "isError": True}

        f = self.ferramentas.get(nome)
        if f is None:
            return erro(f"ferramenta inexistente: {nome}")
        if not isinstance(argumentos, dict):
            return erro("argumentos devem ser um objeto")
        extras = sorted(set(argumentos) - set(f.parametros))
        faltam = sorted(set(f.parametros) - set(argumentos))
        if extras or faltam:
            return erro(f"argumentos inválidos; extras={extras} faltam={faltam}")
        for campo, tipo in f.parametros.items():
            if type(argumentos[campo]) is not tipo:
                return erro(f"{campo} deve ser {TIPOS_JSON[tipo]}")
        if f.escrita and not aprovado:
            return erro("ação de escrita pendente de aprovação humana")
        if f.escrita:
            if not chave_idempotencia:
                return erro("ação de escrita exige chave de idempotência")
            if chave_idempotencia in self.efeitos:
                return {"content": [{"type": "text", "text": str(self.efeitos[chave_idempotencia])}], "isError": False}
        saida = f.fn(**argumentos)
        if f.escrita:
            self.efeitos[chave_idempotencia] = saida
        self.auditoria.append({"ferramenta": nome, "resultado": "ok"})
        return {"content": [{"type": "text", "text": str(saida)}], "isError": False}
        # EXERCICIO-FIM


def servidor(registro: Registro, mensagem: str) -> str:
    """Trata uma mensagem JSON-RPC 2.0 com os métodos tools/list e tools/call."""
    try:
        req = json.loads(mensagem)
    except json.JSONDecodeError:
        return json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}})
    rid, metodo, params = req.get("id"), req.get("method"), req.get("params") or {}
    if metodo == "tools/list":
        resultado = {"tools": registro.listar()}
    elif metodo == "tools/call":
        meta = params.get("_meta") or {}
        resultado = registro.chamar(params.get("name", ""), params.get("arguments", {}),
                                    aprovado=bool(meta.get("aprovado")), chave_idempotencia=meta.get("chave"))
    else:
        return json.dumps({"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "method not found"}})
    return json.dumps({"jsonrpc": "2.0", "id": rid, "result": resultado}, ensure_ascii=False, sort_keys=True)


def registro_aurora() -> Registro:
    contador = {"n": 0}

    def abrir(assunto: str, prioridade: int) -> str:
        contador["n"] += 1
        return f"CH-{contador['n']:04d} ({assunto}, p{prioridade})"

    r = Registro()
    r.registrar(Ferramenta("consultar_prazo", "Prazo em dias de uma política da Aurora.", {"politica": str},
                           lambda politica: {"POL-01": 7}.get(politica, "desconhecida")))
    r.registrar(Ferramenta("abrir_chamado", "Abre chamado de suporte (escrita).", {"assunto": str, "prioridade": int},
                           abrir, escrita=True))
    return r
