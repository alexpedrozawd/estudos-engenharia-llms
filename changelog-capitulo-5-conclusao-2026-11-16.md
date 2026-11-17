# Changelog — capítulo 5 escrito por inteiro, 16/11/2026

Autoria: claude - pessoal (Sonnet 5.5 High, painel). Autorização do operador em 16/11/2026: aprovou a unidade 5.1 e mandou escrever o capítulo inteiro, sem criar imagens (só molduras). Plano: `planejamento-capitulo-5-avaliacao-e-experimentacao.md`. Continua `changelog-capitulo-5-bloco-2-2026-11-16.md`.

## Feito
- Backup anterior: `arquivo/antes-capitulo-5-2026-11-16/` (HTML `bdb34977877270ed`, PDF `1d1dfb567fb3e5db`), feito antes da primeira edição do capítulo 5.
- Partes 5.2a a 5.6d (17 partes), com pergunta de parte em cada uma; gabaritos das perguntas de parte: 5.1 B, D, A; 5.2 C, A, D; 5.3 B, A, C; 5.4 D, B, C, A; 5.5 B, D, A; 5.6 C, B, D, A.
- Seis questões do capítulo (fácil, fácil, média, média, média, difícil), gabarito D, B, A, D, C, B (diferente dos capítulos 1 a 4).
- Abertura e sumário com os links das seis unidades e das questões; 25 termos novos no glossário (193 no total); referências com as cinco fontes do capítulo 5; "capítulos 1 a 5" na introdução e na abertura das referências.
- Navegação: 5.1c → 5.2a (corrigido o provisório); questões do capítulo 5 → glossário; páginas lógicas 94 a 117 (abertura 94, 5.1a 95 … 5.6d 114, questões 115, glossário 116, referências 117).
- Pacote de fontes: 47 trechos (C5-45 a C5-47 acrescentados na escrita), 47 aprovados.
- Três molduras de imagem (5.1a, 5.4a, 5.6b), só `role="img"` + `aria-label`. Nenhuma imagem gerada.
- Blocos não executáveis: critérios (5.1c), caso (5.2b), rubrica de juiz (5.4c), registro de regressão (5.5c), decisão registrada (5.6d), todos com até 12 linhas e `data-executavel="false"`.

## Validação
- `validar-guia.py`: 16 OK, 0 FALHA; 117 páginas lógicas em sequência.
- Navegação conferida por script: anterior e seguinte de cada uma das 22 seções do capítulo coincidem com a ordem do documento; tags balanceadas.
- Corpo das partes: de 380 a 508 palavras (abertura 419; questões 522).
- PDF regenerado (Chrome for Testing 158): 379 páginas A4; capítulo 5 a partir da página física 296; gabarito impresso presente nas seis questões; única página curta é a última, de referências.
- Conferência de fontes: todas as aspas de fonte vêm dos 47 trechos aprovados; a aplicação ao assistente da Aurora e as tabelas estão marcadas como proposta didática; números das tabelas são fictícios e coerentes entre 5.3c, 5.5a, 5.5c e 5.6d (v1 12 de 16; v2 14 de 16).
- Não executado: reflow em 320 px, aparelhos reais, segunda leitura (Sonnet 5.5 High em sessão separada, decisão do operador).

## Limites conhecidos
- Quem escreveu também revisou; a segunda leitura segue pendente.
- Três afirmações do guia não têm trecho literal e estão marcadas como proposta didática: separar casos de ajuste e reservados; benchmark público não substitui avaliação própria; escolha entre as duas páginas da Anthropic (volume versus qualidade).
- A frase da 5.5b sobre incluir no conjunto de regressão o caso corrigido após falha em produção é prática comum, não trecho de fonte.

Hashes finais: HTML `820e006c24e4a899`; PDF `a2be776b9f931796`; pacote de fontes `15c8cecd29d6712c`.

claude - pessoal, 16/11/2026
