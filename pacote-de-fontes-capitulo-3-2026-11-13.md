# Pacote de fontes do capítulo 3

Data: 13/11/2026. Autoria: deepseek - conta não verificada (painel). Cobre as fontes citadas no capítulo 3 do guia. Cada trecho foi conferido contra a página baixada na mesma data; o resultado do `conferir-trechos.py` está na seção 3.

## 1. Como reconferir

Baixar as fontes para uma pasta vazia e extrair o texto, com as chaves da coluna “Fonte”:

- `rfc2119.txt` — https://www.rfc-editor.org/rfc/rfc2119.txt (texto puro; a URL `.html` do mesmo endereço também serve)
- `nasa-se.txt` — https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf, convertido com `pdftotext`
- `nist-ai-rmf.txt` — https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf, com `pdftotext`
- `scrum-guide-2020.txt` — https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf, com `pdftotext`
- `nng-persona.txt` e `anthropic-evals.txt` e `anthropic-agents.txt` — páginas HTML, extraídas com `ferramentas/extrair-texto-web.py`

Comando: `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-capitulo-3-2026-11-13.md --textos <pasta> --projeto .`

## 2. Fontes e trechos

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| C3-01 | 3.1 Problema e usuário | texto | nasa-se | §4.1.1.2.3 | NASA/SP-2016-6105 Rev2, 2016 | registrado na norma | Needs are defined in the answer to the question “What problem are we trying to solve?” |
| C3-02 | 3.1 Problema e usuário | texto | nasa-se | §4.1.1.2.3 | idem | registrado na norma | NGOs are not contractual requirements or designs |
| C3-03 | 3.1 Problema e usuário | texto | nasa-se | §4.1.1.2.3 | idem | registrado na norma | to know who the primary stakeholders are and who has the decision authority to help resolve conflicts |
| C3-04 | 3.1 Problema e usuário | texto | nng-persona | Definição de persona | 03/10/2025 | registrado na documentação | A persona is a fictional, yet realistic, description of a typical or target user of the product |
| C3-05 | 3.1 Problema e usuário | texto | nng-persona | Criação de personas | idem | registrado na documentação | Personas must be based on user research to accurately represent a product’s users |
| C3-06 | 3.3 Restrições | texto | nist-ai-rmf | MAP 1.1 | NIST AI 100-1, janeiro de 2023 | registrado na norma | prospective settings in which the AI system will be deployed are understood and documented |
| C3-07 | 3.3 Restrições | texto | nist-ai-rmf | MAP 1.1 | idem | registrado na norma | the specific set or types of users along with their expectations |
| C3-08 | 3.3 Restrições | texto | rfc2119 | §1 | RFC 2119, BCP 14, março de 1997 | registrado na norma | an absolute requirement of the specification |
| C3-09 | 3.3 Restrições | texto | rfc2119 | §3 | idem | registrado na norma | there may exist valid reasons in particular circumstances to ignore a particular item, but the full implications must be understood and carefully weighed before choosing a different course |
| C3-10 | 3.3 Restrições | texto | rfc2119 | §5 | idem | registrado na norma | truly optional |
| C3-11 | 3.4 Aceite | texto | scrum-guide-2020 | Commitment: Definition of Done | Scrum Guide, 2020 | registrado na norma | a formal description of the state of the Increment when it meets the quality measures required for the product |
| C3-12 | 3.4 Aceite | texto | scrum-guide-2020 | Commitment: Definition of Done | idem | registrado na norma | If a Product Backlog Item does not meet the Definition of Done, it cannot be released or even presented at the Sprint Review |
| C3-13 | 3.4 Aceite | texto | anthropic-evals | Combinar cedo | 09/01/2026 | registrado na documentação | Early on, product requirements naturally translate into test cases. Wait too long and you're reverse-engineering success criteria from a live system. |
| C3-14 | 3.4 Aceite | texto | nasa-se | Apêndice C | idem | registrado na norma | Are the requirements free of unverifiable terms |
| C3-15 | 3.4 Aceite | texto | nasa-se | Apêndice C | idem | registrado na norma | All requirements should be stated in a fashion and with enough information that it will be possible to verify the requirement after the end product is implemented |
| C3-16 | 3.4 Aceite | texto | nasa-se | §4.1, tabela de atributos | idem | registrado na norma | Captures the method of verification (test, inspection, analysis, demonstration) |
| C3-17 | 3.4 Aceite | texto | anthropic-evals | Tarefas iniciais | idem | registrado na documentação | 20-50 simple tasks drawn from real failures is a great start |
| C3-18 | 3.4 Aceite | texto | anthropic-evals | Conclusão | idem | registrado na documentação | Define unambiguous, robust success criteria |
| C3-19 | 3.5 Escolha do uso de IA | texto | anthropic-agents | Introdução | 19/12/2024 | registrado na documentação | finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all |
| C3-20 | 3.5 Escolha do uso de IA | texto | anthropic-agents | Padrões | idem | registrado na documentação | only when it demonstrably improves outcomes |
| C3-21 | 3.6 Contratos e decomposição | texto | nasa-se | §4.1, tabela de atributos | idem | registrado na norma | Person or group responsible for writing, managing, and/or approving changes to this requirement |
| C3-22 | 3.6 Contratos e decomposição | texto | nasa-se | §4.1, quadro Rationale | idem | registrado na norma | If a requirement was written assuming the completion of a technology development program or a successful technology mission, the assumption should be documented |
| C3-23 | 3.6 Contratos e decomposição | texto | nist-ai-rmf | MAP 1.1 | idem | registrado na norma | assumptions and related limitations about AI system purposes, uses, and risks |
| C3-24 | 3.6 Contratos e decomposição | texto | nasa-se | Apêndice C | idem | registrado na norma | Are all external interfaces clearly defined |
| C3-25 | 3.4 Aceite | texto | anthropic-evals | Conclusão | Anthropic, 09/01/2026 | registrado na documentação | Source realistic tasks from the failures you see. |

## 3. Resultado da conferência

```
python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-capitulo-3-2026-11-13.md --textos /tmp/cap3-fontes/txt --projeto .
```

Saída registrada em 13/11/2026: 24 trechos, 24 aprovados, 0 reprovados. A pasta `/tmp` não é permanente; para reconferir, baixar as fontes pelo procedimento da seção 1.

## 4. Lacunas e ressalvas

- **NASA, NIST e Scrum:** lidos só nos trechos citados, em cópia baixada em 13/11/2026. O guia não afirma conformidade com nenhuma das três.
- **RFC 2119:** vale para documentos da IETF; o guia usa as três palavras como vocabulário, não como norma aplicável à especificação do projeto.
- **Anthropic, *Building effective agents*:** a página avisa que parte das ferramentas mudou desde a publicação; as frases citadas são sobre desenho, e não sobre ferramentas específicas.
- **Nielsen Norman Group:** a data de publicação (03/10/2025) consta na página; o conteúdo não foi comparado com versões anteriores.
- **NIST MAP 1.1:** o PDF hifeniza “contextspecific” na quebra de linha; o guia grafa “context-specific”. O trecho citado no pacote é o contíguo, para a conferência automática.
- **NASA §4.1.1.2.3:** a frase sobre partes interessadas atravessa uma quebra de página; o pacote cita o trecho contíguo.
- **Não verificado:** número de páginas dos PDFs normativos; existência de versão mais nova do NIST AI RMF; segunda leitura independente dos trechos por outra pessoa.
- **Exemplos da Aurora Educação:** situação construída para o livro; nenhum dado real, de aluno ou de escola, foi usado.

Assinatura: deepseek - conta não verificada, 13/11/2026.
