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

## 4. Validação completa pós-edição

- `84` testes offline em `laboratorios/`, `76` smoke-tests em `laboratorios-mercado/`, `guia.py fechar` (`0` falhas), `testar-ferramentas.py --rapido`, `testar-fontes.py`, `testar-livros.py`, `podman compose config -q` (todos os perfis incluindo `finetuning`), `Containerfile` build/run e hashes congelados de `guia-engenharia-llms.html`/`.pdf` preservados intactos.
