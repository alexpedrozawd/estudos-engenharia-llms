# Planejamento: reestruturação do guia sem linguagens de programação

Estado: **versão 2, executada por completo em 15/10/2026** (leitura da Fase 4 feita pelo Opus 5.5 High no mesmo dia; achados no changelog). Próximo trabalho: `planejamento-capitulo-2-arquitetura-de-sistemas-com-llm.md`. Decisões do operador na Fase 0: manter os 15 módulos com módulo 2 substituto; linhas de comando só para ler; Sonnet 5.5 High; Chrome opcional incluído. Resultado em `changelog-reestruturacao-sem-programacao.md`. Autoria: claude - pessoal.

## 1. Pedido e decisões do operador (15/10/2026)
- Pedido: excluir por completo o que exija linguagem de programação; foco só em engenharia, arquitetura e operação de LLMs (locais ou de fronteira).
- Capítulo 2 (Software para sistemas com IA): **retirar do guia e arquivar** (não excluir).
- Critério: **sem ensinar nem exigir programar.** Podem aparecer, só para ler e explicar, textos curtos de configuração (JSON de requisição, schema, arquivo de parâmetros) e linhas de comando do runtime (padrão proposto; confirmar). Nenhum código a escrever ou entender como programa. O termo "código determinístico" continua válido como conceito de arquitetura (o que o sistema decide sem o modelo); o Capítulo 1 e os documentos de contexto o usam.
- Módulos 4, 5, 9, 10, 11 e 14: **manter, reescritos como arquitetura e decisão.** O módulo 9 deixa de se chamar "Ferramentas e código".
- As quatro decisões pendentes do Capítulo 2 (nível, pré-requisitos de Python, tamanho, Git) ficam **superadas.**
- Operador concordou em dobrar API/taxa/streaming/simultaneidade em outros módulos e renumerar para 14. **A revisão (item 3) mostrou que a renumeração tem custo não visto antes; a recomendação mudou e precisa de nova confirmação.**

## 2. Situação verificada (somente leitura)
- Guia com 20 páginas; código só no Capítulo 2 (15 blocos `cod-2-*`, 2 `cod-c2q*`); o Capítulo 1 não tem bloco de código.
- Atingido pela retirada: sumário (linhas do capítulo 2), introdução (frase de pré-requisitos de programação e o verbo "construí-la"), `page-nav` da página 10 (aponta para `#capitulo-2`), páginas 11 a 18, glossário (91 termos: 45 do Capítulo 1 e 46 do Capítulo 2; 1 termo cita 1.1 e 1.3), referências (28 itens), numeração (glossário e referências passam de 19 e 20 para 11 e 12).
- O Capítulo 1 (fechado) cita módulos pelo número em 7 trechos (módulos 3, 4, 5, 6, 7, 8 e 12), e o plano do Capítulo 1 e o contexto do Router também (blocos 1–5, 6–10, 11–15).

## 3. Achados da revisão final e ajustes
1. **Renumerar para 14 reabriria o Capítulo 1 fechado** (7 citações de módulo, partes 5/5/5 do sumário e da introdução, plano e contexto). Ganho: nenhum além de estética. **Ajuste: manter a numeração 1 a 15** e substituir o módulo 2 por um módulo sem programação (ver Fase 0).
2. O módulo substituto absorve o que o Capítulo 2 ensinava de conceito e que os módulos seguintes pressupõem: API de provedor como fronteira, pedido e resposta, limite de taxa, tempo limite, streaming, estado e persistência, nova tentativa, simultaneidade. Risco: sobreposição com 12, 14 e 15; delimitar no plano próprio do módulo.
3. **Risco de retomada:** o `CLAUDE.md` e o handoff de 15/10 ainda mandam decidir nível, Python, tamanho e Git. Se a sessão cair no meio, a próxima seguiria o rumo antigo. **Ajuste: apontar o `CLAUDE.md` para este plano já na Fase 1.**
4. Mover (não copiar) planejamento, pacotes de fontes e changelog do Capítulo 2 para o arquivo, depois de conferir hash; copiar só o guia (HTML completo). Cópia dupla gera duas fontes de verdade.
5. **Ganho marginal cortado:** não remover o CSS de bloco de código, a convenção do validador nem `executar-trechos-de-codigo.py` e `conferir-trechos.py`. O validador aceita guia sem código; os blocos servirão a textos de configuração; as ferramentas ficam sem uso, sem custo. Só `requisitos-de-formato-html-do-material.md` muda (questões médias e difícil com "trechos de código", linha 84).
6. **Glossário:** os 46 termos do Capítulo 2 saem do guia, mas vários (idempotência, contrato, determinismo, efeito colateral, condição de corrida, espera crescente) voltam em módulos futuros. Estão no arquivo; reaproveitar com nova redação, sem "Em Python".
7. Redução de validação: Chrome completo (6 larguras, axe, 5 questões) seria excessivo para uma remoção que não toca CSS nem questões do Capítulo 1. Obrigatório: validador, integridade dos `#id` e das tags, conferência de que o Capítulo 1 ficou idêntico. Opcional (pede sua aprovação): Playwright em 320 e 1280 px com axe.
8. IDs `unidade-2-*`, `questoes-capitulo-2` e `c2q*` ficam livres para o novo Capítulo 2; o arquivo está fora do guia, sem conflito.

## 4. Fases (um capítulo por vez; sem commit por fase; pasta fora de repositório)
Modelo/effort: Sonnet 5.5 High na execução; Opus 5.5 High na leitura da Fase 4. Haiku só se houver repositório e autorização (não há).

**Fase 0. Confirmação (antes de executar).** (a) Manter 15 módulos e substituir o módulo 2 por "Arquitetura de sistemas com LLM: fronteiras, APIs e estado" (nome provisório), em vez de renumerar para 14. (b) Linhas de comando de runtime permitidas só para ler. (c) Confirmar effort High.

**Fase 1. Arquivar.** Criar `arquivo\capitulo-2-software\`; copiar o guia como `guia-engenharia-llms-com-capitulo-2-2026-10-15.html` (hash de origem `7fadf7b0cbe4cd5e`); mover `planejamento-capitulo-2-...`, `pacotes-de-fontes-capitulo-2.md`, `changelog-capitulo-2.md` e `HANDOFF-...-decisoes-capitulo-2-...` e `HANDOFF-...-capitulo-2-...`. Conferir hashes e atualizar o `CLAUDE.md` (aponta para este plano). Aceite: cópia idêntica e nenhuma perda.

**Fase 2. Retirar o Capítulo 2.** Remover páginas 11 a 18; ajustar sumário, introdução (pré-requisitos e "construí-la"), `page-nav` da página 10 (para `#glossario`), numeração, glossário (45 termos do Capítulo 1) e referências (só o que o Capítulo 1 não cita). Aceite: sem `#capitulo-2`, `#unidade-2-*`, `questoes-capitulo-2` nem `cod-`; Capítulo 1 byte a byte igual ao original, exceto links de navegação.

**Fase 3. Validar.** `validar-guia.py` (0 falha); `#id` e links; tags equilibradas; comparação do Capítulo 1. Opcional: Chrome em 320 e 1280 px com axe.

**Fase 4. Plano mestre.** Revisar `planejamento-completo-estudos-engenharia-llms.md`: objetivo ("construir" → projetar, configurar, integrar, avaliar e operar), módulo 2 substituto, módulo 9 renomeado, marca "sem programar" nos módulos 4, 5, 9, 10, 11 e 14, e a frase "O módulo 2 será adaptado ao seu conhecimento de programação". Registrar o critério em `requisitos-de-formato-html-do-material.md`. Leitura pelo Opus High (decisão material).

**Fase 5. Fechamento.** `changelog-reestruturacao-sem-programacao.md`; handoff novo (`handoff-clean`); memória atualizada. Sem Git.

**Depois.** Planejar o novo Capítulo 2 com `demand-planning`; cada módulo reescrito ganha plano próprio.

## 5. Riscos
- Perda do Capítulo 2: mitigada por cópia e hash antes de remover.
- Links, ids e numeração: validador e conferência na Fase 3.
- Poda excessiva de glossário e referências: remover só o exclusivo do Capítulo 2.
- Sobreposição do módulo 2 substituto com 12, 14 e 15: delimitar no plano dele.

## 6. Fora do escopo
Redigir módulos novos; alterar o conteúdo do Capítulo 1; tocar nos projetos-fonte; aparelhos reais; pendências 3 a 7 do handoff de 15/10.

claude - pessoal, 15/10/2026
