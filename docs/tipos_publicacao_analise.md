# Analise dos Tipos de Publicacao — Corpus QML + Supply Chain/Inventory

Data: 2026-03-31 (analise original com 2.471 artigos)
Atualizado: 2026-04-11 (strings #10-#14 removidas — corpus reduzido; re-executar scripts para novos totais)
Fonte: `data/artigos_unicos.csv`

---

## 1. Distribuicao por Tipo de Publicacao

| Tipo de Publicacao | Qtd | % do Corpus |
|--------------------|----:|------------:|
| journal article | 1.504 | 60,9% |
| preprint | 345 | 14,0% |
| conference proceedings article | 227 | 9,2% |
| book chapter | 148 | 6,0% |
| report | 107 | 4,3% |
| book | 75 | 3,0% |
| dissertation | 27 | 1,1% |
| other | 19 | 0,8% |
| NaN (sem tipo) | 4 | 0,2% |
| dataset | 3 | 0,1% |
| journal issue | 3 | 0,1% |
| component | 3 | 0,1% |
| editorial | 3 | 0,1% |
| news | 2 | 0,1% |
| conference proceedings | 1 | 0,0% |

---

## 2. Descricao de Cada Tipo

### journal article (1.504 artigos)
Artigo publicado em periodico cientifico com revisao por pares (peer review). E o tipo mais consolidado da comunicacao academica — passou por avaliacao de especialistas antes da publicacao. Representa o padrao-ouro em revisoes sistematicas.

### preprint (345 artigos)
Manuscrito depositado em repositorios abertos (arXiv, SSRN, medRxiv) **antes** da revisao por pares. Comum em areas computacionais e de fisica, onde a velocidade de disseminacao e valorizada. Conteudo nao passou por validacao formal, mas frequentemente contem resultados originais que serao publicados posteriormente como journal articles. Em campos emergentes como QML, preprints representam o estado da arte mais recente.

### conference proceedings article (227 artigos)
Artigo completo apresentado e publicado nos anais de uma conferencia cientifica. Passa por revisao (geralmente menos rigorosa que periodicos), mas em areas como Ciencia da Computacao e IA, conferencias de alto impacto (NeurIPS, ICML, IEEE) tem relevancia equivalente ou superior a periodicos. Contem metodologia e resultados completos.

### book chapter (148 artigos)
Capitulo individual dentro de um livro editado ou coletanea. Pode ser uma revisao do estado da arte, um tutorial aprofundado ou uma contribuicao original sobre um topico especifico. A qualidade varia — alguns sao revisados por pares, outros sao convidados pelo editor.

### report (107 artigos)
Relatorio tecnico ou de pesquisa publicado por instituicoes (universidades, laboratorios governamentais, organizacoes internacionais). Nao passa necessariamente por revisao por pares, mas pode conter dados primarios e analises relevantes. Inclui technical reports, white papers e working papers.

### book (75 artigos)
Livro completo (monografia ou obra editada). Pode ser uma referencia fundamental do campo, um livro-texto ou uma compilacao. Menos comum como fonte primaria em revisoes sistematicas, mas pode conter capitulos relevantes.

### dissertation (27 artigos)
Tese de doutorado ou dissertacao de mestrado. Trabalho academico extenso, avaliado por banca examinadora. Contem revisao de literatura, metodologia detalhada e resultados originais. Pode ser uma fonte rica de dados primarios nao publicados em outros formatos.

### other (19 artigos)
Categoria residual para publicacoes que nao se enquadram nas demais. Pode incluir posters, notas tecnicas, working papers ou documentos mal classificados na base. Requer avaliacao individual.

### dataset (3 artigos)
Publicacao de um conjunto de dados (dataset) com descricao e documentacao. Nao contem analise ou resultados cientificos — o foco e disponibilizar dados para reuso.

### journal issue (3 artigos)
Registro de uma edicao completa de um periodico (o volume/numero em si), nao de um artigo individual. Trata-se de metadado da base, nao de conteudo academico independente.

### component (3 artigos)
Componente suplementar de outra publicacao — figuras, tabelas, materiais complementares ou apendices publicados separadamente. Nao constitui contribuicao independente.

### editorial (3 artigos)
Texto opinativo ou introdutorio escrito pelo editor do periodico. Nao apresenta pesquisa original nem metodologia. Serve como comentario ou nota da edicao.

### news (2 artigos)
Noticia ou reportagem sobre um tema cientifico. Sem metodologia, sem revisao por pares. Conteudo jornalistico, nao academico.

### conference proceedings (1 artigo)
Registro dos anais de uma conferencia como um todo (o volume completo), nao um artigo individual. Similar a "journal issue" — e metadado da base.

### NaN / sem tipo (4 artigos)
Registros sem classificacao de tipo na base Lens.org. Requer verificacao manual.

---

## 3. Classificacao de Relevancia para Triagem

### Alta relevancia — Manter (incluir)

| Tipo | Justificativa |
|------|---------------|
| **journal article** | Padrao-ouro: revisado por pares, metodologia validada |
| **conference proceedings article** | Em Ciencia da Computacao/IA, conferencias de alto impacto sao tao relevantes quanto periodicos |
| **preprint** | Essencial em campo emergente como QML; contem resultados mais recentes, frequentemente a unica fonte disponivel para trabalhos de ponta |
| **dissertation** | Pesquisa original extensa com metodologia detalhada |

### Media relevancia — Manter com cautela (incluir, avaliar individualmente)

| Tipo | Justificativa |
|------|---------------|
| **book chapter** | Pode conter revisoes uteis ou contribuicoes originais; qualidade variavel |
| **report** | Relatorios tecnicos de laboratorios e instituicoes podem conter dados primarios relevantes |
| **book** | Referencia util, mas raramente fonte primaria para revisao sistematica |
| **other** | Categoria ambigua — requer verificacao manual caso a caso |
| **NaN (sem tipo)** | Sem classificacao — verificar manualmente |

### Baixa relevancia — Excluir (CE-5)

| Tipo | Justificativa |
|------|---------------|
| **editorial** | Opiniao do editor, sem pesquisa original nem metodologia |
| **news** | Conteudo jornalistico, sem rigor cientifico |
| **dataset** | Publicacao de dados, sem analise ou contribuicao metodologica |
| **component** | Material suplementar de outra publicacao, nao independente |
| **journal issue** | Metadado da base, nao conteudo academico |
| **conference proceedings** | Registro do volume dos anais, nao artigo individual |

---

## 4. Recomendacao para o Criterio CE-5

Com base nesta analise, a lista de tipos excluidos pelo criterio CE-5 do protocolo de triagem deve incluir:

```
editorial, news, dataset, component, journal issue, conference proceedings
```

**Total de artigos afetados**: 15 artigos (0,6% do corpus)

> **Nota**: O tipo `conference proceedings` (1 artigo) foi adicionado em relacao ao protocolo original. Trata-se do registro dos anais como volume, nao de um artigo individual — diferente de `conference proceedings article`, que e o artigo completo e deve ser **mantido**.

---

## 5. Resumo Visual

```
MANTER (2.375 artigos — 96,1%)
  ├── journal article .............. 1.504  ████████████████████████████
  ├── preprint .....................   345  ██████
  ├── conference proceedings article  227  ████
  ├── book chapter .................   148  ██
  ├── report .......................   107  █
  ├── book .........................    75  █
  ├── dissertation .................    27  ▏
  ├── other ........................    19  ▏
  └── NaN ..........................     4  ▏

EXCLUIR — CE-5 (15 artigos — 0,6%)
  ├── editorial ....................     3  ▏
  ├── dataset ......................     3  ▏
  ├── journal issue ................     3  ▏
  ├── component ....................     3  ▏
  ├── news .........................     2  ▏
  └── conference proceedings .......     1  ▏
```

---

*Analise gerada a partir de `data/artigos_unicos.csv` com 2.471 artigos unicos.*
*Referencia: protocolo de triagem em `docs/protocolo_triagem.md`*
