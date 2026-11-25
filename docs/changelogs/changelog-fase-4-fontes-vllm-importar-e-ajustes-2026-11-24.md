# Changelog: Fontes da vLLM no GitHub, comando `importar`, exceção de consulta manual e ajustes leves — 24/11/2026

Consolida a estratégia definida pelo operador para as fontes fora do cache e aplica os ajustes leves abertos no guia HTML/PDF, mantendo a Fase 4 pronta para a etapa de validação manual em telas (`L2`) e etapa final. Ver [roadmap.md](../../roadmap.md).

## Autoria

- **24/11/2026, `agy - ap` (Gemini 4 Hydrogen High):** migração das `7` chaves da vLLM para a documentação Markdown oficial no GitHub, criação do subcomando `importar` em [ferramentas/fontes.py](../../ferramentas/fontes.py), registro da decisão do operador para as `18` chaves bloqueadas (`13` URLs), aplicação das duas correções leves em [guia-engenharia-llms.html](../../guia-engenharia-llms.html) e regeração do PDF provisório.

## O que mudou

- **Fontes da vLLM (`pacote-de-fontes-capitulo-13-inferencia-local-2026-11-17.md`):**
  - As `7` chaves `vllm-*` (`vllm-quantization`, `vllm-awq`, `vllm-gptqmodel`, `vllm-fp8`, `vllm-int4`, `vllm-kvcache`, `vllm-speculative_decoding`), antes bloqueadas com `HTTP 403` em `docs.vllm.ai`, foram apontadas no manifesto para os respectivos arquivos Markdown oficiais em `raw.githubusercontent.com/vllm-project/vllm/main/docs/features/...`, com hashes brutos atualizados e grafia literal ajustada em `IL-45`, `IL-46`, `IL-58` e `IL-60`.
  - Baixadas, extraídas e aprovadas em `fontes.py conferir`: `81` aprovados, `0` reprovados no pacote do Capítulo 13.
- **Importação manual assistida (`ferramentas/fontes.py`, `ferramentas/testar-fontes.py`):**
  - Adicionado o subcomando `importar` (`--pasta`, padrão `cache-fontes/manuais`), que lê cópias salvas pelo navegador, propaga automaticamente para chaves que compartilham a mesma URL no manifesto, registra em `cache-fontes/indice.json` (`"origem": "manual"`) e executa `extrair`.
  - Adicionados `2` testes determinísticos em `ferramentas/testar-fontes.py` (`Importacao`), passando com `14` testes OK e sem `ResourceWarning`.
- **Exceção de consulta manual (`18` chaves / `13` URLs):**
  - Por decisão do operador (sem contorno de bloqueio `HTTP 403`/`400` ou redirecionamento `http://`, e sem cópia oficial aberta alternativa encontrada para `azure-trace` ou os PDFs do NIST), permanecem registradas como referência de consulta manual fora do cache: `9` URLs da Anthropic (`14` chaves: `anthropic-agents`, `anthropic-building-agents`, `anthropic-building-effective-agents`, `bea`, `anthropic-code-mcp`, `anthropic-context`, `anthropic-context-eng`, `anthropic-contextual-retrieval`, `anthropic-effective-harnesses`, `anthropic-harnesses`, `anthropic-evals-agents`, `anthropic-multiagent`, `anthropic-sandboxing`, `anthropic-writing-tools`), `2` do NIST (`nist-ai-100-1`, `nist-ai-600-1`), `azure-trace` e `cormack-rrf`. Caso o operador salve essas páginas futuramente em `cache-fontes/manuais/`, `fontes.py importar` automatiza a integração.
- **Ajustes leves no guia (`guia-engenharia-llms.html`, sha256 `bb1ff5a2a4db25f3` → `7be9d212a6cb82e8`):**
  - Corrigidos os rótulos de `1.4a`, `1.4b` e `1.4c` de `(parte X de 4)` para `(parte X de 5)`.
  - Adicionada guarda em `ngramas` dentro de `jaccard` (`6.5b`, `cod-6-5-py`) para textos com menos de `n` palavras (`if len(p) < n: return {tuple(p)} if p else set()`), evitando falso `1.0` entre textos curtos distintos.
- **PDF provisório (`guia-engenharia-llms.pdf`):**
  - Regerado com `654` páginas A4 (`15.745.482` bytes, sha256 `8f4a584ed20fe8e1`); cópia anterior preservada em `arquivo/antes-fase-4-fontes-e-ajustes-2026-11-24/`.

## Validações (após a última edição)

- `python3 -I ferramentas/guia.py fechar`: `0` falhas (`377` partes, `219.241` palavras em partes, `445` questões, `149` tabelas com `.rolagem`, `501` termos no Glossário, `26` blocos Python executáveis OK e `21` ilustrativos).
- `python3 -I ferramentas/testar-ferramentas.py`: `15` testes OK (`654` páginas conferidas no PDF).
- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py`: `14` testes OK.
- `python3 -I ferramentas/testar-livros.py`: `2` testes OK.
- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `82` testes OK.
- `python3 -I ferramentas/fontes.py vigencia`: `196` chaves únicas | `178` atuais | `18` fora do cache (consulta manual registrada) | `0` vencidas | `0` hash divergente.
- `auditar-guia-navegador.mjs`: `377` seções sem estouro a `320 px`, `445/445` questões OK, `axe-core` com `0` violações em `1280×800` e `320×640`.

Assinatura: agy - ap (24/11/2026).
