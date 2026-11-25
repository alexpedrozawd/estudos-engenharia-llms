# Changelog — Adaptação AMD ROCm (`gfx1201`), anti-BFLA real e arquivamento VLM (25/11/2026)

Data: 25/11/2026. Autoria: `agy - ap`.

## 1. Projeto 04 (`04_qlora_peft`) em GPU AMD Radeon RX 9070 XT (`gfx1201`)

- **Adaptação de código e infraestrutura (sem alterar a imagem base do Bazzite):**
  - [`laboratorios-mercado/04_qlora_peft/treinar_qlora.py`](../../laboratorios-mercado/04_qlora_peft/treinar_qlora.py): detecção agnóstica CUDA/ROCm (`detectar_acelerador` distinguindo `torch.version.hip` vs `torch.version.cuda`), suporte a `--sem-quant` (LoRA em `bfloat16` opcional), `--epocas` e avaliação direta por `--backend hf` com `--adaptador`.
  - [`laboratorios-mercado/04_qlora_peft/qlora_receita.py`](../../laboratorios-mercado/04_qlora_peft/qlora_receita.py): validação de `dtype_computo` (`bfloat16`, `float16`, `float32`) e campo opcional `acelerador` no `manifesto(...)` sem alterar o hash da configuração padrão.
  - [`laboratorios-mercado/compose.yaml`](../../laboratorios-mercado/compose.yaml): serviço `qlora-rocm` sob `--profile finetuning` com `docker.io/rocm/pytorch:rocm7.14.1_ubuntu24.04_py3.13_pytorch_release_2.12.0`, repasse de `/dev/kfd` e `/dev/dri`, volumes `hf-cache` e `rocm-opt-venv`.
  - [`laboratorios-mercado/pyproject.toml`](../../laboratorios-mercado/pyproject.toml): piso do extra `[finetuning]` ajustado para `bitsandbytes>=0.50` (suporte estável a `gfx1201` via ROCm).
- **Execução real registrada em [`p04-qlora-rocm-2026-11-25T08-02-17-0300.json`](../../laboratorios-mercado/execucoes/p04-qlora-rocm-2026-11-25T08-02-17-0300.json):**
  - Base `Qwen/Qwen3-1.7B` (QLoRA NF4 4-bit + `bfloat16`, `torch 2.12.0+rocm7.14.1`, `bitsandbytes 0.50.2`): acurácia `0,6667`, formato `100%` (`com_ruido: 0,50`, `formal: 0,75`, `informal: 0,75`).
  - Com configuração padrão (`3` épocas, `6` passos, `8,55 s`): `0,5833` (`informal` caiu para `0,25`); portão **reprovou** (`exit code 2`).
  - Com `--epocas 12` (`24` passos, `22,53 s`): `0,9167` (`+0,25` em todas as fatias: `com_ruido: 0,75`, `formal: 1,00`, `informal: 1,00`), formato `100%`, **aprovado** pelo portão (`exit code 0`).

## 2. Projeto 06 (`06_integrador_producao`) — Validação real anti-BFLA

- [`laboratorios-mercado/06_integrador_producao/cliente_integrador_real.py`](../../laboratorios-mercado/06_integrador_producao/cliente_integrador_real.py): adicionadas flags `--chave-aluno`, `--chave-admin` e `--somente-bfla`.
- Execução real contra `uvicorn` + `llama.cpp` (`qwen3-4b-instruct`) + `pgvector` com `INTEGRADOR_PERFIS_CHAVES`: `4/4` verificações aprovadas (`401` sem chave, `403 perfil_nao_autorizado` na elevação `aluno -> admin`, `200` sem vazamento no perfil `aluno` e `200` autorizado no perfil `admin`), registrada em [`p06-integrador-anti-bfla-2026-11-25T07-46-25-0300.json`](../../laboratorios-mercado/execucoes/p06-integrador-anti-bfla-2026-11-25T07-46-25-0300.json).

## 3. Projeto 07 (`07_evals_e_multimodal`) — Arquivamento VLM remoto

- Por decisão do operador em `25/11/2026`, a chamada opcional a VLM remoto foi arquivada em [`laboratorios-mercado/07_evals_e_multimodal/README.md`](../../laboratorios-mercado/07_evals_e_multimodal/README.md), mantendo código, smoke-tests e renderização PNG via `pdftoppm`.

## 4. Ajustes pós-auditoria (`/auditorias` + `/revisar`)

- [`laboratorios-mercado/04_qlora_peft/README.md`](../../laboratorios-mercado/04_qlora_peft/README.md): documentada trava `-c` para `torch==2.12.0+rocm7.14.1` ao preparar o volume `/opt/venv` de `qlora-rocm`.
- [`laboratorios-mercado/06_integrador_producao/cliente_integrador_real.py`](../../laboratorios-mercado/06_integrador_producao/cliente_integrador_real.py): `--somente-bfla` sem `--chave-aluno`/`--chave-admin` agora retorna erro explícito (código `2`).
- [`laboratorios-mercado/06_integrador_producao/integrador_app.py`](../../laboratorios-mercado/06_integrador_producao/integrador_app.py): `GET /v1/relatorio` passou a exigir perfil mínimo `coordenacao` quando `AURORA_PERFIS_CHAVES`/`perfis_por_chave` está ativo (HTTP `403` para `aluno`).

## 5. Validação completa pós-edição

- `84` testes offline em `laboratorios/`, `77` smoke-tests em `laboratorios-mercado/`, `guia.py fechar` (`0` falhas), `testar-ferramentas.py --rapido`, `testar-fontes.py`, `testar-livros.py`, `podman compose config -q` (todos os perfis incluindo `finetuning`), `Containerfile` build/run, CI remoto `testes-offline` aprovado e hashes congelados de `guia-engenharia-llms.html`/`.pdf` preservados intactos.

## 6. Avaliação realista atualizada (mercado de trabalho real — 25/11/2026)

| Dimensão | Nota | Base factual e limites declarados |
|---|---|---|
| Conceitual e pedagógica (`guia-engenharia-llms.html`/`.pdf`) | **9,2 / 10** | 18 capítulos (~229 mil palavras), 2 livros de Chip Huyen + 205 fontes web de 2026 em cache, 453 questões balanceadas sem viés de comprimento, 18 rubricas quantitativas, 22 SVGs e `axe-core` sem violações; teto em 9,2 pela ausência de revisão técnica humana externa (`L1`) e piloto com estudantes (`L2`). |
| Prática de mercado (`laboratorios/` + `laboratorios-mercado/`) | **9,3 / 10** | 84 testes offline + 77 smoke-tests em 7 projetos e 15 execuções reais registradas (`llama.cpp` `--jinja`, `pgvector` com ACL SQL, MCP 2.x com sandbox sem rede, QLoRA 4-bit NF4 real na RX 9070 XT com portão reprovando 3 épocas e aprovando 12 épocas, SSE/Prometheus/OTLP Jaeger v3, anti-BFLA `403` em `/v1/assistente` e `/v1/relatorio`, evals com *kappa* `0,7391` + `pdftoppm`). |
| Engenharia, CI e acabamento do repositório | **9,4 / 10** | Raiz enxuta, históricos organizados em `docs/`, roteiro de estudo no `README.md`, 0 links quebrados nos `.md` rastreados, `compose.yaml` multi-perfil (incluindo `finetuning`) e CI remoto verde com build/smoke do `Containerfile`. |
| **Nota técnica consolidada** | **9,3 / 10** | Média ponderada das três dimensões técnicas |
| **Nota geral realista (mercado de trabalho)** | **9,1 / 10** | Desconto de `0,2` pela ausência de validação humana externa (`L1`/`L2`); fronteiras declaradas de escala distribuída (estado em memória de processo único), datasets didáticos (VLM remoto arquivado), serving GPU de alta carga (`vLLM`/`SGLang`) e segurança adaptativa (*red teaming*). |
