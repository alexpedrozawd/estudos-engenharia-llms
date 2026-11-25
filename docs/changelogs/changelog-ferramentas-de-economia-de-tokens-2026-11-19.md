# Changelog: ferramentas de economia de tokens e teste do LLM local (19/11/2026)

Autoria: claude - pessoal. Pedido do operador: reduzir o gasto das LLMs de fronteira na criação, edição e manutenção do guia (HTML, PDF, documentos e pesquisa em fontes) sem perder qualidade, avaliando o Qwen 3.8 27B Q3 e o Gemma 4 locais. Planejamento revisado com `/revisar` antes da implementação. `guia-engenharia-llms.html` (`19a020013721c5a5`) e `guia-engenharia-llms.pdf` (`10ff8c03dd8dfe83`) não foram alterados.

## O que entrou

- `ferramentas/guia.py`: `mapa`, `contar`, `verificar`, `pdf`, `fechar`. Reaproveita `renumerar-paginas.py`, `validar-guia.py` e `executar-trechos-de-codigo.py` e acrescenta checagens que não existiam (ids únicos, `<dfn>` sem repetição exata, glossário sem repetição, sumário com capítulos, questões e primeira parte de cada unidade, toda tabela em `.rolagem`, um gabarito por questão). O PDF sai em arquivo temporário, conferido com `pdfinfo`; só substitui o original com `--substituir --motivo`, depois de copiar o atual para `arquivo/antes-<motivo>-<data>/`. Chrome: `chromium-1254` do Playwright (ou `--chrome`/`GUIA_CHROME`).
- `ferramentas/fontes.py`: manifesto (212 entradas, 196 chaves, 41 domínios, lidas das tabelas dos pacotes), download só https e só dos domínios do manifesto (redirecionamento para fora é bloqueado; sem cookies; agente de usuário genérico; limite de 25 MB), extração (HTML, RFC, MD e PDF via `pdftotext`), `achar` e `conferir`.
- `ferramentas/llm-local.py`, `benchmark-llm-local.py`, `casos-llm-local.json`: cliente do Ollama só em `127.0.0.1`, uma chamada com esquema JSON, temperatura 0, recusa a GPU ocupada, log sem o texto dos prompts; teste de triagem com 36 casos e 18 controles negativos.
- `.gitignore`: `cache-fontes/` (114 MB de fontes baixadas) e `rascunho-local/`.
- `protocolo-de-economia-de-tokens-entre-sessoes.md`: seções 8 (ferramentas) e 9 (decisão sobre o LLM local).

## Testes (38, todos passam)

- `testar-ferramentas.py` (14): contagens conferidas contra contagem independente (regex, `pdfinfo`); 8 mutações em cópia do guia (id duplicado, gabarito removido, link quebrado, página fora de ordem, `<dfn>` repetido, tabela sem rolagem, unidade fora do sumário) reprovam com a mensagem esperada e a cópia sem defeito passa; idempotência; HTML e PDF com o mesmo hash antes e depois; PDF com 534 páginas como o versionado; `--substituir` exige motivo e faz a cópia.
- `testar-fontes.py` (10): servidor HTTP local; recusa http fora do localhost, domínio fora da lista, redirecionamento para fora e resposta acima do limite; a requisição não leva cookie, `Authorization`, `Referer` nem dados do projeto; manifesto igual à contagem independente; cache ignorado pelo Git; `achar` com linha certa, sem acento/caixa e sem inventar candidato.
- `testar-llm-local.py` (14): carga útil determinística; log sem prompt; recusa de GPU ocupada sem chamar o modelo; `OLLAMA_HOST` ignorado; JSON inválido registrado; no corpus real, o gabarito aparece nas fontes dos 36 casos e os 18 controles negativos não têm o trecho da afirmação na fonte sorteada.
- Defeitos que os testes pegaram e foram corrigidos: `achar` apontava o início da janela e não a linha do termo; checagem de dfn sem diferenciar caixa acusava `cliente`/`Cliente` (2.1a genérico e 10.6a do MCP, sentidos diferentes); a checagem de sumário supunha todas as partes listadas, mas o sumário lista só a primeira de cada unidade; PDF com `-layout` embaralhava colunas (passou de 564 para 579 trechos reconfirmados ao trocar).

## Medições

- Fechamento: 4.393 bytes de saída com comandos soltos contra 1.115 bytes do `guia.py fechar --pdf` (que ainda faz mais checagens). a geração do PDF leva cerca de 6 s.
- Fontes do Capítulo 16: 300.406 bytes de texto que a fronteira leria contra 123 bytes de saída do script.
- Download: 171 de 196 fontes (cerca de 3 min). 25 falharam: 23 com 403 (Anthropic, vLLM, NIST), 1 com 400 (Azure), 1 por usar http (`cormack-rrf`). Não se disfarça o agente de usuário.
- Conferência: 579 de 754 trechos dos pacotes dos Caps. 6–16 e da expansão do Grupo A reconfirmados; 167 reprovados por fonte não baixada e 8 com a fonte baixada e trecho não achado (`openai-model-selection` 6, `openai-your-data` 1, `gemma-4-31b` 1): pedem conferência manual de vigência (a página pode ter mudado ou depender de JavaScript).
- LLM local (54 casos por modelo): os três empataram com o script lexical (97% de acerto@3), com 0 casos exclusivos e falso aceite de 2/18 (11%) nos mesmos dois controles (`FI-01~HW-08`, `HW-08~FI-01`, fontes da Anthropic com assunto próximo). Limite G2 (≤ 5%) reprovado nos três. Bytes lidos: 740–860 contra 4.403 dos 10 candidatos e 1.546 do top-3 do script.

## Decisões e limites

- Divergência com o Pipeline Triangular da diretriz global: neste projeto o LLM local não entra no fluxo (reprovado no portão fixado antes; sem ganho de acerto sobre o script). A diretriz global não foi alterada. Reabrir só com tarefa nova, verificador por código e novo portão.
- Limites do teste: as palavras-chave em inglês foram escritas por quem conhecia o gabarito (favorece o script); 36 casos, uma tarefa, uma repetição por caso, temperatura 0 e semente fixa (o plano previa 3 repetições; não repeti e não verifiquei o determinismo das respostas).
- Economia da fronteira medida em bytes de saída; não há tokenizador no ambiente, então não é medida exata de tokens.
- Baixos da revisão tratados: scripts chamam subprocessos com `sys.executable` e `-I`; Chrome fixado em `chromium-1254` por padrão.
- Não feito: `vigencia` automática das 275 URLs (depende da decisão sobre o L7 do `plano-de-lacunas-para-nota-10-2026-11-19.md`); tarefa T3 (pré-lint), dispensada porque o local não passou na triagem; as 25 fontes bloqueadas seguem pela busca da fronteira.

claude - pessoal
