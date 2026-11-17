# Changelog — capítulo 4: pacote de fontes e bloco 1

Data: 13/11/2026. Autoria: deepseek - conta não verificada (painel). Rodada: Bloco 1 (fontes) e primeira metade do Bloco 2 (abertura e unidade 4.1). O capítulo 4 **não está concluído**.

## 1. O que mudou

- **Novo:** `pacote-de-fontes-capitulo-4-2026-11-13.md`, com 24 trechos literais de 13 fontes, todos conferidos pelo `conferir-trechos.py` (24/24).
- **Guia:** abertura do capítulo 4 e as três partes da unidade 4.1 (`4-1a`, `4-1b`, `4-1c`), com dois blocos de prompt ilustrativos e uma tabela.
- **Navegação:** o sumário aponta para `#capitulo-4` e para a 4.1; as questões do capítulo 3 passam a apontar para o capítulo 4; o glossário aponta para a 4.1c (estado intermediário).
- **Impressão:** `#capitulo-4` entrou na lista de seções que começam em página nova; a lista também já prevê `#questoes-capitulo-4`.
- **Numeração:** 77 páginas lógicas. Glossário passou a 76 e Referências a 77.
- **PDF:** regerado com Chrome for Testing 158.0.8127.18, 266 páginas A4. Páginas do capítulo 4 conferidas em PNG, na versão intermediária e na final; nenhum bloco dividido; o capítulo começa em página nova.

## 2. Decisões do operador aplicadas

1. Estrutura aprovada: seis unidades, 20 partes (3/4/3/3/3/4), seis questões.
2. O indício sobre a remoção de `temperature`, `top_p` e `top_k` na Anthropic entra no capítulo como fato registrado na documentação, com data, e será confirmado no fechamento.
3. A pausa era o ponto de checagem depois da abertura e da 4.1; este bloco para aqui para o operador aprovar nível, exemplo e tabela.
4. Fontes confirmadas: Brown, Wei e Min; Anthropic; OpenAI; JSON Schema.
5. Três molduras de imagem confirmadas (4.1a, 4.3a, 4.6b), só como moldura.
6. Prompt em bloco não executável, com legenda “ilustrativo, não executado”.

## 3. Validações

- `conferir-trechos.py`: 24 aprovados, 0 reprovados.
- `validar-guia.py`: 16 OK, 0 FALHA; 77 páginas em sequência.
- Estrutura: 78 seções abertas e fechadas, 84 fieldsets, ids sem duplicata; a 4.1 tem 3 partes, 3 perguntas e 4 alternativas por pergunta.
- PDF: 266 páginas A4; capítulo 4 na página física 233; 4.1c em 241; glossário em 245.
- **Não executado:** reflow em 320 px, axe-core, leitor de tela, aparelhos reais, segunda leitura independente das citações.

## 4. Hashes (16 caracteres)

- `guia-engenharia-llms.html`: `dee65d72c838dd29`
- `guia-engenharia-llms.pdf`: `8f1e887ca4b798c5`
- `pacote-de-fontes-capitulo-4-2026-11-13.md`: `8ef533d293c65ccc`
- `planejamento-capitulo-4-prompts-parametros-e-respostas.md`: `db29d34237704f28`

## 5. Pendências

1. Escrever 4.2 a 4.6 (17 partes), as seis questões do capítulo, o glossário (termos das seis unidades) e as referências do capítulo 4.
2. Trocar, no sumário e na abertura, os itens 4.2 a 4.6 e “Questões do capítulo 4” de texto para links, quando as âncoras existirem.
3. Trocar a navegação do glossário de “Parte 4.1c” para “Questões do capítulo 4” no fim.
4. Renumerar glossário e referências a cada bloco novo (as páginas crescem).
5. Regerar o PDF no fechamento; conferir páginas novas.
6. Decidir a geração das imagens (4.1a, 4.3a, 4.6b) só depois do texto validado.

## 6. Backup

- `arquivo/antes-capitulo-4-2026-11-13/` criado **depois** da edição. O HTML anterior foi reconstruído por operações inversas e o hash bateu exatamente com o estado de entrada (`78afd3998fa2c19e`, 253 páginas de PDF na regeneração).
- O PDF do backup foi regerado a partir do HTML reconstruído: 253 páginas, hash `92dd196e3e45245c`. Não são os bytes originais (`a0b8f86d9f2a6df3`), porque o hash do PDF muda a cada geração; a paginação e o conteúdo conferem.
- **Procedimento correto, repetido do capítulo 3:** copiar HTML e PDF para `arquivo/antes-<motivo>-<data>/` **antes** da primeira edição. Registrado para não se repetir.

## 7. Ressalvas

- O prompt da 4.1c é ilustrativo e não foi executado; nenhuma chamada real a modelo foi feita.
- A página de migração da Anthropic foi lida em cópia baixada em 13/11/2026; a data de publicação não aparece no texto extraído.
- O texto da 4.1b foi ajustado para não afirmar que exemplo “nunca ensina” uma regra: ele não é fonte confiável para fato ou regra de negócio; a regra precisa estar escrita e conferível.

Assinatura: deepseek - conta não verificada, 13/11/2026.
