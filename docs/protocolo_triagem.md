# Protocolo de Triagem — Revisao Sistematica QML + Inventario/Supply Chain

## 1. Objetivo

Este protocolo define os criterios e procedimentos para triagem sistematica do corpus de artigos unicos obtidos na Etapa 1 (busca bibliografica + deduplicacao).

> **Atualizacao (2026-04-11):** As strings de busca #10 a #14 foram removidas do pipeline por baixa precisao (1,7% de relevancia para supply chain). O corpus foi reduzido de 2.471 para o total gerado pela re-execucao do script de deduplicacao. Adicionalmente, o campo `Fields of Study` foi incorporado a Fase 1 (metadados) e a Fase 2 passou a analisar apenas o abstract (sem redundancia de titulo). O objetivo e classificar cada artigo como relevante ou irrelevante para a revisao sobre **Quantum Machine Learning (QML) aplicado a previsao de demanda e controle de inventario em cadeias de suprimentos**.

A triagem e realizada em **duas fases automatizadas**, seguidas de revisao manual dos casos elegiveis. Todos os artigos sao mantidos no dataset — nenhum e removido, apenas classificado.

---

## 2. Criterios de Inclusao (CI)

O artigo deve atender a **todos** os criterios abaixo para ser considerado elegivel:

| Codigo | Criterio | Justificativa |
|--------|----------|---------------|
| CI-1 | Aplica algum metodo de Quantum Machine Learning (QNN, VQC, QSVM, QRL, Quantum Kernel, Quantum Reservoir Computing ou hibrido quantum-classico) | Garante que o corpus se limita a QML, excluindo computacao quantica pura (otimizacao combinatoria sem aprendizado) |
| CI-2 | Aborda ao menos um dos problemas: previsao de demanda, controle/otimizacao de inventario, predicao de backorder, ou gestao de supply chain | Alinha com os eixos tematicos 1 e 3 do sistema de busca |
| CI-3 | Publicado entre 2017 e 2026 | 2017 = ano do artigo seminal Biamonte et al.; janela alinhada ao corpus coletado |
| CI-4 | Texto em ingles ou portugues | Idiomas de trabalho do projeto |
| CI-5 | Disponivel em acesso aberto ou acessivel via instituicao | Viabilidade pratica para mestrado profissional |

> **Nota**: CI-3, CI-4 e CI-5 sao verificados manualmente na fase de elegibilidade (pos-triagem automatizada). A triagem automatizada foca em CI-1 e CI-2 indiretamente, via criterios de exclusao.

---

## 3. Criterios de Exclusao (CE)

A presenca de **qualquer um** dos criterios abaixo exclui o artigo:

| Codigo | Criterio | Justificativa | Fase de Aplicacao |
|--------|----------|---------------|-------------------|
| CE-1 | Artigo aborda apenas otimizacao quantica pura sem componente de aprendizado de maquina (QAOA, quantum annealing, VQE para problemas combinatorios, sem treinamento/learning) | Computacao quantica para otimizacao nao e QML | Fase 1 (titulo + fields of study) + Fase 2 (abstract) |
| CE-2 | QML e mencionado apenas como trabalho futuro ou especulacao, sem implementacao ou experimento | Sem contribuicao empirica ou metodologica para QML | Fase 2 apenas (requer abstract) |
| CE-3 | Dominio de aplicacao nao relacionado a supply chain/logistica/predicao (ex.: drug discovery, protein folding, financas, telecomunicacoes, grafeno, ciencia de materiais, medicina, genomica, energia, reconhecimento facial) | Dominio fora do escopo da pesquisa | Fase 1 (titulo + fields of study) + Fase 2 (abstract) |
| CE-3 (forte) | Titulo evidencia claramente outro dominio de pesquisa — blockchain, patent review/analysis, nanotechnology/nanotech, digital health, biomedical, quantum cryptography, post-quantum cryptography, satellite communication — mesmo quando o artigo menciona "supply chain" ou termos correlatos de passagem | Artigos cujo titulo centraliza a contribuicao em outra area nao devem ser salvos pela simples mencao de SC | Fase 1 (titulo apenas) |
| CE-4 | Artigo duplicado nao removido na deduplicacao por DOI | Ja tratado pelo script `deduplicar_artigos.py` — nao aplicado na triagem | N/A |
| CE-5 | Tipo de publicacao nao-substantivo: editorial, news, dataset, component, journal issue, conference proceedings (volume dos anais, nao artigo individual) | Nao constitui contribuicao academica substantiva | Fase 1 (coluna Publication Type) |

---

## 4. Fluxo de Triagem (PRISMA-ScR)

```
IDENTIFICACAO
  Artigos unicos (pos-deduplicacao, strings 10-14 removidas)
        |
        v
========================================
  FASE 1 — Triagem por Metadados
  (titulo + tipo de publicacao + fields of study)
----------------------------------------
  Criterios aplicados:
    CE-5: tipo de publicacao excluido
    CE-1: otimizacao pura no titulo + fields of study
    CE-3: dominio fora de escopo no titulo + fields of study
========================================
        |
        v
  Artigos incluidos na Fase 1
        |
        v
========================================
  FASE 2 — Triagem por Abstract
  (apenas abstract)
----------------------------------------
  Criterios aplicados:
    CE-1: otimizacao pura no abstract
    CE-2: QML apenas como trabalho futuro
    CE-3: dominio fora de escopo no abstract
  Nota: artigos sem abstract passam
        automaticamente (abordagem conservadora)
========================================
        |
        v
  Artigos elegiveis para revisao completa
```

---

## 5. Operacionalizacao

### 5.1 Automacao

A triagem e executada pelo script `src/triagem_artigos.py`, que:

1. Carrega `data/artigos_unicos.csv` (artigos deduplicados, strings 10-14 excluidas)
2. Aplica **Fase 1** — classificacao por titulo + tipo de publicacao + fields of study
3. Aplica **Fase 2** — classificacao por abstract apenas (artigos incluidos na Fase 1)
4. Exporta `data/artigos_unicos_triagem.csv` com todas as colunas originais + 3 novas colunas

### 5.2 Colunas Adicionadas

| Coluna | Valores Possiveis | Descricao |
|--------|-------------------|-----------|
| `fase1_decisao` | `incluir` / `excluir` | Decisao da Fase 1 |
| `fase2_decisao` | `incluir` / `excluir` / `nao_avaliado` | Decisao da Fase 2 (`nao_avaliado` se excluido na Fase 1) |
| `motivo_exclusao` | `CE-1` / `CE-2` / `CE-3` / `CE-3 (forte)` / `CE-5` / vazio | Primeiro criterio que excluiu o artigo |
| `tipo_problema` | Ver taxonomia na secao 5.5 / `nao_avaliado` | Tipo de problema de SC abordado (apenas para `fase2_decisao = incluir`) |

### 5.3 Logica de Matching

- Todas as comparacoes sao **case-insensitive**
- Palavras-chave sao compiladas como **regex com word boundary** (`\b`) para evitar matches parciais
- Logica de **duas camadas**: palavra de exclusao + safety net de retencao
  - CE-1: excluir se `tem_otimizacao E NAO tem_ml`
  - CE-3: excluir se `tem_dominio_fora E NAO tem_dominio_supply_chain`
  - CE-2: excluir se `tem_mencao_futuro E NAO tem_indicador_experimento`

### 5.4 Prioridade de Aplicacao

**Fase 1** (ordem de verificacao — titulo + tipo de publicacao + fields of study):
1. CE-5 (tipo de publicacao)
2. CE-1 (otimizacao pura no titulo + fields of study)
3. CE-3 (forte) — dominio claramente fora de escopo no titulo (ignora salvaguarda de SC)
4. CE-3 (dominio fora de escopo no titulo + fields of study, com salvaguarda de SC)

**Fase 2** (ordem de verificacao — apenas abstract):
1. CE-1 (otimizacao pura no abstract)
2. CE-2 (apenas trabalho futuro no abstract)
3. CE-3 (dominio fora de escopo no abstract)

Apenas o **primeiro criterio** que exclui o artigo e registrado em `motivo_exclusao`.

### 5.5 Classificacao por Tipo de Problema (pos-triagem)

Apos a triagem, o script `src/classificar_problema.py` atribui a coluna `tipo_problema` para artigos com `fase2_decisao = incluir`. Taxonomia (em ordem de prioridade de matching):

| # | Categoria | Descricao |
|---|-----------|-----------|
| 1 | `backorder_prediction` | Predicao de backorder / stockout (CI-2) |
| 2 | `demand_forecasting` | Previsao de demanda / vendas (CI-2) |
| 3 | `inventory_control` | Controle/otimizacao de inventario, replenishment, safety stock (CI-2) |
| 4 | `routing_transportation` | VRP, TSP, roteamento, last-mile, freight, fleet |
| 5 | `scheduling_production` | Job/flow shop, production scheduling, lot sizing |
| 6 | `supplier_procurement` | Selecao de fornecedor, sourcing, procurement |
| 7 | `risk_resilience` | Risco, resiliencia, disruption, counterfeit em SC |
| 8 | `sustainability_sc` | SC sustentavel/verde, carbono, circular economy, reverse logistics |
| 9 | `predictive_maintenance` | Prognosis, health management, RUL, fault detection |
| 10 | `supply_chain_general` | Catch-all SC (gestao geral, warehousing, distribuicao) |
| 11 | `industry40_smart_mfg` | Industry 4.0/5.0, smart manufacturing, digital twin, IIoT |
| 12 | `qml_method_review` | Reviews/surveys de QML, benchmarks metodologicos sem foco em SC |
| 13 | `outros` | Nao classificado |

Matching por regex com word boundary no `Title + Abstract`. A **primeira** categoria que casa (em ordem da tabela) e atribuida, priorizando problemas especificos sobre categorias amplas.

Execucao: `python src/classificar_problema.py` (le/sobrescreve `data/artigos_unicos_triagem.csv` adicionando a coluna `tipo_problema`). Artigos com `fase2_decisao != 'incluir'` recebem `tipo_problema = 'nao_avaliado'`.

---

## 6. Notas Metodologicas

1. **Abordagem conservadora**: na duvida, incluir. Artigos borderline sao mantidos para revisao manual posterior.

2. **Abstracts vazios**: artigos sem abstract (aproximadamente 132 no corpus) passam automaticamente pela Fase 2, pois nao ha informacao suficiente para exclusao. Serao avaliados na revisao de texto completo.

3. **Artigos multilinguagem**: titulos em idiomas diferentes do ingles que nao contenham palavras-chave de exclusao passam automaticamente. O criterio CI-4 (idioma) e verificado manualmente na fase de elegibilidade.

4. **Reprodutibilidade**: todos os criterios, palavras-chave e regras de matching estao documentados neste protocolo e codificados no script. Outro pesquisador aplicando o mesmo protocolo deve obter resultados identicos.

5. **Atualizacao**: este protocolo foi definido **antes** da triagem. Qualquer alteracao posterior deve ser documentada com justificativa e data.

6. **Strings 10-14 removidas (2026-04-11)**: as strings #10 ("QML" AND "Time Series"), #11 ("QML" AND "Forecasting"), #12 ("QNN" AND "Forecasting"), #13 ("Variational Quantum" AND "Forecasting") e #14 ("QML" AND "Prediction") foram removidas do pipeline. Analise de precisao identificou que 98,3% dos artigos exclusivos dessas strings eram falsos positivos (QML aplicado a clima, financas, saude, energia etc.) com apenas 1,7% de relevancia para supply chain. A remocao trata a causa raiz do ruido no corpus.

7. **Fields of Study na Fase 1 (2026-04-11)**: o campo `Fields of Study` (metadado do Lens.org com areas tematicas separadas por `;`) foi incorporado a Fase 1, concatenado ao titulo para analise de CE-1 e CE-3. A Fase 2 passou a analisar apenas o abstract (sem redundancia de titulo, que ja foi checado na Fase 1).

8. **CE-3 "forte" (2026-04-13)**: apos inspecao dos resultados da triagem, foi identificado que 18 artigos sobre blockchain, alem de artigos de patent review e nanotechnology, passavam pela triagem por mencionarem "supply chain" no titulo/abstract. Foi introduzida uma sub-regra CE-3 "forte" — aplicada apenas ao TITULO na Fase 1 — que exclui artigos cujo titulo evidencia claramente outro dominio (blockchain, patent review/analysis, nanotechnology/nanotech, digital health, biomedical, quantum cryptography, post-quantum cryptography, satellite communication), sem revogacao pela presenca de palavras de dominio_manter. Palavras adicionais tambem foram incorporadas a lista padrao CE-3 (patent/landscape, nanomaterial/nanostructure/nanotube/nanofluid, e-health/telemedicine, aerospace/space mission, nuclear fusion/tokamak/plasma physics).

9. **Expansao CE-3 apos revisao manual (2026-04-14)**: revisao manual dos artigos incluidos identificou novos padroes fora de escopo. Foram adicionadas palavras-chave nas listas padrao e "forte" do CE-3 para os seguintes dominios: (a) gas natural/LNG e infraestrutura energetica (lng, liquefied natural gas, mobile power plant, low-carbon energy, energy infrastructure); (b) farmacia e dispensacao de medicamentos (pharmacy, pharmaceutical/medication dispensing, central fill, robotic dispensing); (c) neurociencia/espectroscopia (functional near-infrared, fnirs, fear detection); (d) quimica/fisica quantica (hamiltonian framework, nonadiabatic dynamics, condensed phase, wave-particle duality); (e) comunicacao quantica nao-logistica (quantum communication/communications); (f) estudos de COVID/pandemia (covid, covid-19, pandemic impact); (g) manutencao preditiva veicular (vehicle break down, breakdown prediction); (h) politica economica/comercio internacional (export control, trade sanction, economic/corporate resilience); (i) semicondutores (semiconductor manufacturing/industry); (j) gestao/negocios genericos (innovation ecosystem, human-centric economy, ESG goals/reporting, augmented reality); (k) geracao procedural de conteudo/jogos (level generation, procedural content); (l) engenharia de software (microservice/microservices); (m) editoriais/sociais (women in quantum).

---

## 7. Referencias Metodologicas

- PRISMA-ScR (Preferred Reporting Items for Systematic Reviews and Meta-Analyses extension for Scoping Reviews)
- Tricco, A. C. et al. (2018). PRISMA Extension for Scoping Reviews (PRISMA-ScR)
- Arksey, H., & O'Malley, L. (2005). Scoping studies: towards a methodological framework

---

*Protocolo definido em: 2026-03-31*
*Corpus de entrada: `data/artigos_unicos.csv` (2.471 artigos)*
*Script de execucao: `src/triagem_artigos.py`*
