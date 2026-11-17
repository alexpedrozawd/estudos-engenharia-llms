# Changelog — Capítulo 1 (Fundamentos de IA e LLMs)

## 15/10/2026 — Bloco 3 (revisão) e Bloco 4 (validação e registro)

Autoria: claude - ap. Bloco 3 em Opus 5.5 High (escolha do operador, acima do Medium recomendado). Bloco 4 em Haiku 5.5 Medium (acima do Low recomendado). Sem Git: a pasta não é repositório.

### Alterações no guia (`guia-engenharia-llms.html`)

- Unidade 1.4: a fonte cita três estratégias de escolha no §7.6, e top-k e top-p aparecem no §7.6.4. Incluídos como menção.
- Unidade 1.5: os pesos de atenção foram separados dos pesos do modelo. Retirada a frase "um texto maior costuma trazer mais pistas", que contradizia a 1.3. "Custo cresce com o quadrado" virou "custo da atenção".
- Unidade 1.4: frase sobre o assistente com a Nanda Mac virou condicional, com rótulo *proposta didática*. "Explicam" virou "podem explicar".
- Unidade 1.1 e 1.2: advertência sobre antropomorfismo inclui "esquece" e segue o §1.11. Retirada a formulação "o que o modelo sabe".
- Questões 1 e 3: distratores alongados para que a correta não se destaque pelo tamanho. Gabarito mantido (B, D, A, C, B).
- Ajustes menores: "reembolsável" deixou de ser "fictícia"; definição de *verificado no código local* com "sem executá-lo"; "documentação de estudo" do Router; "forma de atenção" em Vaswani; "nesta unidade" na caixa opcional.

### Pacotes de fontes (`pacotes-de-fontes-capitulo-1.md`)

- 12 trechos acrescentados (1.1-T6 a T8, 1.2-T15 e T16, 1.3-T14, 1.4-T15 a T19, 1.6-T11), conferidos contra o rascunho de 19/08/2026.
- Registrado: extrair o PDF sem `-layout`.

### Validações executadas em 15/10/2026

- `python -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: 13 OK, 0 FALHA.
- `python -I ferramentas/conferir-trechos.py`: 102 aprovados, 0 reprovados.
- Pendente: reflow em 320 px no navegador (teste de Chrome não está em `ferramentas/`); conforto nos três aparelhos reais.

### Hashes SHA-256 (16 primeiros caracteres)

- `guia-engenharia-llms.html`: bac10c9573db4598
- `pacotes-de-fontes-capitulo-1.md`: bbb9c5bef5767b44
- `validar-guia.py`: f3ae508ab623a71f
- `conferir-trechos.py`: 3c83f88c0819fba4
- `planejamento-capitulo-1-fundamentos-de-ia-e-llms.md`: 43b3d5d71d5d9d18 (inalterado)

### Pendências

- Decidir se o plano §4 deve citar as quatro estratégias de decodificação (não alterado).
- Pendências 1 a 8 do handoff de 13/10 seguem abertas.
- Bloco 4b (piloto Haiku High) não iniciado.

claude - ap, 15/10/2026
