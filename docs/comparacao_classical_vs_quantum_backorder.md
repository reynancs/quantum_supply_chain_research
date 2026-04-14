# Comparação: Machine Learning Clássica vs Quantum Machine Learning para Predição de Backorder em Supply Chain

Data: 2026-03-31

---

## 1. Introdução

A predição de backorder é um problema crítico em gestão de cadeias de suprimentos. Backorders ocorrem quando um produto está fora de estoque e o cliente aguarda a reposição, gerando custos operacionais, perda de receita e insatisfação do cliente. A classificação binária — o produto entrará em backorder ou não — é o desafio central.

Este documento compara duas abordagens distintas para resolver este problema utilizando o **mesmo dataset de referência**: Machine Learning clássica (Sattar et al., 2026) e Quantum Machine Learning híbrida (Jahin et al., 2023). A análise é orientada pela seguinte **hipótese de investigação**:

> **A computação quântica supera a computação clássica em termos de resultados no problema de classificação binária de backorder em supply chain? Quais os pontos em que a computação quântica se destaca?**

---

## 2. Dataset

Ambos os artigos utilizam o dataset público **"Predict Product Backorders"** do Kaggle:

| Característica | Valor |
|----------------|-------|
| **Fonte** | Kaggle (gowthammiryala/back-order-prediction-dataset) |
| **Total de registros** | 1.929.935 pedidos |
| **Features** | 22 atributos + 1 target binário (went_on_backorder) |
| **Features numéricas** | 15 (national_inv, lead_time, forecast_x_month, sales_x_month, etc.) |
| **Features categóricas** | 7 (flags: potential_issue, deck_risk, oe_constraint, ppap_risk, etc.) |
| **Classe positiva (Backorder)** | 13.981 (0,72%) |
| **Classe negativa (Not Backorder)** | 1.915.954 (99,28%) |
| **Ratio de desbalanceamento** | 1:137 |

O desbalanceamento extremo (137:1) é uma característica central do problema. Ambos os artigos aplicam técnicas de reamostragem, porém com estratégias e escalas diferentes.

---

## 3. Artigo 1 — Machine Learning Clássica

**Sattar, A. et al. (2026).** "A data analytics-driven approach to backorder prediction using federated machine learning in industrial supply chains." *Scientific Reports (Nature)*, 16:4560.

### 3.1 Metodologia

| Aspecto | Descrição |
|---------|-----------|
| **Abordagem** | Redes neurais (SLP e MLP) em setup de Federated Learning |
| **Dataset utilizado** | Dataset completo (~1,9M amostras) |
| **Balanceamento** | Near-Miss (undersampling) + SMOTE (oversampling) |
| **Features** | 21 features originais (sem redução de dimensionalidade) |
| **Arquitetura SLP** | Input (21 neurônios) -> Output (1, sigmoid) |
| **Arquitetura MLP** | Input -> Dense(64, ReLU) -> Dense(32, ReLU) -> Dense(16, ReLU) -> Output(1, sigmoid) |
| **Otimizador** | Adam (lr=0,01) |
| **Loss** | Binary Cross-Entropy |
| **Federated setup** | 3 clientes, 20 rounds, FedAvg |
| **Validação** | 5-fold cross-validation |
| **Explainability** | LIME + SHAP |
| **Ambiente** | Google Colab, NVIDIA Tesla K80 GPU |

### 3.2 Resultados

**Modelo Federado (MLP) — Melhor resultado:**

| Métrica | Not Backorder | Backorder | Média |
|---------|:------------:|:---------:|:-----:|
| Accuracy | 86,0% | 91,2% | **90,3%** |
| Precision | 91,0% | 87,2% | 89,1% |
| Recall | 86,0% | 91,2% | 88,6% |
| F1-Score | 88,4% | 89,0% | **88,7%** |

**AUC-ROC**: 0,93 (93%)

**Modelo Centralizado (MLP, sem Federated Learning):**

| Métrica | Not Backorder | Backorder | Média |
|---------|:------------:|:---------:|:-----:|
| Accuracy | - | - | **90,9%** |
| Precision | 88,6% | 94,0% | 91,4% |
| Recall | 94,0% | 87,8% | 90,8% |
| F1-Score | 91,0% | 90,6% | **90,8%** |

---

## 4. Artigo 2 — Quantum Machine Learning Híbrida

**Jahin, M. A. et al. (2023).** "QAmplifyNet: Pushing the Boundaries of Supply Chain Backorder Prediction Using Interpretable Hybrid Quantum-Classical Neural Network." *IEEE Access* (preprint arXiv:2307.12906).

### 4.1 Metodologia

| Aspecto | Descrição |
|---------|-----------|
| **Abordagem** | Rede neural híbrida quantum-clássica (QAmplifyNet) |
| **Dataset utilizado** | Dataset reduzido: 1.000 treino (1:1) + 267 teste (3:1) |
| **Balanceamento** | NearMiss (undersampling agressivo, ratio 1:1 treino, 3:1 teste) |
| **Pré-processamento** | Log transform + Standard Scaler + VIF (multicolinearidade) |
| **Redução de dimensionalidade** | PCA: 22 features -> 4 componentes principais |
| **Framework quântico** | PennyLane (simulador, não hardware real) |
| **Qubits** | 2 |
| **Encoding** | Amplitude Embedding (4 amplitudes em 2 qubits) |
| **Circuito variacional** | StronglyEntanglingLayers (1 camada, 6 parâmetros treináveis) |
| **Validação** | 5-fold stratified cross-validation |
| **Explainability** | LIME + SHAP |
| **Teste estatístico** | Paired t-test (10-fold) contra 17 modelos |

### 4.2 Arquitetura do QAmplifyNet

```
Input (4 PCs)
    |
Dense(512, ReLU) -----> FROZEN (não-treinável)
    |
Dense(256, ReLU) -----> FROZEN (não-treinável)
    |
Dense(4, ReLU)   -----> FROZEN (não-treinável)
    |
QNN Keras Layer  -----> 2 qubits, AmplitudeEmbedding + StronglyEntanglingLayers
    |                   (6 parâmetros treináveis: 3 x 2 qubits x 1 layer)
Dense(2, Softmax) ----> Output (Not Backorder / Backorder)
```

As camadas clássicas Dense são **congeladas** (não-treináveis) e servem apenas como extrator de features. O único componente treinado é o circuito quântico com 6 parâmetros.

### 4.3 Resultados — QAmplifyNet

| Métrica | Not Backorder | Backorder | Macro-Average |
|---------|:------------:|:---------:|:-------------:|
| Accuracy | - | - | **90%** |
| Precision | 88% | 100% | 94% |
| Recall | 100% | 60% | 80% |
| F1-Score | 94% | 75% | **84%** |
| Specificity | 60% | 100% | 80% |

**AUC-ROC**: 79,85%
**False Positive Rate**: 0% (nenhum item não-backorder classificado como backorder)

### 4.4 Comparação com outros modelos no MESMO dataset curto

| Categoria | Modelo | Accuracy | AUC-ROC |
|-----------|--------|:--------:|:-------:|
| **Proposto** | **QAmplifyNet** | **90%** | **79,85%** |
| CML | CatBoost | 47% | 73,83% |
| CML | LGBM | 46% | 75,23% |
| CML | Random Forest | 46% | 73,96% |
| CML | XGBoost | 46% | 71,90% |
| CML | 3 Dense NN | 55% | 72,52% |
| CML | KNN | 48% | 55,03% |
| CML | SVM | 49% | 63,74% |
| CML | Decision Tree | 46% | 68,07% |
| QNN | MERA 4-Layered | 78% | 55,97% |
| QNN | RY-CNOT 6-Layered | 75% | 50,00% |
| QNN | Classical NN+Encoder+QNN | 77% | 71,09% |
| Ensemble | QSVM+LGBM+LR | 45% | 70,00% |
| Ensemble | VQC+QSVM | 45% | 62,00% |
| Ensemble | VQC+LGBM | 45% | 60,00% |
| Deep RL | DDQN | 46% | 47,58% |

QAmplifyNet superou **todos os 17 modelos** com significância estatística (paired t-test, p < 0,05).

---

## 5. Comparação Direta

### 5.1 Métricas Globais

| Métrica | ML Clássica (MLP Federado) | ML Clássica (MLP Centralizado) | QML Híbrida (QAmplifyNet) |
|---------|:--------------------------:|:------------------------------:|:-------------------------:|
| Accuracy | 90,3% | 90,9% | 90,0% |
| Precision (média) | 89,1% | 91,4% | 94,0% |
| Recall (média) | 88,6% | 90,8% | 80,0% |
| F1-Score (média) | 88,7% | 90,8% | 84,0% |
| AUC-ROC | 93,0% | - | 79,85% |

### 5.2 Métricas por Classe

| Métrica | MLP Federado (NB / BO) | MLP Centralizado (NB / BO) | QAmplifyNet (NB / BO) |
|---------|:----------------------:|:--------------------------:|:---------------------:|
| Precision | 91,0% / 87,2% | 88,6% / 94,0% | 88% / 100% |
| Recall | 86,0% / 91,2% | 94,0% / 87,8% | 100% / 60% |
| F1-Score | 88,4% / 89,0% | 91,0% / 90,6% | 94% / 75% |
| False Positive Rate | >0% | >0% | **0%** |

*NB = Not Backorder, BO = Backorder*

### 5.3 Aspectos Metodológicos

| Aspecto | Sattar et al. (Clássica) | Jahin et al. (Quântica) |
|---------|--------------------------|-------------------------|
| **Tamanho do treino** | ~1.9M amostras | 1.000 amostras |
| **Tamanho do teste** | ~380K (20% do total) | 267 amostras |
| **Features utilizadas** | 21 originais | 4 componentes (PCA) |
| **Balanceamento** | SMOTE + Near-Miss | Near-Miss agressivo (1:1) |
| **Parâmetros treináveis** | ~5.000+ (MLP 64-32-16) | 6 (circuito quântico) |
| **Hardware** | GPU clássica (Tesla K80) | Simulador quântico (PennyLane) |
| **Privacidade** | Sim (Federated Learning) | Não |
| **Explainability** | LIME + SHAP | LIME + SHAP |
| **Publicação** | Scientific Reports, 2026 | IEEE Access/arXiv, 2023 |

---

## 6. Resposta à Hipótese de Investigação

### Hipótese

> A computação quântica supera a computação clássica em termos de resultados no problema de predição de backorder?

### Resposta

**Não de forma absoluta, mas sim em cenários específicos.** A superioridade depende do contexto operacional, particularmente da disponibilidade de dados.

---

### 6.1 Onde o QML se destaca

#### 1. Cenário de dados escassos — principal vantagem

Este é o ponto mais significativo da comparação. No **mesmo dataset reduzido** (1.000 amostras de treino), QAmplifyNet alcançou 90% de accuracy enquanto o melhor modelo clássico (3-Dense NN) alcançou apenas 55%. A margem de superioridade foi de **+35 pontos percentuais** sobre o melhor clássico, com significância estatística comprovada (paired t-test, p < 0,05).

Em cadeias de suprimentos reais, dados de backorder são inerentemente escassos (ratio de desbalanceamento 137:1 neste dataset). Além disso, empresas frequentemente não compartilham dados por questões de privacidade e competitividade. O cenário de "poucos dados" não é uma limitação artificial — é a realidade operacional de muitas organizações.

#### 2. Eficiência de parâmetros

QAmplifyNet opera com apenas **6 parâmetros treináveis** no circuito quântico (3 ângulos x 2 qubits x 1 camada), contra milhares de parâmetros nos modelos clássicos equivalentes. Menos parâmetros treináveis significam menor risco de overfitting, especialmente crítico em datasets pequenos. O circuito variacional quântico atua como um regularizador natural.

#### 3. Eliminação de Falsos Positivos (FP = 0%)

QAmplifyNet foi o **único modelo entre 18 testados** a alcançar taxa de Falsos Positivos igual a zero. Nenhum item não-backorder foi incorretamente classificado como backorder. Em termos práticos, isso elimina custos de armazenamento desnecessário, obsolescência de estoque e alocação ineficiente de recursos de produção.

#### 4. Robustez em dados desbalanceados com volume reduzido

Os modelos clássicos baseados em árvore (CatBoost, LGBM, RF, XGBoost) colapsaram para ~46% de accuracy no dataset curto — desempenho próximo ao acaso para um problema com ratio de teste 3:1. Estes modelos dependem de volume para construir árvores de decisão eficazes. O circuito quântico, operando no espaço de Hilbert, captura padrões com menos dados através de superposição e entanglement.

#### 5. Amplitude Encoding — compressão exponencial

A codificação por amplitude permite representar N features em log2(N) qubits. No QAmplifyNet, 4 features foram codificadas em 2 qubits. Essa compressão exponencial é uma vantagem inerente da computação quântica que escala favoravelmente: 8 features -> 3 qubits, 16 features -> 4 qubits, 1024 features -> 10 qubits.

---

### 6.2 Onde o ML Clássico se destaca

#### 1. Dataset grande disponível

Quando o dataset completo (~1,9M amostras) está disponível, o MLP clássico centralizado alcança 90,9% de accuracy e 90,8% de F1-Score, superando o QAmplifyNet (90% accuracy, 84% F1). A vantagem clássica emerge com volume de dados.

#### 2. Capacidade discriminativa (AUC-ROC)

O MLP federado alcançou AUC-ROC de **93%** contra **79,85%** do QAmplifyNet. Essa diferença de 13 pontos percentuais indica que o modelo clássico tem capacidade muito superior de distinguir entre as classes em diferentes thresholds de decisão.

#### 3. Detecção real de backorders (Recall classe Backorder)

O recall da classe Backorder é a métrica mais crítica operacionalmente — mede quantos backorders reais o modelo consegue detectar. O MLP federado alcança **91,2%** de recall contra **60%** do QAmplifyNet. Ou seja, o modelo clássico detecta 91 de cada 100 backorders reais, enquanto o quântico detecta apenas 60, perdendo 40% dos casos.

#### 4. F1-Score da classe minoritária

O F1-Score para a classe Backorder é: clássico **89%** vs quântico **75%**. A classe minoritária é precisamente a que importa neste problema — prever backorders corretamente é o objetivo central do sistema.

#### 5. Escalabilidade comprovada

O modelo clássico opera diretamente no dataset completo sem necessidade de PCA ou undersampling extremo. O QAmplifyNet requer redução a 4 componentes principais e 1.000 amostras de treino, com potencial perda de informação discriminativa.

#### 6. Maturidade e infraestrutura

Frameworks clássicos (TensorFlow, PyTorch, scikit-learn) são maduros, com deploy em produção consolidado. O QAmplifyNet foi executado em simulador (PennyLane), não em hardware quântico real. A transição para hardware NISQ introduziria ruído adicional não contabilizado nos resultados.

---

### 6.3 Limitações da Comparação

Esta análise possui limitações importantes que devem ser consideradas:

1. **Condições experimentais diferentes**: Sattar opera no dataset completo (1,9M), Jahin opera em 1.000 amostras. A comparação direta de métricas entre os dois artigos não é rigorosamente justa.

2. **Comparação justa é interna ao artigo de Jahin**: O verdadeiro insight está na comparação de QAmplifyNet contra 17 outros modelos no MESMO dataset curto. Neste cenário controlado, QAmplifyNet superou todos.

3. **Simulador vs hardware real**: QAmplifyNet foi executado em simulador ideal (sem ruído quântico). Resultados em hardware NISQ real tenderiam a ser inferiores.

4. **Perda de informação por PCA**: A redução de 22 features para 4 componentes principais pode descartar informação discriminativa relevante que os modelos clássicos com dataset completo conseguem explorar.

5. **Época NISQ**: Os resultados quânticos representam o estado atual da tecnologia (2 qubits, circuito raso). A evolução do hardware quântico pode alterar substancialmente esta comparação no futuro.

---

## 7. Conclusão

### A computação quântica supera a clássica neste problema?

**A resposta é condicional.** Com base nos dados analisados:

**Em cenários de dados abundantes** — a ML clássica supera o QML. O MLP clássico com dataset completo alcança métricas superiores em AUC-ROC (+13 p.p.), recall de backorder (+31 p.p.) e F1 de backorder (+14 p.p.). Quando dados estão disponíveis, a abordagem clássica é a escolha mais eficaz e prática.

**Em cenários de dados escassos** — o QML híbrido demonstra superioridade expressiva. QAmplifyNet superou todos os 17 modelos comparados (8 clássicos, 5 QNNs, 3 ensembles, 1 deep RL) com margem de +35 p.p. sobre o melhor clássico no mesmo dataset reduzido. Este resultado tem significância estatística comprovada e implicação prática direta: em supply chains reais, dados de backorder são escassos e frequentemente sigilosos.

### Pontos de destaque do QML

A computação quântica se destaca especificamente em:

1. **Generalização com poucos dados** — a vantagem mais robusta e demonstrada
2. **Eficiência paramétrica** — 6 parâmetros treináveis vs milhares
3. **Eliminação de falsos positivos** — único modelo com FP = 0%
4. **Compressão exponencial de features** — via Amplitude Encoding

### Viabilidade do QML para backorder prediction

O QML híbrido é **viável e promissor**, mas **não substitui** a ML clássica no estado atual da tecnologia. A recomendação é:

- **Usar ML clássica** quando dados em volume estão disponíveis e a infraestrutura é madura
- **Considerar QML híbrido** quando dados são escassos, desbalanceados, ou em cenários de privacidade que impedem agregação de dados
- **Explorar abordagens combinadas** (ex.: Federated QML) como direção futura de pesquisa

A evolução do hardware quântico (mais qubits, menor ruído, correção de erros) tende a ampliar as vantagens do QML. O cenário atual (era NISQ) já demonstra resultados promissores com circuitos rasos de 2 qubits, sugerindo potencial significativo conforme a tecnologia amadurece.

---

## Referências

1. Sattar, A. et al. (2026). A data analytics-driven approach to backorder prediction using federated machine learning in industrial supply chains. *Scientific Reports*, 16:4560. DOI: 10.1038/s41598-025-34578-z

2. Jahin, M. A. et al. (2023). QAmplifyNet: Pushing the Boundaries of Supply Chain Backorder Prediction Using Interpretable Hybrid Quantum-Classical Neural Network. *IEEE Access*. arXiv:2307.12906

3. Dataset: Gowtham Miryala. "Back Order Prediction Dataset." Kaggle. https://www.kaggle.com/datasets/gowthammiryala/back-order-prediction-dataset

---

*Documento gerado como parte da revisão bibliográfica do projeto QML + Inventory/Supply Chain.*
*Artigos fonte: `docs/referencia_bibliografica/classical_vs_quantica/`*
