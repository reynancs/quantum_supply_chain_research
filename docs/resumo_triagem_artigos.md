# Resumo da Etapa 2 — Triagem Automatizada de Artigos

**Projeto**: Quantum Machine Learning (QML) Aplicado à Previsão e Controle de Inventário em Logística
**Programa**: Mestrado Profissional em Gestão de Tecnologia e Inovação — SENAI CIMATEC
**Data da triagem**: Abril/2026 (última atualização: 2026-04-14)
**Scripts de execução**: `src/triagem_artigos.py`, `src/classificar_problema.py`
**Protocolo completo**: `docs/protocolo_triagem.md`

---

## 1. Contexto e Objetivo

Esta etapa constitui a Fase 2 do projeto de pesquisa, sucedendo a pesquisa bibliográfica e deduplicação (Etapa 1). O objetivo foi classificar sistematicamente cada artigo do corpus como **elegível** ou **excluído** para a revisão de texto completo, seguindo o protocolo PRISMA-ScR (Preferred Reporting Items for Systematic Reviews — extension for Scoping Reviews).

A triagem foi integralmente automatizada por meio de critérios de exclusão baseados em palavras-chave com regex e word boundaries, aplicados em duas fases sequenciais. Todos os artigos são mantidos no dataset — nenhum é removido, apenas classificado — garantindo rastreabilidade e reprodutibilidade.

---

## 2. Pré-processamento: Remoção das Strings 10–14

### 2.1 Problema Identificado

Durante a análise dos resultados iniciais da triagem (com 2.471 artigos), foi identificado que **73% dos artigos elegíveis eram falsos positivos** — artigos que utilizam QML mas aplicado a domínios completamente fora do escopo (clima, finanças, saúde, energia, física pura etc.).

A análise de causa raiz revelou que as **strings de busca #10 a #14** (prioridade Média) eram a principal fonte de ruído:

| # | String de Busca | Artigos |
|---|----------------|---------|
| 10 | "Quantum Machine Learning" AND "Time Series" | 264 |
| 11 | "Quantum Machine Learning" AND "Forecasting" | 363 |
| 12 | "Quantum Neural Network" AND "Forecasting" | 266 |
| 13 | "Variational Quantum" AND "Forecasting" | 176 |
| 14 | "Quantum Machine Learning" AND "Prediction" | 853 |

Essas strings combinam termos de QML com termos genéricos de previsão (Forecasting, Prediction, Time Series) **sem exigir nenhum termo de supply chain**, capturando indiscriminadamente artigos de qualquer domínio que aplique QML à previsão.

### 2.2 Análise de Precisão

Dos artigos exclusivos das strings 10–14 (não encontrados por nenhuma outra string 1–9):

| Métrica | Valor |
|---------|-------|
| Total de artigos exclusivos das strings 10–14 | 1.282 |
| Destes, elegíveis após triagem | 421 |
| Destes, com palavras-chave de supply chain | **7 (1,7%)** |
| Destes, com alta relevância para cadeia de suprimentos | **2 (0,5%)** |
| **Precisão das strings 10–14 para supply chain** | **1,7%** |

### 2.3 Decisão

As strings #10 a #14 foram **removidas do pipeline** de deduplicação e triagem. Justificativa:

- **Trata a causa raiz**: em vez de expandir indefinidamente os critérios de exclusão CE-3 para cobrir cada domínio que aplica QML a previsão, a remoção elimina a fonte de ruído
- **Perda mínima**: apenas 2 artigos de alta relevância em risco (0,5%), facilmente recuperáveis por revisão manual
- **Artigos retidos**: os 91 artigos encontrados simultaneamente por strings 1–9 **e** 10–14 são preservados, pois existem via strings 1–9

### 2.4 Impacto no Corpus

| Métrica | Antes | Depois |
|---------|-------|--------|
| Total bruto (com duplicatas) | 3.714 | 1.792 |
| Total único (sem duplicatas) | 2.471 | 1.231 |

---

## 3. Deduplicação Aprimorada

### 3.1 Deduplicação Cross-DOI por Título

A deduplicação original (Etapa 1) identificava duplicatas apenas por DOI e, para artigos sem DOI, por título normalizado. Isso deixava escapar artigos com **DOIs diferentes, mas mesmo título** — comum quando um preprint (arXiv) e a versão publicada em periódico recebem DOIs distintos.

Foi adicionada uma **Etapa 5 de deduplicação por título normalizado** (case-insensitive, espaços normalizados) aplicada a todo o corpus, independentemente de DOI.

### 3.2 Resultado

| Etapa de Deduplicação | Duplicatas Removidas |
|-----------------------|---------------------|
| Por DOI | 493 |
| Por título (sem DOI) | 0 |
| **Por título (cross-DOI)** | **68** |
| **Total** | **561** |

Corpus final após deduplicação: **1.231 artigos únicos**.

---

## 4. Processo de Triagem

### 4.1 Arquitetura

A triagem é implementada no script `src/triagem_artigos.py` e opera em duas fases sequenciais:

```
IDENTIFICAÇÃO
  1.231 artigos únicos
        |
        v
========================================
  FASE 1 — Triagem por Metadados
  (título + tipo de publicação + fields of study)
----------------------------------------
  CE-5: tipo de publicação não-substantivo
  CE-1: otimização quântica pura (sem ML)
  CE-3 (forte): domínio claramente fora de escopo no título
                (ignora safety net de "supply chain")
  CE-3: domínio fora de escopo
========================================
        |
  380 artigos incluídos
        |
        v
========================================
  FASE 2 — Triagem por Abstract
  (apenas abstract)
----------------------------------------
  CE-3: sem abstract + sem palavra-chave SC no título
  CE-1: otimização quântica pura (sem ML)
  CE-2: QML apenas como trabalho futuro
  CE-3: domínio fora de escopo
========================================
        |
        v
  261 artigos elegíveis para revisão
        |
        v
========================================
  CLASSIFICAÇÃO POR TIPO DE PROBLEMA
  (src/classificar_problema.py)
========================================
  Taxonomia com 13 categorias (backorder,
  demand forecasting, inventory, routing,
  scheduling, supplier, risk, sustainability,
  predictive maintenance, SC general,
  Industry 4.0, QML review, outros)
```

### 4.2 Critérios de Exclusão

| Código | Critério | Lógica de Matching | Fase |
|--------|----------|-------------------|------|
| **CE-1** | Otimização quântica pura sem ML (QAOA, quantum annealing, VQE sem treinamento/learning) | `tem_otimização E NÃO tem_ml` | Fase 1 (título + fields of study) + Fase 2 (abstract) |
| **CE-2** | QML mencionado apenas como trabalho futuro ou especulação | `tem_futuro E NÃO tem_experimento` | Fase 2 apenas |
| **CE-3** | Domínio fora de supply chain/logística | `tem_domínio_excluir E NÃO tem_domínio_manter` | Fase 1 (título + fields of study) + Fase 2 (abstract) |
| **CE-3 (forte)** | Título evidencia claramente outro domínio de pesquisa (blockchain, patent review, nanotechnology, digital health, biomedical, quantum cryptography, satellite communication, quantum communication, COVID, LNG, semiconductor manufacturing, ESG, vaccine, etc.) | `tem_domínio_excluir_forte` (sem safety net — não é revogado por "supply chain") | Fase 1 (título apenas) |
| **CE-5** | Tipo de publicação não-substantivo (editorial, news, dataset, book chapter, report, book, dissertation, other) | Comparação direta com lista de tipos | Fase 1 apenas |

### 4.3 Lógica de Duas Camadas (Safety Net)

Cada critério utiliza uma lógica de **duas camadas** para evitar exclusões indevidas:

- **Camada de exclusão**: palavras-chave que indicam escopo fora do tema
- **Camada de retenção (safety net)**: palavras-chave que "resgatam" o artigo se estiverem presentes

Exemplo para CE-3: um artigo com "healthcare" no abstract seria normalmente excluído, mas se também contiver "supply chain", é retido. Isso protege artigos que discutem supply chain em contexto de saúde (ex: cadeia de suprimentos de vacinas).

**Exceção — CE-3 (forte)**: após a revisão manual dos resultados, foi identificado que artigos fundamentalmente focados em outros domínios (ex: blockchain, patent review, nanotechnology) passavam pela triagem apenas por mencionarem "supply chain" de passagem. Para esses casos foi criada a regra **CE-3 (forte)**, aplicada **somente ao título na Fase 1**, que exclui sem revogação pela safety net. Exemplo: *"Quantum-Accelerated Blockchain Framework for Identifying Counterfeit Detection in Global Supply Chains"* — o título evidencia que o artigo é primariamente sobre blockchain, não sobre QML aplicado a SC, portanto é excluído por CE-3 (forte) mesmo contendo "supply chain".

### 4.4 Matching por Regex com Word Boundary

Todas as comparações utilizam:

- **Regex compilado** com `\b` (word boundary) para evitar matches parciais (ex: "rain" não faz match com "training")
- **Case-insensitive** (`re.IGNORECASE`)
- Cada lista de palavras-chave é pré-compilada uma única vez como padrões regex para performance

### 4.5 Campos Analisados por Fase

| Fase | Campos | Justificativa |
|------|--------|---------------|
| **Fase 1** | Title + Publication Type + Fields of Study | Metadados disponíveis para todos os artigos. Fields of Study (campo do Lens.org com áreas temáticas separadas por `;`) foi adicionado para melhorar a detecção de domínios fora de escopo |
| **Fase 2** | Abstract apenas | Evita redundância — o título já foi analisado na Fase 1. Apenas o abstract traz informação nova |

**Decisão de design**: na versão inicial, a Fase 2 combinava título + abstract. Isso foi identificado como redundante — se um artigo passou pela checagem de título na Fase 1, re-checar o título na Fase 2 não exclui nenhum artigo adicional.

### 4.6 Tratamento de Artigos sem Abstract

Artigos sem abstract recebem tratamento especial na Fase 2:

- **Se o título contém palavra-chave de supply chain** → incluído (preserva artigos possivelmente relevantes)
- **Se o título NÃO contém palavra-chave de supply chain** → excluído como CE-3 (sem informação suficiente para justificar inclusão)

Esta abordagem substitui a regra anterior de incluir automaticamente todos os artigos sem abstract, que permitia a passagem de conteúdo editorial irrelevante (ex: "NATIONAL SCIENCE FOUNDATION", "Table of Contents").

---

## 5. Palavras-chave dos Critérios de Exclusão

### 5.1 CE-1 — Otimização Quântica Pura

**Palavras de otimização** (17 termos): `qaoa`, `quantum approximate optimization`, `quantum annealing`, `adiabatic quantum`, `variational quantum eigensolver`, `vqe`, `ising model`, `ising formulation`, `maxcut`, `max-cut`, `max cut`, `combinatorial optimization`, `qubo`, `d-wave`, `quantum walk`, `grover search`, `grover's algorithm`, `quantum counting`, `quantum integer programming`

**Palavras de ML (safety net)** (27 termos): `quantum machine learning`, `quantum neural network`, `qnn`, `variational quantum circuit`, `vqc`, `parameterized quantum circuit`, `pqc`, `quantum kernel`, `quantum support vector`, `qsvm`, `quantum reservoir`, `quantum convolutional`, `quantum transfer learning`, `quantum classifier`, `quantum reinforcement learning`, `hybrid quantum-classical`, `quantum generative`, `quantum autoencoder`, `quantum boltzmann`, `quantum feature map`, `quantum embedding`, `machine learning`, `deep learning`, `neural network`, `classification`, `regression`, `training`, `supervised`, `unsupervised`, `forecasting`, `prediction`, `predictive`, `backorder`, `demand forecast`

### 5.2 CE-2 — QML Apenas como Trabalho Futuro

**Palavras de futuro** (13 termos): `future work`, `future research`, `future direction`, `could be applied`, `could be explored`, `potential application`, `potential of quantum`, `promising direction`, `promising avenue`, `remains to be explored`, `left for future`, `as a next step`, `we plan to`, `we intend to`

**Palavras de experimento (safety net)** (27 termos): `experiment`, `experimental result`, `we implement`, `we implemented`, `we propose and evaluate`, `we propose and test`, `we train`, `we trained`, `accuracy`, `precision`, `recall`, `f1`, `mean squared error`, `mse`, `rmse`, `mae`, `benchmark`, `benchmarked`, `dataset`, `data set`, `simulation result`, `simulated`, `our result`, `results show`, `results demonstrate`, `outperform`, `outperforms`, `tested on`, `evaluated on`, `quantum circuit`, `qiskit`, `pennylane`, `cirq`

### 5.3 CE-3 — Domínio Fora de Escopo

**Palavras de domínio excluído** (~210 termos após expansões de 2026-04-13 e 2026-04-14), organizadas por categoria:

| Categoria | Qtd. Termos | Exemplos |
|-----------|-----------|----------|
| Biomédico / Saúde | 35+ | `healthcare`, `drug discovery`, `cancer`, `diabetes`, `vaccine`, `cardiovascular`, `biomedical`, `digital health`, `telemedicine` |
| Finanças / Portfolio | 20 | `stock market`, `financial trading`, `credit scoring`, `fraud detection`, `capital market`, `loan risk`, `inflation` |
| Telecomunicações / Wireless | 14 | `6g`, `antenna design`, `beamforming`, `spectrum allocation`, `telecommunication`, `satellite communication`, `quantum communication` |
| Física pura / Ciência de Materiais | 24+ | `graphene`, `condensed matter`, `Rydberg`, `gravitational wave`, `hamiltonian framework`, `nonadiabatic dynamics`, `wave-particle duality` |
| Energia / Gás / Infraestrutura | 20+ | `solar energy`, `wind power`, `power grid`, `battery degradation`, `microgrid`, `LNG`, `liquefied natural gas`, `mobile power plant`, `low-carbon energy`, `nuclear fusion`, `tokamak` |
| Clima / Meteorologia | 12+ | `weather forecast`, `weather`, `rainfall`, `earthquake`, `drought` |
| Agricultura | 7 | `crop yield`, `soil moisture`, `agricultural`, `Ecology` |
| Imagem / Visão / NLP | 14 | `face recognition`, `image classification`, `remote sensing`, `sentiment analysis` |
| Cibersegurança / Criptografia | 13 | `intrusion detection`, `malware`, `quantum key distribution`, `post-quantum cryptography`, `Blockchain`, `quantum cryptography` |
| Patentes / Reviews de QML | 4 | `patent`, `patent review`, `patent analysis`, `patent landscape` |
| Nanotecnologia | 8 | `nanotechnology`, `nanotech`, `nanomaterial`, `nanostructure`, `nanoparticle`, `nanotube`, `nanofluid` |
| Farmácia / Dispensação | 7 | `pharmacy`, `pharmaceutical dispensing`, `medication dispensing`, `central fill`, `robotic dispensing`, `fnirs`, `fear detection` |
| Espaço / Aeroespacial | 4 | `space mission`, `space exploration`, `aerospace`, `satellite communication` |
| COVID / Pandemia | 3 | `covid-19`, `covid`, `pandemic impact` |
| Manutenção veicular | 3 | `vehicle break down`, `vehicle breakdown`, `breakdown prediction` |
| Política econômica / Comércio | 5 | `export control`, `export controls`, `trade sanction`, `economic resilience`, `corporate resilience` |
| Semicondutores | 2 | `semiconductor manufacturing`, `semiconductor industry` |
| Gestão / Negócios genéricos | 5 | `innovation ecosystem`, `human-centric economy`, `ESG goals`, `ESG reporting`, `augmented reality` |
| Jogos / Conteúdo procedural | 2 | `level generation`, `procedural content` |
| Engenharia de software | 2 | `microservice`, `microservices` |
| Baterias específicas | 3 | `lifepo4`, `battery lifetime`, `lithium iron phosphate` |
| QML genérico sem âncora de SC | 4 | `non-trivial classification`, `quantum kernel framework`, `shallow entangled circuits`, `ibm devices` |
| Transportes (não-logística) | 5 | `mobility`, `Public transport`, `Smart City`, `traffic prediction` |
| Social / Humanidades / Editorial | 7 | `Sociology`, `psychology`, `education`, `sociotechnical`, `women in quantum` |
| Conteúdo editorial irrelevante | 8 | `Table of Contents`, `National Science Foundation`, `Notes from the Editor` |
| Outros | 8 | `Ethnography`, `football club`, `quantum chemistry`, `hearing protector` |

**Palavras de domínio manter (safety net)** (16 termos): `supply chain`, `logistics`, `inventory`, `warehouse`, `demand forecast`, `backorder`, `procurement`, `freight`, `distribution network`, `supplier`, `replenishment`, `order fulfillment`, `last mile`, `transportation planning`, `production planning`, `manufacturing`

**Palavras de domínio excluir forte (CE-3 forte — aplicadas apenas ao título, sem safety net)**: `blockchain`, `patent review`, `patent analysis`, `nanotechnology`, `nanotech`, `digital health`, `biomedical`, `quantum cryptography`, `post-quantum cryptography`, `satellite communication`, `quantum communication(s)`, `covid-19`, `covid`, `pandemic`, `lng`, `liquefied natural gas`, `pharmacy`, `central fill`, `robotic dispensing`, `semiconductor manufacturing`, `ESG goals`, `augmented reality`, `women in quantum`, `editorial`, `export control(s)`, `vehicle break(down)`, `level generation`, `microservice(s)`, `innovation ecosystem`, `human-centric economy`, `functional near-infrared`, `fnirs`, `wave-particle duality`, `hamiltonian framework`, `nonadiabatic dynamics`, `weather`, `forecasting the weather`, `lifepo4`, `lithium iron phosphate`, `vaccine supply chain`, `vaccine`, `non-trivial classification`, `quantum kernel framework`, `finance and supply chain`, `shallow entangled circuits`, `ibm devices`.

### 5.4 CE-5 — Tipos de Publicação Excluídos

Tipos não-substantivos excluídos: `book chapter`, `report`, `book`, `dissertation`, `other`, `NaN (sem tipo)`, `dataset`, `component`, `journal issue`, `editorial`, `news`, `conference proceedings`

---

## 6. Resultados

### 6.1 Resumo Geral do Fluxo PRISMA-ScR

```
IDENTIFICAÇÃO
  Artigos brutos (28 CSVs, strings 10-14 excluídas): 1.792
        |
  Deduplicação por DOI:              -493
  Deduplicação por título (sem DOI):    -0
  Deduplicação por título (cross-DOI): -68
        |
  Artigos únicos: 1.231
        |
========================================
  FASE 1 — Triagem por Metadados
========================================
  CE-5 (tipo de publicação):    -295
  CE-1 (otimização pura):        -14
  CE-3 (forte — título):        -139
  CE-3 (domínio excluído):      -404
  Total excluídos Fase 1:       -851 (69,1%)
        |
  Incluídos Fase 1: 380
        |
========================================
  FASE 2 — Triagem por Abstract
========================================
  CE-1 (otimização pura):       -10
  CE-2 (apenas trabalho futuro): -24
  CE-3 (domínio excluído):      -84
  Total excluídos Fase 2:      -118 (31,1%)
        |
  ELEGÍVEIS PARA REVISÃO: 261 (21,2% do corpus)
```

### 6.2 Detalhamento por Critério de Exclusão

| Critério | Fase 1 | Fase 2 | Total | % do Corpus |
|----------|--------|--------|-------|-------------|
| CE-5 (tipo de publicação) | 295 | — | 295 | 24,0% |
| CE-1 (otimização pura) | 14 | 10 | 24 | 1,9% |
| CE-2 (trabalho futuro) | — | 24 | 24 | 1,9% |
| CE-3 (domínio excluído) | 404 | 84 | 488 | 39,6% |
| CE-3 (forte — título) | 139 | — | 139 | 11,3% |
| **Total excluídos** | **851** | **118** | **970** | **78,8%** |
| **Elegíveis** | — | — | **261** | **21,2%** |

### 6.3 Evolução da Triagem ao Longo das Iterações

O processo de triagem passou por cinco iterações de refinamento:

| Métrica | Iter. 1 (original) | Iter. 2 (sem strings 10-14) | Iter. 3 (dedup cross-DOI) | Iter. 4 (CE-3 forte, 04-13) | Iter. 5 (revisão manual, 04-14) |
|---------|-------------------|----------------------------|--------------------------|----------------------------|-------------------------------|
| Corpus total | 2.471 | 1.299 | 1.231 | 1.231 | **1.231** |
| Fase 1 excluídos | 1.006 (40,7%) | 770 (59,3%) | 792 (64,3%) | 818 (66,4%) | **851 (69,1%)** |
| Fase 2 excluídos | 311 | 121 | 127 | 124 | **118** |
| Elegíveis | 1.154 (46,7%) | 408 (31,4%) | 312 (25,3%) | 289 (23,5%) | **261 (21,2%)** |
| Precisão estimada | ~27% | ~58% | ~75-85% | ~85-90% | **~90%+** |

**Iteração 4 (2026-04-13) — CE-3 forte**: após inspeção manual do corpus de 312 artigos, foram identificados 18 artigos de blockchain, patent reviews e nanotechnology que passavam pela triagem apenas por mencionarem "supply chain". Introduzida regra CE-3 (forte) — aplicada ao título, sem safety net — que excluiu 89 artigos nesta iteração.

**Iteração 5 (2026-04-14) — Expansão pós-revisão manual**: a segunda revisão manual identificou 24 falsos positivos adicionais em 14 novos domínios (LNG/gás natural, farmácia/dispensação, química quântica, comunicação quântica, COVID, manutenção veicular, política econômica, semicondutores, ESG/AR, jogos, microservices, editorial, etc.). Palavras-chave expandidas em ambas as listas (CE-3 padrão e CE-3 forte), resultando em 50 exclusões adicionais.

### 6.4 Artigos sem Abstract

| Tratamento | Quantidade |
|------------|-----------|
| Incluídos (título com palavra-chave SC) | 1 |
| Excluídos (título sem palavra-chave SC) | 8 |
| **Total sem abstract** | **9** |

### 6.5 Classificação por Tipo de Problema (pós-triagem)

Após a triagem, os 261 artigos elegíveis foram classificados por tipo de problema abordado através do script `src/classificar_problema.py`. A taxonomia aplica matching por regex (word boundary) em `Title + Abstract`, com prioridade hierárquica — problema mais específico prevalece sobre categoria ampla.

| # | Categoria | Descrição | Qtd. | % |
|---|-----------|-----------|-----:|----:|
| 1 | `backorder_prediction` | Predição de backorder / stockout (CI-2) | 4 | 1,5% |
| 2 | `demand_forecasting` | Previsão de demanda / vendas (CI-2) | 32 | 12,3% |
| 3 | `inventory_control` | Controle/otimização de inventário, replenishment (CI-2) | 17 | 6,5% |
| 4 | `routing_transportation` | VRP, TSP, roteamento, last-mile, freight, fleet | 17 | 6,5% |
| 5 | `scheduling_production` | Job/flow shop, production scheduling, lot sizing | 4 | 1,5% |
| 6 | `supplier_procurement` | Seleção de fornecedor, sourcing, procurement | 6 | 2,3% |
| 7 | `risk_resilience` | Risco, resiliência, disruption, counterfeit em SC | 4 | 1,5% |
| 8 | `sustainability_sc` | SC sustentável/verde, carbono, circular economy | 4 | 1,5% |
| 9 | `predictive_maintenance` | Prognosis, health management, RUL, fault detection | 8 | 3,1% |
| 10 | `supply_chain_general` | Catch-all SC (gestão geral, warehousing, distribuição) | 73 | 28,0% |
| 11 | `industry40_smart_mfg` | Industry 4.0/5.0, smart manufacturing, digital twin, IIoT | 13 | 5,0% |
| 12 | `qml_method_review` | Reviews/surveys de QML, benchmarks metodológicos sem foco em SC | 21 | 8,0% |
| 13 | `outros` | Não classificado (apenas QML sem âncora clara em SC) | 58 | 22,2% |
| | **Total** | | **261** | **100%** |

**Observações**:
- As três categorias do núcleo CI-2 (`backorder_prediction`, `demand_forecasting`, `inventory_control`) totalizam **53 artigos (20,3%)** — representam o centro de interesse da pesquisa.
- `supply_chain_general` (28,0%) agrega artigos de SC sem especialização clara em um problema específico — requerem revisão manual para identificar o sub-problema real.
- `outros` (22,2%) captura artigos genéricos de QML ou Industry 4.0 que passaram pela triagem mas não têm âncora clara em SC — candidatos prioritários para revisão crítica e eventual exclusão manual.

---

## 7. Decisões de Design e Justificativas

### 7.1 Por que remover strings em vez de expandir CE-3?

A abordagem de expandir critérios de exclusão para cada domínio fora de escopo é uma estratégia limitada: cada novo domínio exige dezenas de termos, e sempre haverá domínios emergentes não cobertos. A remoção das strings 10–14 trata a **causa raiz** — strings sem especificidade de domínio capturando QML aplicado a qualquer área — com perda mínima (1,7% de relevância).

### 7.2 Por que Fields of Study na Fase 1?

O campo `Fields of Study` do Lens.org contém áreas temáticas atribuídas automaticamente (ex: "Computer science; Quantum mechanics; Physics"). Para CE-3, este campo é altamente informativo: se um artigo está classificado como "Particle physics" ou "Organic chemistry", a probabilidade de ser relevante para supply chain é mínima. Incluí-lo na Fase 1 (metadados) ampliou a detecção de domínios fora de escopo sem necessidade do abstract.

### 7.3 Por que separar título (Fase 1) e abstract (Fase 2)?

Aplicar CE-1 e CE-3 no título em ambas as fases era redundante — se um artigo passou pela checagem de título na Fase 1, re-checar o título na Fase 2 não produz exclusões adicionais. A separação garante que cada fase analisa informação nova: Fase 1 = metadados (título + tipo + fields of study), Fase 2 = conteúdo textual (abstract).

### 7.4 Por que deduplicação cross-DOI por título?

Artigos podem receber DOIs diferentes em estágios distintos de publicação (preprint no arXiv vs. versão final em periódico). A deduplicação original por DOI não captura esses casos. A etapa adicional de normalização e comparação de títulos removeu 68 duplicatas que inflavam artificialmente o corpus.

### 7.5 Abordagem conservadora vs. entradas irrelevantes sem abstract

A regra original incluía automaticamente artigos sem abstract ("na dúvida, incluir"). Após análise, verificou-se que a maioria dos artigos sem abstract eram entradas irrelevantes (editoriais, tabelas de conteúdo, registros institucionais). A nova regra exige pelo menos uma palavra-chave de supply chain no título para inclusão sem abstract, equilibrando conservadorismo com qualidade do corpus.

---

## 8. Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `data/artigos_unicos.csv` | 1.231 artigos deduplicados com metadados completos |
| `data/artigos_unicos_triagem.csv` | 1.231 artigos + colunas `fase1_decisao`, `fase2_decisao`, `motivo_exclusao`, `tipo_problema` |
| `data/resumo_deduplicacao.csv` | Estatísticas da deduplicação |
| `data/resumo_por_string.csv` | Distribuição de artigos por string de busca |

### Colunas Adicionadas pela Triagem e Classificação

| Coluna | Valores | Descrição |
|--------|---------|-----------|
| `fase1_decisao` | `incluir` / `excluir` | Decisão da Fase 1 |
| `fase2_decisao` | `incluir` / `excluir` / `nao_avaliado` | Decisão da Fase 2 (`nao_avaliado` = excluído na Fase 1) |
| `motivo_exclusao` | `CE-1` / `CE-2` / `CE-3` / `CE-3 (forte)` / `CE-5` / vazio | Primeiro critério que excluiu o artigo |
| `tipo_problema` | Ver taxonomia na seção 6.5 / `nao_avaliado` | Categoria do problema abordado (apenas para `fase2_decisao = incluir`) |

---

## 9. Reprodutibilidade

Para reproduzir os resultados:

```bash
# 1. Regenerar o corpus deduplicado (exclui strings 10-14, dedup cross-DOI)
python src/deduplicar_artigos.py

# 2. Executar a triagem automatizada (gera fase1_decisao, fase2_decisao, motivo_exclusao)
python src/triagem_artigos.py

# 3. Classificar os elegíveis por tipo de problema (gera tipo_problema)
python src/classificar_problema.py
```

Todos os critérios, palavras-chave, regras de matching e lógicas de decisão estão codificados no script `src/triagem_artigos.py` e documentados no protocolo `docs/protocolo_triagem.md`. Outro pesquisador aplicando os mesmos scripts sobre os mesmos CSVs de entrada deve obter resultados **idênticos**.

---

## 10. Conclusão

A triagem automatizada reduziu o corpus de **1.231 artigos únicos** para **261 elegíveis** (21,2%), com uma precisão estimada de **~90%+** para artigos efetivamente relacionados ao escopo da pesquisa (QML aplicado a supply chain, logística, inventário e previsão de demanda).

O critério CE-3 em suas duas variantes (padrão + forte) foi o mais impactante, responsável por **627 exclusões (51,0% do corpus)**, refletindo a natureza multidisciplinar da literatura em QML — o campo atrai pesquisadores de física, saúde, finanças, energia e dezenas de outros domínios que aplicam os mesmos métodos QML a problemas distintos.

Três decisões de design foram especialmente impactantes:

1. **Remoção das strings de busca #10–#14** (Iteração 2): reduziu o corpus em 47% (de 2.471 para 1.231 artigos) eliminando a principal fonte de ruído, com perda de apenas 2 artigos de alta relevância. Demonstra a importância de avaliar a qualidade das fontes de dados antes de sofisticar o processo de filtragem.

2. **Introdução do CE-3 (forte)** (Iteração 4): a lógica de safety net, embora conservadora, criava uma "imunidade" para artigos que mencionavam "supply chain" de passagem. A regra forte — aplicada apenas ao título, sem safety net — corrige esse viés excluindo artigos cujo foco principal está em outro domínio (blockchain, patent review, nanotecnologia, etc.).

3. **Ciclo de revisão manual → expansão de keywords** (Iterações 4 e 5): a inspeção humana de amostras dos resultados permitiu identificar padrões de falsos positivos não antecipados no protocolo inicial. A expansão iterativa das listas de exclusão — tanto padrão quanto forte — demonstra que um pipeline PRISMA-ScR automatizado se beneficia de loops de feedback humano para refinamento contínuo.

Adicionalmente, a classificação pós-triagem por **tipo de problema** (coluna `tipo_problema` com 13 categorias) fornece estrutura semântica ao corpus elegível, identificando que o núcleo da CI-2 (backorder, demand forecasting, inventory) concentra **53 artigos (20,3%)** e que 80 artigos (30,6%) requerem atenção especial na revisão manual (`supply_chain_general` subclassificado + `outros`).

---

## 11. Próximos Passos

1. **Revisão manual dos 261 artigos elegíveis** — priorização por `tipo_problema`: iniciar pelas categorias do núcleo CI-2 (`backorder_prediction`, `demand_forecasting`, `inventory_control`), seguida das demais categorias específicas e por fim os catch-all (`supply_chain_general`, `outros`)
2. **Triagem crítica das categorias genéricas** — revisão manual direcionada de `outros` (58) e `qml_method_review` (21) para confirmar exclusão ou reclassificação
3. **Leitura de texto completo (full-text review)** — para os artigos confirmados como relevantes na revisão manual, leitura integral para extração de dados
4. **Classificação por método QML** — categorizar os artigos por arquitetura QML utilizada (QNN, VQC, QSVM, QRL, Quantum Kernel, QRC) e resultados reportados (complementa a coluna `tipo_problema` já existente)
5. **Construção da tabela de revisão bibliográfica** — tabela estruturada para o artigo final com: autor, ano, método QML, problema (`tipo_problema`), dataset, métricas de desempenho, comparação com baseline clássico
6. **Atualização do diagrama PRISMA-ScR** — com os números finais de cada etapa do fluxo de triagem (inclusive CE-3 forte e classificação por tipo de problema)

---

*Documentação criada em: 2026-04-11*
*Última atualização: 2026-04-14 (CE-3 forte, revisão manual expandida, classificação por tipo_problema)*
*Corpus de entrada: `data/artigos_unicos.csv` (1.231 artigos)*
*Scripts de execução: `src/triagem_artigos.py`, `src/classificar_problema.py`*
*Protocolo de referência: `docs/protocolo_triagem.md`*
