"""Embeddings e armazéns vetoriais do projeto 02 (pgvector real + memória para testes).

- `EmbedderHash`: embeddings determinísticos por *feature hashing* (só para testes offline;
  não captura sinônimos).
- `EmbedderOpenAICompativel`: `POST /v1/embeddings` (llama-server, Ollama, vLLM, OpenAI).
- `ArmazemPgvector`: PostgreSQL + extensão `vector`, índice HNSW por cosseno e busca lexical
  com `tsvector` em português (híbrida, fundida por RRF no `rag_pipeline`).
- `ArmazemMemoria`: mesma interface, em memória, para smoke-tests.
"""
from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from typing import Callable, Dict, List, Optional, Sequence

import httpx

from rag_ingestao import Trecho

PALAVRAS_VAZIAS = frozenset(
    "a o as os de da do das dos e em no na nos nas um uma para por com que se ao à é ou "
    "qual quais como quando onde quanto custa sobre ser são há".split()
)


def normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sem_acento.lower()


def termos(texto: str) -> List[str]:
    return [t for t in re.findall(r"[a-z0-9]+(?:,[0-9]+)?", normalizar(texto)) if t not in PALAVRAS_VAZIAS]


def _normalizar_vetor(v: List[float]) -> List[float]:
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def cosseno(a: Sequence[float], b: Sequence[float]) -> float:
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(x * x for x in b)) or 1.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


class EmbedderHash:
    """Feature hashing com sinal; determinístico entre execuções e máquinas."""

    def __init__(self, dim: int = 256):
        self.dim = dim
        self.nome = f"hash-{dim}"

    def embutir(self, textos: Sequence[str]) -> List[List[float]]:
        saida = []
        for texto in textos:
            v = [0.0] * self.dim
            for t in termos(texto):
                h = hashlib.sha256(t.encode("utf-8")).digest()
                idx = int.from_bytes(h[:4], "big") % self.dim
                v[idx] += 1.0 if h[4] % 2 == 0 else -1.0
            saida.append(_normalizar_vetor(v))
        return saida


class EmbedderOpenAICompativel:
    """Cliente de `/v1/embeddings` com lotes e validação de dimensão."""

    def __init__(self, base_url: str, modelo: str, *, api_key: str = "", lote: int = 16,
                 transport: Optional[httpx.BaseTransport] = None, timeout_s: float = 60.0):
        self.base_url = base_url.rstrip("/")
        self.modelo = modelo
        self.nome = modelo
        self.lote = lote
        self._cabecalhos = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self._transport = transport
        self._timeout = timeout_s
        self.dim: Optional[int] = None

    def embutir(self, textos: Sequence[str]) -> List[List[float]]:
        vetores: List[List[float]] = []
        with httpx.Client(transport=self._transport, timeout=self._timeout) as c:
            for i in range(0, len(textos), self.lote):
                lote = list(textos[i:i + self.lote])
                r = c.post(f"{self.base_url}/embeddings", json={"model": self.modelo, "input": lote},
                           headers=self._cabecalhos)
                r.raise_for_status()
                dados = sorted(r.json()["data"], key=lambda d: d["index"])
                if len(dados) != len(lote):
                    raise ValueError("resposta de embeddings com tamanho diferente do lote")
                vetores.extend(_normalizar_vetor([float(x) for x in d["embedding"]]) for d in dados)
        dims = {len(v) for v in vetores}
        if len(dims) > 1:
            raise ValueError(f"dimensões inconsistentes: {sorted(dims)}")
        self.dim = dims.pop() if dims else self.dim
        return vetores


class ArmazemMemoria:
    """Armazém em memória com busca vetorial (cosseno) e lexical (BM25 simplificado)."""

    def __init__(self):
        self.itens: Dict[str, tuple] = {}

    def criar_esquema(self, dim: int, recriar: bool = False) -> None:
        self.dim = dim
        if recriar:
            self.itens.clear()

    def inserir(self, trechos: Sequence[Trecho], vetores: Sequence[Sequence[float]]) -> int:
        for t, v in zip(trechos, vetores, strict=True):
            self.itens[t.id] = (t, list(v))
        return len(trechos)

    def buscar_vetorial(self, vetor: Sequence[float], k: int) -> List[tuple]:
        pont = [(t, cosseno(vetor, v)) for t, v in self.itens.values()]
        return sorted(pont, key=lambda x: (-x[1], x[0].id))[:k]

    def buscar_lexical(self, consulta: str, k: int) -> List[tuple]:
        q = set(termos(consulta))
        if not q:
            return []
        docs = [(t, termos(t.texto)) for t, _ in self.itens.values()]
        n = len(docs)
        media = sum(len(d) for _, d in docs) / max(n, 1)
        df = {w: sum(1 for _, d in docs if w in d) for w in q}
        pont = []
        for t, d in docs:
            s = 0.0
            for w in q:
                f = d.count(w)
                if f:
                    idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
                    s += idf * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * len(d) / max(media, 1)))
            if s > 0:
                pont.append((t, s))
        return sorted(pont, key=lambda x: (-x[1], x[0].id))[:k]


def literal_vetor(v: Sequence[float]) -> str:
    """Formato textual aceito por `::vector` no pgvector."""
    return "[" + ",".join(f"{x:.7g}" for x in v) + "]"


class ArmazemPgvector:
    """PostgreSQL + pgvector. `conectar` é injetável (testes usam conexão falsa)."""

    TABELA = "rag_trechos"

    def __init__(self, dsn: str = "", conectar: Optional[Callable[[], object]] = None):
        if conectar is None:
            import psycopg  # import tardio: só o caminho real exige o driver

            def conectar():
                return psycopg.connect(dsn, autocommit=True)
        self._conectar = conectar

    def criar_esquema(self, dim: int, recriar: bool = False) -> None:
        if not isinstance(dim, int) or not 1 <= dim <= 16000:
            raise ValueError("dimensão inválida")
        comandos = ["CREATE EXTENSION IF NOT EXISTS vector"]
        if recriar:
            comandos.append(f"DROP TABLE IF EXISTS {self.TABELA}")
        comandos += [
            f"CREATE TABLE IF NOT EXISTS {self.TABELA} (id text PRIMARY KEY, doc text NOT NULL, "
            f"pagina int NOT NULL, tipo text NOT NULL, texto text NOT NULL, texto_busca text NOT NULL, "
            f"embedding vector({dim}) NOT NULL, "
            "lexico tsvector GENERATED ALWAYS AS (to_tsvector('portuguese', texto_busca)) STORED)",
            f"CREATE INDEX IF NOT EXISTS {self.TABELA}_hnsw ON {self.TABELA} USING hnsw (embedding vector_cosine_ops)",
            f"CREATE INDEX IF NOT EXISTS {self.TABELA}_lexico ON {self.TABELA} USING gin (lexico)",
        ]
        with self._conectar() as con, con.cursor() as cur:
            for sql in comandos:
                cur.execute(sql)

    def inserir(self, trechos: Sequence[Trecho], vetores: Sequence[Sequence[float]]) -> int:
        sql = (
            f"INSERT INTO {self.TABELA} (id, doc, pagina, tipo, texto, texto_busca, embedding) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s::vector) ON CONFLICT (id) DO UPDATE SET "
            "doc = EXCLUDED.doc, pagina = EXCLUDED.pagina, tipo = EXCLUDED.tipo, texto = EXCLUDED.texto, "
            "texto_busca = EXCLUDED.texto_busca, embedding = EXCLUDED.embedding"
        )
        linhas = [(t.id, t.doc, t.pagina, t.tipo, t.texto, normalizar(t.texto), literal_vetor(v))
                  for t, v in zip(trechos, vetores, strict=True)]
        with self._conectar() as con, con.cursor() as cur:
            cur.executemany(sql, linhas)
        return len(linhas)

    @staticmethod
    def _trecho(linha) -> Trecho:
        return Trecho(id=linha[0], doc=linha[1], pagina=int(linha[2]), tipo=linha[3], texto=linha[4])

    def buscar_vetorial(self, vetor: Sequence[float], k: int) -> List[tuple]:
        lit = literal_vetor(vetor)
        sql = (
            f"SELECT id, doc, pagina, tipo, texto, 1 - (embedding <=> %s::vector) AS similaridade "
            f"FROM {self.TABELA} ORDER BY embedding <=> %s::vector, id LIMIT %s"
        )
        with self._conectar() as con, con.cursor() as cur:
            cur.execute(sql, (lit, lit, int(k)))
            return [(self._trecho(l), float(l[5])) for l in cur.fetchall()]

    def buscar_lexical(self, consulta: str, k: int) -> List[tuple]:
        # Termos já normalizados ([a-z0-9,]), unidos por OU: sem sintaxe de tsquery vinda do usuário.
        q = " | ".join(t.replace(",", "") for t in termos(consulta))
        if not q:
            return []
        sql = (
            "SELECT id, doc, pagina, tipo, texto, ts_rank(lexico, q) AS pontuacao "
            f"FROM {self.TABELA}, to_tsquery('portuguese', %s) q "
            "WHERE lexico @@ q ORDER BY pontuacao DESC, id LIMIT %s"
        )
        with self._conectar() as con, con.cursor() as cur:
            cur.execute(sql, (q, int(k)))
            return [(self._trecho(l), float(l[5])) for l in cur.fetchall()]
