# Changelog — Versão Final 1.0 e Revisão Adversarial Final (25/11/2026)

Data: 25/11/2026. Autoria: `agy - ap`.

## 1. Correções da revisão adversarial final

1. **Prevenção de elevação de privilégio no perfil RAG (anti-BFLA / OWASP API5):**
   - [`laboratorios-mercado/mercado_base/seguranca_http.py`](../../laboratorios-mercado/mercado_base/seguranca_http.py): adicionado suporte opcional a vínculo chave → perfil máximo (`perfis_por_chave` / `AURORA_PERFIS_CHAVES` no formato `chave:perfil`, propagando `request.state.perfil_maximo`).
   - [`laboratorios-mercado/06_integrador_producao/integrador_app.py`](../../laboratorios-mercado/06_integrador_producao/integrador_app.py): `POST /v1/assistente` bloqueia com HTTP `403` (`perfil_nao_autorizado`) quando o cliente autenticado solicita `perfil` acima do `perfil_maximo` vinculado à chave. Sem vínculo configurado, mantém-se o comportamento didático aberto.
2. **Degradação segura em falha persistente de *structured output*:**
   - Em `integrador_app.py` (`_executar_agente_e_gerar` e `responder`): se `gerar_estruturado` falhar após esgotar `max_reparos`, o integrador não lança HTTP `500`; devolve HTTP `200` com `RESPOSTA_RECUSA`, `acao_saida: "falha_esquema_estruturado"` e contador `falhas_esquema` em `GET /v1/relatorio`.
3. **Testes:** adicionados `test_anti_bfla_bloqueia_elevacao_de_perfil_com_403` e `test_falha_esquema_estruturado_degrada_sem_500` em [`test_p06_integrador.py`](../../laboratorios-mercado/06_integrador_producao/test_p06_integrador.py) (`74` smoke-tests offline no total).

## 2. Decisão do operador e encerramento de L1/L2

- Por decisão explícita do operador em `25/11/2026`, as etapas externas `L1` (revisão técnica humana) e `L2` (piloto com estudantes) foram **encerradas e substituídas pela revisão adversarial automatizada**, sem simular validação humana externa, fechando o material na **Versão Final 1.0** para estudo pessoal.

## 3. Avaliação realista final (Versão 1.0)

| Dimensão | Nota | Base factual e limites declarados |
|---|---|---|
| Conceitual (`guia-engenharia-llms.html`/`.pdf`) | **9,2 / 10** | 18 capítulos, 2 livros de Chip Huyen + 205 fontes web em cache, 453 questões sem viés de comprimento, 22 SVGs, 18 aquarelas, acessibilidade `axe-core` sem violações; teto em 9,2 por não ter revisão humana `L1` nem piloto `L2` |
| Prática de mercado (`laboratorios/` + `laboratorios-mercado/`) | **9,0 / 10** | 84 testes offline + 74 smoke-tests em 7 projetos, execuções reais registradas em container (`llama.cpp` `--jinja`, `pgvector`, Jaeger v3, Prometheus `/metrics`, `pdftoppm`, evals com *kappa* `0,7391` e bootstrap), anti-BFLA `403`, auth/rate limit e degradação segura; limites: sem treino QLoRA real (GPU AMD sem CUDA), sem chamada VLM remota e estado/rate-limit em memória de instância única |
| Acabamento e repositório | **9,3 / 10** | Raiz enxuta, históricos organizados em `docs/`, roteiro de estudo no `README.md`, 0 links quebrados, CI offline com build/smoke do `Containerfile` |
| **Nota técnica consolidada** | **9,1 / 10** | Média ponderada das três dimensões técnicas |
| **Nota geral realista (incluindo ausência de L1/L2 humanos)** | **8,9 / 10** | Desconto explícito de 0,2 pela substituição de revisão/piloto humano externo por revisão automatizada |
