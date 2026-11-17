# Changelog: protocolo de economia de tokens entre sessões (13/11/2026)

Autoria: deepseek - conta não verificada. Projeto sem Git. Pedido do operador: trocar a frase do `continue-work` e aplicar o protocolo nos dois arquivos de sessão.

## 1. O que mudou

- **`CLAUDE.md`:** a instrução de início de sessão deixou de mandar aplicar `continue-work` (comando inexistente, conferido em 13/11/2026) e passou a remeter ao `protocolo-de-economia-de-tokens-entre-sessoes.md`.
- **Handoff vigente (`handoff-reestruturacao-capitulo-2-2026-11-13.md`):** mesma troca na seção 0; hash do `CLAUDE.md` atualizado e o do protocolo acrescentado na seção 2; nova seção 7 registra a rodada.
- **Protocolo:** seção 6 atualizada para registrar que a frase foi trocada.
- **Guia e PDF não mudaram.** O achado lateral da unidade 1.4c continua aberto e fora do escopo.

## 2. Hashes (SHA-256, 16 primeiros)

- `guia-engenharia-llms.html` `0f7d5613418acf7d` (inalterado)
- `guia-engenharia-llms.pdf` `98b94658ab680c13` (inalterado)
- `CLAUDE.md` `689d18cc993e4674`
- `protocolo-de-economia-de-tokens-entre-sessoes.md` `855a8e4b2394503d`
- `planejamento-capitulo-1-fundamentos-de-ia-e-llms.md` `27959e5c1467be2a` (só a frase do §6.3 mudou)

## 3. Validações

- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: 16 OK, 0 FALHA.
- Nenhuma instrução para aplicar `continue-work` restou nos arquivos de sessão vigentes (`CLAUDE.md` e handoff); neles a palavra só aparece nas notas que registram a troca. Fora deles, a única referência em arquivo não superado era a de `planejamento-capitulo-1-fundamentos-de-ia-e-llms.md`, trocada nesta rodada; as demais estão em handoffs superados e no arquivo histórico.
- `planejamento-capitulo-1-fundamentos-de-ia-e-llms.md`, §6.3: a frase "aberta com o `continue-work` sobre este plano" passou a "aberta com este plano como entrada — use o handoff vigente e revalide os hashes".

deepseek - conta não verificada, 13/11/2026.
