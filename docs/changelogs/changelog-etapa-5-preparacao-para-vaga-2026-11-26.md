# Changelog — Etapa 5: preparação para vaga (26/11/2026)

Autoria: claude - pessoal. Etapa 5 do [plano de prontidão](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md), com as quatro decisões recomendadas aprovadas pelo operador: pasta `docs/preparacao-para-vaga/` em `.md`, nova coleta com termos "pleno", lista dos 10 casos e `laboratorios/projeto_integrador/` como projeto final. HTML, PDF, código, testes e `laboratorios/` inalterados.

## Entregas

1. **Mapa de vagas reconferido** ([seção nova](../historico/mapa-de-vagas-linkedin-brasil-2026-11-25.md#reconferência-em-26112026-55-vagas)). Mesma rota pública do LinkedIn, sem login, com os `5` termos de 25/11, mais `Engenheiro de IA Pleno` e `AI Engineer Pleno`, duas páginas por termo.
   - Das `29` vagas de 25/11, `28` seguem abertas (a da Claro Brasil foi encerrada).
   - Após tirar repetições e vagas sem foco em LLM, a amostra ficou com `55` vagas, sendo `29` novas.
   - Pelo título, `26` são sênior, lead ou especialista, `2` pleno e `5` júnior.
   - A regra de 1/3 foi reaplicada, e nenhum requisito sem prática passou do corte.
   - Os dados brutos e os scripts ficaram em `rascunho-local/vagas-linkedin-2026-11-26/`, fora do Git.
2. **Pacote de fontes de bancos vetoriais** ([pacote-de-fontes-bancos-vetoriais-2026-11-26.md](../fontes/pacote-de-fontes-bancos-vetoriais-2026-11-26.md)): `10` páginas oficiais (pgvector, FAISS, Pinecone e Weaviate) e `22` trechos literais aprovados em `conferir-trechos.py`. O guia não citava esses produtos.
3. **[Casos de system design](../preparacao-para-vaga/casos-de-system-design.md):** `10` casos com rubrica comum (8 critérios, de 0 a 16), roteiro de 45 minutos, perguntas de esclarecimento, arquitetura de referência, trade-offs, armadilhas e números dos projetos. O caso 1 compara `pgvector`, Pinecone, Weaviate e FAISS e faz a conta de memória do HNSW.
4. **[Bloco de entrevista](../preparacao-para-vaga/entrevista-comunicacao-e-diagnostico.md):** três roteiros (limites da IA para quem não é técnico, pedido vago → especificação e diagnóstico de falhas não determinísticas), com `6` casos reais dos projetos.
5. **[Guia de portfólio](../preparacao-para-vaga/guia-de-portfolio.md):** resumo de 30 segundos e de 2 minutos, decisões, números com origem, limites e perguntas prováveis para P02, P06, P08 e o projeto final.

## Achados

- **Médio, corrigido na auditoria:** o bloco de entrevista dizia que "a busca" do P02 acertou todas as `28` perguntas. Só a variante vetorial teve `recall@4 = 1,0`; a frase passou a citar a busca vetorial.
- **Registrado, sem correção nesta etapa:** o P02 usa HNSW com filtro de ACL no `WHERE`, sem varredura iterativa. Segundo a documentação do `pgvector`, o filtro roda depois da varredura do índice e pode devolver menos de `k` trechos em escala. Não há vazamento, porque o filtro continua aplicado. Com `275` trechos, o efeito não pesa. O limite está declarado no caso 1 e no guia de portfólio.

## Validação

- `conferir-trechos.py` no pacote novo: `22` aprovados e `0` reprovados. `fontes.py vigencia`: `10` atuais.
- Links e âncoras dos `6` arquivos novos ou alterados conferidos por script.
- Números conferidos contra `laboratorios-mercado/execucoes/` e READMEs dos projetos.
- Suítes no fechamento do commit.

## Pendências

- Revisão humana da Etapa 3 (P04, P02 e P07), que só o operador faz.
- Etapa 6, opcional (a 6b, deploy em nuvem, exige autorização), e Etapa 7.
