# Correção da nota de fonte da unidade 1.4c (13/11/2026)

Origem: achado lateral registrado no handoff vigente, seção 4. Autoria: deepseek - conta não verificada. Projeto sem Git; nada foi commitado.

## 1. Verificação feita antes de corrigir

As três páginas foram abertas ao vivo em 13/11/2026.

- **Thinking** (`platform.claude.com/docs/en/build-with-claude/thinking`, a página citada pela nota): contém as duas frases da nota, literais — "the tokens Claude spends reasoning are billed as output tokens, even when the thinking text isn’t returned to you, and they count toward `max_tokens` alongside the response text" e "which lets Claude determine when and how deeply to think based on the request".
- **Extended thinking** (`…/extended-thinking`, citada pela nota da 2.2): tem "Thinking tokens count toward the `max_tokens` limit for the turn, so the budget must leave room for the final response", mas não tem as frases de cobrança.
- **Steering thinking** (`…/thinking-steering-and-cost`, antes pendente): tem "Tokens Claude uses while thinking (billed as output tokens)", "You are billed for the full thinking process, not the thinking content visible in the response" e "the model evaluates each request and determines whether to think and how much".

## 2. O que mudou

- **Guia, unidade 1.4c, nota "Custo e limite":** data de consulta de 15/10/2026 para 13/11/2026. As citações foram mantidas porque foram confirmadas na página citada. Nenhuma outra linha do guia mudou.
- **Pacote de fontes do capítulo 2:** a linha da Extended thinking registra o desfecho (a página Thinking tem as frases; a Steering thinking foi aberta); o achado 1 e a lacuna do billing como saída foram fechados.
- **PDF regenerado.**

## 3. Por que a troca de citação proposta não foi feita

A premissa do achado não se sustentou: as duas frases estão na página *Thinking*. Trocar a citação por "apoio indireto" ou condicionar à *Steering thinking* removeria uma citação direta e correta. A correção ficou na data, que era o único dado desatualizado. O registro anterior provavelmente conferiu a página *Extended thinking*, que de fato não tem as frases — mas a nota cita *Thinking*.

## 4. Validações

- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA**.
- PDF por Chrome for Testing 158.0.8127.18, 178 páginas A4. O Chrome do flatpak (157) foi descartado: sem a fonte Noto Sans Mono, trocava o monoespaçado por DejaVu e gerava 181 páginas. Páginas 1, 46, 155 e 178 conferidas em PNG; a nota corrigida aparece na 46.
- Não executado: impressão em papel, leitor de tela, aparelhos reais.

## 5. Hashes (SHA-256, 16 primeiros)

- `guia-engenharia-llms.html` `4fd56745e08b1530`
- `guia-engenharia-llms.pdf` `ff800aeca59ac66b`
- `pacote-de-fontes-capitulo-2-reestruturacao-2026-11-13.md` `c15481a6e642b481`
- Backup: `arquivo/antes-correcao-fonte-1-4c-2026-11-13/` (HTML `0f7d5613418acf7d`, PDF `98b94658ab680c13`).

Assinatura: deepseek - conta não verificada, 13/11/2026.
