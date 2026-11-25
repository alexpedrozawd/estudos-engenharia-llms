# Pacote de fontes do capítulo 5

Data: 16/11/2026. Autoria: claude - pessoal (Sonnet 5.5 High, painel). Cobre as fontes candidatas ao capítulo 5 (Avaliação e experimentação), conforme `planejamento-capitulo-5-avaliacao-e-experimentacao.md` §3. Cada trecho foi extraído do texto baixado em 16/11/2026; o resultado do `conferir-trechos.py` está na seção 3. Nenhuma afirmação do guia pode ir além do que o trecho diz.

## 1. Como reconferir

Baixar as fontes para uma pasta vazia e extrair o texto, com as chaves da coluna “Fonte”:

- `anthropic-demystifying-evals.txt` — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (redireciona para `/research/...`; metadado da página: publicado em 09/01/2026)
- `anthropic-develop-tests.txt` — https://platform.claude.com/docs/en/test-and-evaluate/develop-tests (a URL antiga `.../define-success` redireciona para ela; título da página: “Define success criteria and build evaluations”)
- `arxiv-2306.05685.txt` e `2306.05685.txt` — resumo em https://arxiv.org/abs/2306.05685 (v4, 24/12/2023) e PDF em https://arxiv.org/pdf/2306.05685
- `arxiv-2305.17926.txt` — resumo em https://arxiv.org/abs/2305.17926 (v2, 30/08/2023); o PDF tem duas colunas e não entra no pacote
- `arxiv-2411.00640.txt` e `2411.00640.txt` — resumo em https://arxiv.org/abs/2411.00640 (1/11/2024) e PDF em https://arxiv.org/pdf/2411.00640

As páginas HTML são extraídas com `python3 -I ferramentas/extrair-texto-web.py --entrada <pasta-bruta> --saida <pasta-textos>`; os PDFs, com `pdftotext -layout`.

Comando: `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-capitulo-5-2026-11-16.md --textos <pasta-textos> --projeto .`

## 2. Fontes e trechos

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| C5-01 | 5.1 Resultado adequado | texto | anthropic-develop-tests | Define your success criteria | consultada em 16/11/2026 | registrado na documentação | Specific: Clearly define what you want to achieve. |
| C5-02 | 5.1 Resultado adequado | texto | anthropic-develop-tests | Define your success criteria | consultada em 16/11/2026 | registrado na documentação | Measurable: Use quantitative metrics or well-defined qualitative scales. |
| C5-03 | 5.1 Resultado adequado | texto | anthropic-demystifying-evals | Step 2 | Anthropic, 09/01/2026 | registrado na fonte | A good task is one where two domain experts would independently reach the same pass/fail verdict. |
| C5-04 | 5.1 Resultado adequado | texto | anthropic-demystifying-evals | Step 2 | Anthropic, 09/01/2026 | registrado na fonte | Ambiguity in task specifications becomes noise in metrics. |
| C5-05 | 5.2 Exemplos e falhas | texto | anthropic-demystifying-evals | Step 1 | Anthropic, 09/01/2026 | registrado na fonte | In reality, 20-50 simple tasks drawn from real failures is a great start. |
| C5-06 | 5.2 Exemplos e falhas | texto | anthropic-demystifying-evals | Step 1 | Anthropic, 09/01/2026 | registrado na fonte | Evals get harder to build the longer you wait. |
| C5-07 | 5.2 Exemplos e falhas | texto | anthropic-demystifying-evals | Step 3 | Anthropic, 09/01/2026 | registrado na fonte | Test both the cases where a behavior should occur and where it shouldn't. |
| C5-08 | 5.2 Exemplos e falhas | texto | anthropic-demystifying-evals | Step 3 | Anthropic, 09/01/2026 | registrado na fonte | One-sided evals create one-sided optimization. |
| C5-09 | 5.2 Exemplos e falhas | texto | anthropic-develop-tests | Eval design principles | consultada em 16/11/2026 | registrado na documentação | Be task-specific: Design evals that mirror your real-world task distribution. |
| C5-10 | 5.2 Exemplos e falhas | texto | anthropic-develop-tests | Eval design principles | consultada em 16/11/2026 | registrado na documentação | Prioritize volume over quality: More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals. |
| C5-11 | 5.3 Referência inicial | texto | anthropic-demystifying-evals | Introdução | Anthropic, 09/01/2026 | registrado na fonte | Once evals exist, you get baselines and regression tests for free |
| C5-12 | 5.3 Referência inicial | texto | anthropic-develop-tests | Define your success criteria (exemplo) | consultada em 16/11/2026 | registrado na documentação | which is a 5% improvement over the current baseline (Achievable) |
| C5-13 | 5.3 Referência inicial | texto | arxiv-2306.05685 | Resumo | Zheng et al., 2023 (v4) | registrado no artigo | the inadequacy of existing benchmarks in measuring human preferences |
| C5-14 | 5.4 Testes e avaliações | texto | anthropic-demystifying-evals | Types of graders | Anthropic, 09/01/2026 | registrado na fonte | Agent evaluations typically combine three types of graders: code-based, model-based, and human. |
| C5-15 | 5.4 Testes e avaliações | texto | anthropic-demystifying-evals | Step 5 | Anthropic, 09/01/2026 | registrado na fonte | We recommend choosing deterministic graders where possible, LLM graders where necessary or for additional flexibility, and using human graders judiciously for additional validation. |
| C5-16 | 5.4 Testes e avaliações | texto | anthropic-demystifying-evals | Step 5 | Anthropic, 09/01/2026 | registrado na fonte | LLM-as-judge graders should be closely calibrated with human experts |
| C5-17 | 5.4 Testes e avaliações | texto | anthropic-demystifying-evals | Step 5 | Anthropic, 09/01/2026 | registrado na fonte | give the LLM a way out |
| C5-18 | 5.4 Testes e avaliações | texto | anthropic-demystifying-evals | Step 6 | Anthropic, 09/01/2026 | registrado na fonte | You won't know if your graders are working well unless you read the transcripts and grades from many trials. |
| C5-19 | 5.4 Testes e avaliações | texto | anthropic-demystifying-evals | Estrutura de uma avaliação | Anthropic, 09/01/2026 | registrado na fonte | but the outcome is whether a reservation exists in the environment’s SQL database |
| C5-20 | 5.4 Testes e avaliações | texto | anthropic-develop-tests | Choose how to grade | consultada em 16/11/2026 | registrado na documentação | Code-based grading: Fastest and most reliable, extremely scalable, but also lacks nuance for more complex judgments that require less rule-based rigidity. |
| C5-21 | 5.4 Testes e avaliações | texto | anthropic-develop-tests | Choose how to grade | consultada em 16/11/2026 | registrado na documentação | Human grading: Most flexible and high quality, but slow and expensive. Avoid if possible. |
| C5-22 | 5.4 Testes e avaliações | texto | anthropic-develop-tests | Choose how to grade | consultada em 16/11/2026 | registrado na documentação | LLM-based grading: Fast and flexible, scalable and suitable for complex judgment. Test to ensure reliability first, then scale. |
| C5-23 | 5.4 Testes e avaliações | texto | anthropic-develop-tests | Tips for LLM-based grading | consultada em 16/11/2026 | registrado na documentação | Have detailed, clear rubrics |
| C5-24 | 5.4 Testes e avaliações | texto | arxiv-2306.05685 | Resumo | Zheng et al., 2023 (v4) | registrado no artigo | including position, verbosity, and self-enhancement biases, as well as limited reasoning ability |
| C5-25 | 5.4 Testes e avaliações | texto | arxiv-2306.05685 | Resumo | Zheng et al., 2023 (v4) | registrado no artigo | achieving over 80% agreement, the same level of agreement between humans |
| C5-26 | 5.4 Testes e avaliações | texto | 2306.05685 | Seção sobre vieses | Zheng et al., 2023 (v4) | registrado no artigo | Position bias is when an LLM exhibits a propensity to favor certain positions over others. |
| C5-27 | 5.4 Testes e avaliações | texto | 2306.05685 | Seção sobre vieses | Zheng et al., 2023 (v4) | registrado no artigo | Verbosity bias is when an LLM judge favors longer, verbose responses, even if they are not as clear, high-quality, or accurate as shorter alternatives. |
| C5-28 | 5.4 Testes e avaliações | texto | 2306.05685 | Seção sobre soluções | Zheng et al., 2023 (v4) | registrado no artigo | A conservative approach is to call a judge twice by swapping the order of two answers and only declare a win when an answer is preferred in both orders. |
| C5-29 | 5.4 Testes e avaliações | texto | arxiv-2305.17926 | Resumo | Wang et al., 2023 (v2) | registrado no artigo | the quality ranking of candidate responses can be easily hacked by simply altering their order of appearance in the context |
| C5-30 | 5.4 Testes e avaliações | texto | arxiv-2305.17926 | Resumo | Wang et al., 2023 (v2) | registrado no artigo | Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator |
| C5-31 | 5.5 Regressões | texto | anthropic-demystifying-evals | Capability vs. regression evals | Anthropic, 09/01/2026 | registrado na fonte | They should start at a low pass rate, targeting tasks the agent struggles with and giving teams a hill to climb. |
| C5-32 | 5.5 Regressões | texto | anthropic-demystifying-evals | Capability vs. regression evals | Anthropic, 09/01/2026 | registrado na fonte | and should have a nearly 100% pass rate. They protect against backsliding, as a decline in score signals that something is broken and needs to be improved. |
| C5-33 | 5.5 Regressões | texto | anthropic-demystifying-evals | Capability vs. regression evals | Anthropic, 09/01/2026 | registrado na fonte | it’s important to also run regression evals to make sure changes don’t cause issues elsewhere |
| C5-34 | 5.5 Regressões | texto | anthropic-demystifying-evals | Capability vs. regression evals | Anthropic, 09/01/2026 | registrado na fonte | to become a regression suite that is run continuously to catch any drift |
| C5-35 | 5.5 Regressões | texto | anthropic-demystifying-evals | Step 7 | Anthropic, 09/01/2026 | registrado na fonte | An eval at 100% tracks regressions but provides no signal for improvement. |
| C5-36 | 5.6 Comparações confiáveis | texto | anthropic-demystifying-evals | Trials | Anthropic, 09/01/2026 | registrado na fonte | Because model outputs vary between runs, we run multiple trials to produce more consistent results. |
| C5-37 | 5.6 Comparações confiáveis | texto | anthropic-demystifying-evals | Medição de variação | Anthropic, 09/01/2026 | registrado na fonte | a task that passed on one eval run might fail on the next. |
| C5-38 | 5.6 Comparações confiáveis | texto | anthropic-demystifying-evals | Medição de variação | Anthropic, 09/01/2026 | registrado na fonte | pass@k measures the likelihood that an agent gets at least one correct solution in k attempts. |
| C5-39 | 5.6 Comparações confiáveis | texto | anthropic-demystifying-evals | Medição de variação | Anthropic, 09/01/2026 | registrado na fonte | pass^k measures the probability that all k trials succeed. |
| C5-40 | 5.6 Comparações confiáveis | texto | anthropic-demystifying-evals | Step 1 | Anthropic, 09/01/2026 | registrado na fonte | this large effect size means small sample sizes suffice. More mature agents may need larger, more difficult evals to detect smaller effects |
| C5-41 | 5.6 Comparações confiáveis | texto | arxiv-2411.00640 | Resumo | Miller, 2024 | registrado no artigo | Fundamentally, evaluations are experiments |
| C5-42 | 5.6 Comparações confiáveis | texto | 2411.00640 | Introdução, recomendação 4 (“When two models are being compared, conducting statistical inference on the question-level paired differences...”; o trecho começa depois da hifenização da quebra de linha) | Miller, 2024 | registrado no artigo | paired differences, rather than the population-level summary statistics |
| C5-43 | 5.6 Comparações confiáveis | texto | 2411.00640 | Introdução, recomendação 5 | Miller, 2024 | registrado no artigo | Using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest |
| C5-44 | 5.6 Comparações confiáveis | texto | 2411.00640 | Seção 2.1 | Miller, 2024 | registrado no artigo | We suggest reporting the standard error of the mean alongside (beneath) the mean when reporting eval scores. |
| C5-45 | 5.6 Comparações confiáveis | texto | anthropic-demystifying-evals | Medição de variação | Anthropic, 09/01/2026 | registrado na fonte | If your agent has a 75% per-trial success rate and you run 3 trials, the probability of passing all three is (0.75)³ ≈ 42%. |
| C5-46 | 5.4 Testes e avaliações | texto | anthropic-demystifying-evals | Estrutura de uma avaliação | Anthropic, 09/01/2026 | registrado na fonte | A flight-booking agent might say “Your flight has been booked” at the end of the transcript, but the outcome is whether a reservation exists in the environment’s SQL database. |
| C5-47 | 5.6 Comparações confiáveis | texto | anthropic-develop-tests | Define your success criteria (exemplo) | consultada em 16/11/2026 | registrado na documentação | On a held-out test set of 10,000 diverse Twitter posts |

## 3. Resultado da conferência

`conferir-trechos.py` em 16/11/2026: **47 aprovados, 0 reprovados** (total 47; C5-45 a C5-47 acrescentados na escrita das unidades 5.4 e 5.6), com as fontes baixadas e extraídas na mesma data. Houve uma reprovação inicial (C5-42), por hifenização do PDF em “question-level”; o trecho foi trocado por um fragmento literal sem a palavra quebrada e reaprovado. Os dois candidatos recordados do plano foram confirmados: Miller, *Adding Error Bars to Evals* (arXiv:2411.00640) e Wang et al., *Large Language Models are not Fair Evaluators* (arXiv:2305.17926).

## 4. Limites de uso (leia antes de escrever)

- **Data da Anthropic:** o metadado da página traz 09/01/2026 (`article:published_time`). A URL `/engineering/...` redireciona para `/research/...` em 16/11/2026; citar a URL original e a data de consulta.
- **Tensão entre as duas páginas da Anthropic:** a documentação diz “Prioritize volume over quality” (C5-10) e “Human grading ... Avoid if possible” (C5-21); o artigo de engenharia pede tarefas sem ambiguidade (C5-03) e uso judicioso de avaliadores humanos (C5-15). O guia não escolhe um lado: o conjunto de 20 a 50 casos exige qualidade de caso, e o volume só ajuda se o critério for claro. Isso é leitura do guia (*proposta didática*), não afirmação da fonte.
- **Casos de ajuste e reservados:** a documentação da Anthropic usa “held-out test set” só no exemplo de critério de sucesso (linhas “on a held-out test set of 10,000 diverse Twitter posts”). Nenhum trecho do pacote afirma que reusar os casos do ajuste infla o resultado. Essa regra entra como *proposta didática*.
- **Benchmark público não substitui avaliação própria:** C5-13 só diz que, para Zheng et al., benchmarks existentes eram inadequados para medir preferência humana. A frase do guia sobre “outra tarefa, outros dados” é *proposta didática*.
- **Zheng et al.:** “mais de 80% de concordância” vale para o juiz forte (GPT-4) contra preferências humanas, no conjunto MT-bench e no Chatbot Arena, em 2023. Não generalizar para outros juízes, modelos ou tarefas.
- **Wang et al.:** o resumo cita um resultado com ChatGPT como avaliador e Vicuna-13B; é exemplo de viés de ordem, não taxa geral.
- **Miller:** as tabelas do artigo usam modelos e números fictícios (“fictional models and numbers”). As recomendações são para quem tem treino em estatística; o guia traduz sem fórmulas e marca como explicação do guia o que não estiver nos trechos.
- **pass@k e pass^k:** o texto da Anthropic trata de agentes; no guia, a ideia (acertar uma vez ou acertar sempre) aplica-se ao assistente por analogia (*proposta didática*). O exemplo numérico da fonte (75% por tentativa, três tentativas) pode ser citado com atribuição.
- **Não verificado:** “mais de 80% de concordância” aparece também em resumos de terceiros; só o resumo do arXiv (C5-25) conta como fonte primária.

## 5. Estado

- Pacote criado em 16/11/2026; nenhum trecho do guia usa estas fontes ainda.
- Pasta temporária com as fontes: `/tmp/cap5-fontes` (não é fonte de verdade; baixar de novo para reconferir).

claude - pessoal, 16/11/2026
