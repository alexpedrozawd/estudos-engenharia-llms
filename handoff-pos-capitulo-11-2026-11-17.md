# Handoff: Parte II concluída (Capítulos 9, 10 e 11); próximo é Parte III — Capítulo 12 (17/11/2026)

Origem: agy - ap (Gemini 4 Hydrogen High, painel). Projeto: `/var/home/apsrv/Documentos/Projetos/estudos-engenharia-llms` (repositório Git público `https://github.com/alexpedrozawd/estudos-engenharia-llms`). Substitui `handoff-pos-capitulo-8-2026-11-17.md` (movido para `arquivo/`). Sessão continuada, sem memória da anterior: antes de agir, leia `protocolo-de-economia-de-tokens-entre-sessoes.md`, revalide hashes (`sha256sum`, 16 primeiros caracteres) e rode `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`. Histórico não autoriza ações.

## Objetivo
Avançar para a **Parte III** iniciando pelo **Capítulo 12 — Harnesses, workflows e agentes**, mantendo Capítulos 1–11 validados.

## Decisões confirmadas pelo operador (17/11/2026)
- **Conclusão integral da Parte II (Capítulos 9, 10 e 11):** aprovada pelo operador em 17/11/2026 e entregue com 172 trechos literais conferidos nos pacotes dos três capítulos.
- **Busca por símbolos (Cap. 11):** decidida com base em fontes primárias (`ripgrep`, `Tree-sitter` e Anthropic *Effective context engineering*): busca textual ao vivo (`glob`/`grep`) evita índices obsoletos em código mutável; busca por símbolos com árvore sintática só entra quando é necessário distinguir definição de citação em bases formais grandes.
- **Cache e esforço (Cap. 9):** incorporada a correção factual observada na documentação da Anthropic (mudar `output_config.effort` no meio da conversa depende do modelo e do modo de envio — Opus 5.5 preserva com `output_config` por mensagem, mas outros modelos/modos podem invalidar blocos).
- **Neutralidade e formato preservados:** partes `<= 500` palavras até `Pergunta`, `<= 1` tabela por parte, **88/88** tabelas com `.rolagem`, zero `AP AI Router`/`Nanda`, múltiplos fornecedores, apenas molduras `role="img"`, links externos com `target="_blank" rel="noopener noreferrer"`.

## Estado verificado
- `guia-engenharia-llms.html` `718ddeec0ecb86d8` (**237 páginas lógicas**; Capítulos 1–11 completos; Glossário p. 236 com 312 termos; Referências p. 237).
- `guia-engenharia-llms.pdf` `3893b8e1553e915f` (**720 páginas A4**, Chrome 158).
- `pacote-de-fontes-capitulo-9-contexto-e-memoria-2026-11-17.md` `521e6aa801a53963` (77 trechos).
- `pacote-de-fontes-capitulo-10-ferramentas-e-integracoes-2026-11-17.md` `9afa157a2e21c70e` (53 trechos).
- `pacote-de-fontes-capitulo-11-busca-indexacao-e-rag-2026-11-17.md` `fafd6cbf02b3896d` (42 trechos).
- `planejamento-completo-estudos-engenharia-llms.md` `53dc380144e0f69b` (Módulos 1–11 concluídos).
- Backup pré-Parte II restante em `arquivo/antes-parte-2-caps-9-11-2026-11-17/`.

## Validações executadas em 17/11/2026
- `conferir-trechos.py`: Cap. 9 (**77/77**), Cap. 10 (**53/53**), Cap. 11 (**42/42**).
- `validar-guia.py`: **16 OK, 0 FALHA** (237 páginas lógicas, 464 links web, 277 questões/regiões/fieldsets).
- Script estrutural: **88/88** tabelas com `.rolagem`, **0** termos proibidos, **0** duplicatas no Glossário.
- Auditoria Chrome 158 em **320 px**: `innerW: 320`, `clientWidth: 305`, `scrollWidth: 305`, **0 estouros** fora de `.rolagem`/`pre` nas 63 seções verificadas + retorno interativo verificado em `c9q3`, `c10q4` e `c11q5`.
- PDF conferido visualmente em 7 páginas renderizadas (`4, 5, 523, 580, 586, 650, 717`).

## Pendências (em ordem)
1. **Parte III (Capítulos 12–16):** iniciar pelo **Capítulo 12 — Harnesses, workflows e agentes** (`planejamento-completo-estudos-engenharia-llms.md`: Anthropic *Building effective agents* e *Effective harnesses for long-running agents*, além de documentação de agentes de outros fornecedores para neutralidade; referenciar Cap. 6 `EG-15`–`EG-30`, `EG-33`–`EG-43` sem duplicar).
2. **Capítulos 13–16:** Inferência local, Seleção e roteamento, Integração empresarial e LLMOps, Eficiência e economia.
3. **Última etapa (após texto revisado):** gerar imagens em aquarela medieval (1056×704), revisão do Cap. 4 com Opus 5.5 High (se mantida) e validação nos três aparelhos físicos (Galaxy S24, Nitro 5, APSRV 55").

## Armadilhas
- Nunca abrir `guia-engenharia-llms.html`, o PDF ou backups inteiros; usar `grep -n` + leitura localizada.
- `validar-guia.py` não valida ordem de `page-nav` nem reflow em 320 px; manter scripts de verificação após edições.
- Pastas `/tmp/cap9-*`, `/tmp/cap10-*`, `/tmp/cap11-*`, `/tmp/pdf-p2` e `/tmp/audit320_p2.mjs` são voláteis.

## Próxima ação
Ler `protocolo-de-economia-de-tokens-entre-sessoes.md` e este handoff, revalidar hashes e `validar-guia.py`, e preparar o pacote de fontes públicas + mapa de unidades/partes curtas do **Capítulo 12 — Harnesses, workflows e agentes** (Parte III).

Assinatura: agy - ap, 17/11/2026.
