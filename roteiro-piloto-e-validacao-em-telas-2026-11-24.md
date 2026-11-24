# Roteiro de piloto e validação em telas (`L2`)

Data: 24/11/2026. Escopo definido pelo operador: **leitura exclusiva em telas** (smartphones, tablets, notebooks e televisores) e **leitor de tela**. A validação em papel A4 foi desconsiderada por decisão explícita do operador.

## 1. Piloto com leitores (3 a 5 pessoas)

Objetivo: medir compreensão real, ritmo de leitura (TDAH) e clareza das questões e dos blocos de código sem assistência do autor.

### Seleção sugerida de capítulos
1. **Capítulo conceitual/estrutural:** [Capítulo 6 — Engenharia de Dados e Datasets para IA](guia-engenharia-llms.html#capitulo-6) (18 partes curtas + 6 questões + estudo de caso).
2. **Capítulo operacional/quantitativo:** [Capítulo 15 — Fine-tuning, Quantização e Destilação](guia-engenharia-llms.html#capitulo-15) (18 partes curtas + 6 questões + estudo de caso).
*(Alternativa rápida: 1 unidade completa de cada capítulo + as 6 questões de fechamento.)*

### Protocolo por participante
1. Entregar apenas o link/arquivo [guia-engenharia-llms.html](guia-engenharia-llms.html) aberto no navegador do aparelho que a pessoa usa no dia a dia.
2. Registrar aparelho, navegador, zoom do sistema e hora de início.
3. Pedir que leia as partes em sequência sem pular `Em 3 linhas`, `Pense assim.` e `Pergunta`, respondendo às perguntas na hora e anotando qualquer termo ou frase que exija releitura.
4. Ao fim do capítulo, resolver as 6 questões de fechamento e ler a rubrica do estudo de caso após formular uma resposta curta em voz alta ou texto.

### Formulário de registro do piloto

| Participante | Aparelho / Tela | Tempo total | Acertos (texto) | Acertos (fechamento) | Trechos onde travou (parte + motivo) | Termos pouco claros |
|---|---|---|---|---|---|---|
| Leitor 1 | | | /18 | /6 | | |
| Leitor 2 | | | /18 | /6 | | |
| Leitor 3 | | | /18 | /6 | | |
| Leitor 4 | | | /18 | /6 | | |
| Leitor 5 | | | /18 | /6 | | |

Critério de aceite do piloto: todos os participantes completam sem ajuda externa, apontam eventuais pontos de fadiga ou jargão solto para ajuste, e não há questão ambígua com erro sistemático pela mesma razão.

---

## 2. Validação manual nos aparelhos de tela

Executar sobre a versão atual de [guia-engenharia-llms.html](guia-engenharia-llms.html), verificando pelo menos a capa, o sumário, a parte `6.3c` (código), `6.4c` (tabela + código + moldura), `15.3c` (código), `15.4a` (código + moldura) e as páginas de questões.

| Dispositivo / Categoria | Condição de teste | O que conferir | Situação |
|---|---|---|---|
| **Smartphone (Galaxy S24)** | Retrato e paisagem; zoom padrão e texto ampliado (+125%) | Sem rolagem horizontal na página; tabelas em `.rolagem` e código em `pre.codigo` rolam só dentro do próprio bloco; botões e alternativas fáceis de tocar; feedback legível após marcar | [x] Concluído em 24/11/2026 (layout aprovado pelo operador; sem ajustes solicitados) |
| **Notebook (Acer Nitro 5, 15" 1080p)** | Janela cheia e meia tela | Comprimento de linha confortável (~55–70 caracteres); hierarquia de títulos e contraste de texto `#000` sobre `#f5f1e8`; navegação por teclado (`Tab`, setas nos `radio`, foco visível em `tabindex="0"`) | [ ] Ignorado por decisão explícita do operador em 24/11/2026 |
| **Televisor (LG OLED EVO C5 4K 55")** | Distância real de uso da sala | Tamanho de fonte legível sem forçar a vista; coluna central limitada sem linhas extensas demais; contraste de alertas verde/vermelho nas questões | [ ] Não registrado em separado; etapa encerrada pelo operador após aprovação no S24 |

*(Nota: o teste em tablet genérico foi substituído pelos aparelhos reais informados pelo operador em 24/11/2026.)*

---

## 3. Validação em leitor de tela

Testar com leitor de tela real (ex.: NVDA/Orca no notebook ou TalkBack no Galaxy S24) pelo menos uma unidade com tabela e código (`6.4c`) e uma questão (etapa encerrada pelo operador sem apontamentos humanos adicionais; acessibilidade automatizada validada via `axe-core` com `45` passes e `0` violações em `1280×800` e `320×640`):

- [ ] A capa anuncia apenas título e subtítulo, sem número de página. *(Não executado manualmente; dispensado no encerramento da etapa.)*
- [ ] Marcos (`main`, `nav`, cabeçalhos `h2`/`h3`) permitem saltar entre capítulos, partes e sumário. *(Não executado manualmente; dispensado no encerramento da etapa.)*
- [ ] Blocos `.rolagem` e `pre.codigo` / `pre.saida` são anunciados como regiões (`role="region"`) com rótulo claro e acessíveis por teclado (`tabindex="0"`). *(Não executado manualmente; dispensado no encerramento da etapa.)*
- [ ] Molduras de imagem com `role="img"` leem a descrição do `aria-label` sem anunciar texto decorativo redundante. *(Não executado manualmente; dispensado no encerramento da etapa.)*
- [ ] Ao marcar uma alternativa na questão, a região `.retorno` (`role="status"`, `aria-live="polite"`) anuncia `Correto.` ou `Incorreto.` e a explicação sem perder o foco do controle selecionado. *(Não executado manualmente; dispensado no encerramento da etapa.)*
- [ ] O número da página no rodapé (`role="img"`, `aria-label="Página N"`) lê de forma natural sem interromper a navegação. *(Não executado manualmente; dispensado no encerramento da etapa.)*

---

## 4. Registro de encerramento do `L2`

- Data de conclusão dos testes: 24/11/2026
- Ajustes de CSS/HTML solicitados (se houver): Nenhum (layout aprovado pelo operador no Galaxy S24; Acer Nitro 5 ignorado e piloto externo/leitor de tela dispensados para conclusão da etapa L2).
- Responsável pelo registro: Alexandre Pedroza (operador) / agy - ap

Assinatura: agy - ap (roteiro preparado e etapa L2 encerrada conforme decisão do operador em 24/11/2026).
