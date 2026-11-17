# Changelog: reestruturação do capítulo 2 em partes curtas (13/11/2026)

Autoria: claude - pessoal. Projeto sem Git. Pedido do operador em 13/11/2026: estruturar o capítulo 2 como o capítulo 1, depois `/revisar` e `/handoff`.

## 1. O que mudou

- **Capítulo 2 reestruturado:** de 6 unidades longas para **20 partes curtas** (2.1a a 2.6d), no molde do capítulo 1: resumo de 3 linhas, analogia, texto, pergunta de múltipla escolha, ponto de retomada, notas de fonte; "Fontes da unidade" na última parte de cada unidade (só *Ler* e *Aprofundar*; sem vídeo conferido).
- **Partes por unidade:** 2.1 (a peças, b três formas de acesso, c caminho do pedido); 2.2 (a pedido e resposta, b sem memória, c como terminou); 2.3 (a dois tempos, b streaming, c quando falha); 2.4 (a limites e classes de erro, b quando repetir, c repetir sem duplicar); 2.5 (a onde mora o estado, b o que guardar, c ordem de registro e retomada, **d registros: nova**); 2.6 (a muitos pedidos, b fila/limite/recusa/disjuntor, c sobrecarga e tentativas, **d pedidos que demoram: nova**).
- **Questões de fechamento:** 5 → 6 (duas fáceis, três médias, uma difícil); nova questão sobre pedidos longos. Mais 20 perguntas de parte. Letras corretas: 7/6/6/7 (A a D). A alternativa correta é a mais longa em 6 de 26 (verificado por script).
- **Imagens:** 4 molduras com `role="img"` e `aria-label` (2.1a, 2.3b, 2.4c, 2.6b), sem geração, conforme a regra fixa.
- **Fontes reabertas em 13/11/2026** (pacote: `pacote-de-fontes-capitulo-2-reestruturacao-2026-11-13.md`). Correções: citação de "Thinking" trocada por frase verificada; NVIDIA trocada para frases do corpo do artigo; Stripe com "For API v1"; links da OpenAI para `developers.openai.com`; AWS para o endereço do Builder Center; datas "15/10/2026" → "13/11/2026" onde a página foi reaberta; "documentação prevê identificador não encontrado" (OpenAI) retirada, por não confirmada.
- **Remissões a "módulo N" removidas** do capítulo 2 (viraram "mais adiante no guia").
- **Mantido por decisão pendente do operador:** o antipadrão da "fila distribuída", apoiado só nas diretrizes locais do autor (2.6c), com ressalva.
- **Sumário, introdução, glossário e referências** ajustados: âncoras `#unidade-2-Na`; "Nos capítulos 1 e 2"; novos termos (impressão digital, processamento em segundo plano, trava); "processamento em lote" passou de 2.3 para 2.6; referências com URLs e datas novas e OpenTelemetry.
- **Páginas lógicas:** 37 → 51. **PDF:** 143 → 178 páginas A4.

## 2. Arquivos

- Alterados: `guia-engenharia-llms.html`, `guia-engenharia-llms.pdf`, `CLAUDE.md`, `requisitos-de-formato-html-do-material.md` (§8).
- Novos: `pacote-de-fontes-capitulo-2-reestruturacao-2026-11-13.md`, este changelog, `handoff-reestruturacao-capitulo-2-2026-11-13.md`.
- Backup: `arquivo/antes-reestruturacao-capitulo-2-2026-11-13/` (HTML `137f8cfa517197e3`, PDF `577978b2fd3736b0`).
- Método de geração: partes escritas em dados e renderizadas por script fora do projeto (`/tmp/ch2-build`, não guardado); o resultado está no HTML.

## 3. Validações executadas

- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: 16 OK, 0 FALHA (55 questões, 51 páginas numeradas).
- Citações em inglês do capítulo 2 (80) cruzadas por script com o pacote e com os relatórios dos agentes: nenhuma sem apoio.
- PDF gerado por Chrome headless, 178 páginas A4; conferidas em PNG as páginas 85, 96, 99, 123, 146 e 155 (gabarito impresso abaixo da questão: visto na 155).
- Não executado: reflow em 320 px, impressão em papel, leitor de tela, aparelhos reais; segunda leitura independente das citações; revisão do operador sobre o conteúdo.

## 4. Pendências

1. Operador lê o capítulo 2 e veta ou ajusta.
2. Decidir sobre a "fila distribuída" (2.6c) e sobre fontes didáticas além das oficiais (curso ou vídeo conferido).
3. Reconferir por segunda leitura as citações antes de publicar; pendências de fonte no pacote, seção 4.
4. Imagens: última etapa, depois do texto aprovado.

claude - pessoal
