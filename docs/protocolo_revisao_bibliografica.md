# Protocolo de Revisão Bibliográfica — Extração Manual de Dados

## 1. Objetivo

Este protocolo padroniza a extração manual de dados dos 261 artigos elegíveis (fase2_decisao == `incluir`) durante a leitura de texto completo. A tabela estruturada em `data/tabela_revisao_bibliografica.xlsx` é o artefato de trabalho principal desta etapa e servirá de base para:

1. Identificação de artigos efetivamente relevantes para a dissertação (filtro humano final)
2. Extração de dados metodológicos (método QML, baseline clássico, dataset, métricas)
3. Composição da tabela de resultados do artigo final
4. Atualização do diagrama PRISMA-ScR com números consolidados

A tabela é gerada por `src/gerar_tabela_revisao.py`, que herda metadados do CSV de triagem (`data/artigos_unicos_triagem.csv`) e adiciona campos vazios para preenchimento manual.

---

## 2. Estrutura da Tabela

### 2.1 Colunas auto-preenchidas (grupo A — 11 colunas)

Herdadas dos metadados do Lens.org. **Não editar** manualmente (serão sobrescritas se a geração for re-executada).

| Coluna | Descrição |
|--------|-----------|
| `id` | Lens ID (identificador único do artigo) |
| `titulo` | Título completo |
| `autores_completo` | Lista completa de autores (separados por `;`) |
| `ano` | Ano de publicação |
| `venue` | Periódico/conferência |
| `publication_type` | journal article / conference paper / preprint |
| `doi` | DOI |
| `url` | Link direto (External URL) |
| `is_open_access` | Booleano de acesso aberto |
| `citing_works` | Número de citações no Lens |
| `tipo_problema_auto` | Classificação automática da triagem (não é dado extraído — é pré-classificação) |

### 2.2 Colunas de extração manual (grupo B — 19 colunas)

#### Decisão do revisor

| Coluna | Valores | Descrição |
|--------|---------|-----------|
| `revisado` | `sim` / `nao` | Marque `sim` após leitura do texto completo |
| `relevancia_final` | `alta` / `media` / `baixa` / `excluir` | Ver critérios na seção 3 |
| `problema_validado` | taxonomia da seção 5.5 do protocolo de triagem | Confirma ou revisa `tipo_problema_auto` (ver seção 4) |

#### Método QML

| Coluna | Valores | Descrição |
|--------|---------|-----------|
| `metodo_qml` | `QNN` / `VQC` / `QSVM` / `QRL` / `Quantum Kernel` / `QRC` / `Hybrid` / `Other` | Ver definições na seção 5 |
| `metodo_qml_detalhe` | texto livre | Arquitetura, nº camadas, ansatz, encoding, etc. |

#### Baseline clássico

| Coluna | Valores | Descrição |
|--------|---------|-----------|
| `baseline_classico` | texto livre | Método clássico comparado (ex: LSTM, ARIMA, Random Forest, XGBoost, SVM). Use `nenhum` se não há comparação |

#### Dataset

| Coluna | Valores | Descrição |
|--------|---------|-----------|
| `dataset_nome` | texto livre | Nome ou descrição breve |
| `dataset_tamanho` | número inteiro | N de amostras. Use `NA` se não reportado |
| `dataset_fonte` | `publico` / `proprietario` / `sintetico` / `benchmark` | Ver seção 6 |

#### Resultados

| Coluna | Formato | Descrição |
|--------|---------|-----------|
| `metricas` | `metrica=valor; metrica=valor` | Ver convenção na seção 7 |
| `resultado_qml_vs_classico` | `melhor` / `equivalente` / `pior` / `nao_comparado` | Desempenho relativo do método QML proposto |
| `diferenca_percentual` | texto | Ex: `+3.2% acc`, `-0.015 MSE`, `2x speedup` |

#### Hardware

| Coluna | Valores | Descrição |
|--------|---------|-----------|
| `hardware` | `simulator` / `real_quantum` / `both` | Tipo de execução |
| `hardware_detalhe` | texto livre | Provedor/simulador (ex: Qiskit Aer, IBM Brisbane, D-Wave Advantage, Xanadu X8, PennyLane lightning.qubit) |
| `n_qubits` | número inteiro | Qubits usados (físicos ou simulados). Use `NA` se não aplicável |

#### Síntese

| Coluna | Valores | Descrição |
|--------|---------|-----------|
| `limitacoes` | texto livre | Limitações reportadas pelos próprios autores |
| `tipo_contribuicao` | `novel_method` / `benchmark` / `application` / `review` / `case_study` | Ver seção 8 |
| `contribuicao_para_sc` | texto livre | Como o trabalho contribui especificamente para QML em Supply Chain/Logística |
| `notas` | texto livre | Observações do revisor (artigo duplicado, versões do mesmo trabalho, trabalhos relacionados, ressalvas metodológicas) |

---

## 3. Critérios de Relevância Final

| Nível | Critério |
|-------|----------|
| `alta` | Aplica método QML a problema **do núcleo CI-2** (demand forecasting, inventory control, backorder prediction) **com** experimento reproduzível e comparação com baseline clássico |
| `media` | Aplica QML a outro problema de SC/logística (routing, scheduling, supplier, risk, sustainability) OU aplica QML ao núcleo CI-2 sem baseline clássico claro |
| `baixa` | Mencão superficial de SC sem contribuição metodológica QML-SC clara; artigos de contexto/motivação |
| `excluir` | Falso positivo da triagem — artigo não é sobre QML aplicado a SC (ex: QML genérico, outro domínio). Registrar em `notas` o motivo da exclusão |

Artigos `relevancia_final = excluir` devem ser justificados no campo `notas` e serão contabilizados no diagrama PRISMA-ScR como exclusões de full-text review.

---

## 4. `problema_validado` vs `tipo_problema_auto`

A coluna `tipo_problema_auto` vem da classificação automática por palavras-chave (`src/classificar_problema.py`). É uma **pré-classificação** derivada de Title + Abstract, que pode estar errada ou ser genérica demais (muitos artigos são classificados como `supply_chain_general`).

Após a leitura do texto completo, preencha `problema_validado` com a categoria correta da mesma taxonomia. Se `problema_validado == tipo_problema_auto`, a classificação automática é confirmada. Se diferente, a automática foi corrigida — registre o motivo em `notas` quando útil (para calcular a precisão da classificação automática posteriormente).

---

## 5. Taxonomia de `metodo_qml`

| Valor | Definição |
|-------|-----------|
| `QNN` | Quantum Neural Network — rede quântica parametrizada treinada como NN (inclui QCNN, QRNN, QLSTM quando a componente principal é uma rede) |
| `VQC` | Variational Quantum Classifier / Variational Quantum Circuit — circuito parametrizado treinado por otimização clássica para classificação/regressão |
| `QSVM` | Quantum Support Vector Machine — SVM com kernel computado em hardware quântico |
| `QRL` | Quantum Reinforcement Learning — agentes de RL com políticas ou value functions quânticas |
| `Quantum Kernel` | Método baseado em kernel quântico (sem ser QSVM — ex: Kernel ridge regression, Gaussian process com kernel quântico) |
| `QRC` | Quantum Reservoir Computing — reservoir dinâmico quântico com readout clássico |
| `Hybrid` | Arquitetura híbrida que não se encaixa em uma única categoria acima (ex: CNN clássica + camada variacional final) |
| `Other` | Qualquer outro método QML não listado (QBM, QGAN, Quantum Autoencoder, etc.) — descreva em `metodo_qml_detalhe` |

**Regra de desempate**: quando o artigo combina múltiplos métodos, escolha o método **central** da contribuição. Ex: "QLSTM híbrido com camada clássica" → `QNN` (a LSTM quântica é o método central) + detalhe em `metodo_qml_detalhe`.

---

## 6. Taxonomia de `dataset_fonte`

| Valor | Definição |
|-------|-----------|
| `publico` | Dataset publicamente acessível (Kaggle, UCI, GitHub, site oficial) com link/citação |
| `proprietario` | Dataset privado/industrial sem acesso público |
| `sintetico` | Dataset gerado pelos autores (simulação, distribuição paramétrica, random walks) |
| `benchmark` | Dataset canônico de benchmark em SC (ex: Beer Game, M5 Competition, SKU-Level Demand Datasets) |

---

## 7. Convenção de `metricas`

Formato chave-valor separado por ponto-e-vírgula, sem espaços após o `=`:

```
accuracy=0.92; mse=0.015; f1=0.89
```

Métricas aceitas (use estas abreviações quando aplicável):

- Classificação: `accuracy`, `precision`, `recall`, `f1`, `auc`, `auroc`
- Regressão/previsão: `mse`, `rmse`, `mae`, `mape`, `r2`
- Otimização: `cost`, `gap`, `approximation_ratio`
- Treinamento: `loss`, `epochs`, `training_time`

Se o artigo reporta múltiplas variantes, capture apenas o **melhor resultado do método QML proposto**. Variantes adicionais podem ir em `notas`.

Se nenhuma métrica quantitativa foi reportada (ex: artigo teórico), use `nao_reportado`.

---

## 8. Taxonomia de `tipo_contribuicao`

| Valor | Definição |
|-------|-----------|
| `novel_method` | Propõe nova arquitetura/algoritmo QML |
| `benchmark` | Compara métodos QML existentes em dataset(s) de SC, sem novidade metodológica |
| `application` | Aplica método QML existente a problema específico de SC (estudo de aplicação) |
| `review` | Review/survey da literatura |
| `case_study` | Estudo de caso industrial ou institucional específico |

---

## 9. Procedimento de Preenchimento

1. **Ordem recomendada**: a tabela já está ordenada por `tipo_problema_auto` priorizando o núcleo CI-2 (backorder → demand → inventory → demais). Leia nesta ordem — artigos mais centrais ao objetivo da pesquisa são os primeiros.

2. **Ciclo por artigo**:
   1. Abrir o artigo via `url` ou `doi`
   2. Ler título, abstract, e seções de método/experimento
   3. Se `relevancia_final = excluir`, preencha apenas `revisado`, `relevancia_final`, `notas` — demais campos podem ficar vazios
   4. Caso contrário, preencher todos os campos manuais aplicáveis
   5. Marcar `revisado = sim`

3. **Campos sem informação**: use `nao_reportado` (texto livre) ou `NA` (numérico). **Não deixe em branco** após revisar — isso permite distinguir "não lido" de "lido mas sem info".

4. **Dupla-checagem**: se disponível um segundo revisor, rode a leitura em paralelo e compare preenchimentos divergentes. Cálculo de concordância inter-avaliadores (Cohen's kappa) pode ser adicionado depois.

5. **Versionamento**: a tabela `.xlsx` é o artefato de trabalho; exporte snapshots periódicos para `data/snapshots/tabela_revisao_YYYY-MM-DD.csv` para rastreabilidade.

---

## 10. Reprodutibilidade

Para regenerar a **estrutura** da tabela (descartando preenchimento manual):

```bash
python src/gerar_tabela_revisao.py
```

**Atenção**: o script sobrescreve `tabela_revisao_bibliografica.csv` e `.xlsx`. Antes de re-executar após preenchimento manual, salve backup dos campos manuais.

Estratégia recomendada de atualização sem perda de dados:

1. Manter o `.xlsx` preenchido como artefato principal
2. Re-executar o script apenas quando o conjunto de elegíveis mudar (após nova iteração de triagem)
3. Merge manual dos campos preenchidos do `.xlsx` antigo para o novo (via `id` como chave)

---

## 11. Entregáveis Finais desta Etapa

Após completar a extração manual:

1. `data/tabela_revisao_bibliografica.xlsx` completa (todos os artigos com `revisado = sim`)
2. Estatísticas derivadas:
   - Distribuição de `metodo_qml` entre os relevantes
   - Distribuição de `resultado_qml_vs_classico`
   - Precisão da classificação automática (`tipo_problema_auto` vs `problema_validado`)
   - Contagem de artigos por `relevancia_final`
3. Atualização do diagrama PRISMA-ScR com o número final após full-text review
4. Subset de artigos `relevancia_final = alta` como corpus de síntese para o artigo final

---

*Protocolo criado em: 2026-04-14*
*Script de geração: `src/gerar_tabela_revisao.py`*
*Corpus de entrada: `data/artigos_unicos_triagem.csv` (261 artigos com `fase2_decisao = incluir`)*
