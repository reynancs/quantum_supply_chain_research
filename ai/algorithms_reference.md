# Referência de Algoritmos — Computação Quântica para TSP e QML em Supply Chain

## Taxonomia dos Algoritmos

### 1. Quantum Annealing (QA)

**Princípio**: Explora o estado de menor energia de um sistema quântico via tunelamento quântico. O TSP é formulado como QUBO (Quadratic Unconstrained Binary Optimization) ou modelo de Ising.

| Algoritmo | Descrição | Hardware Típico | Escala (cidades) |
|-----------|-----------|----------------|-----------------|
| D-Wave Quantum Annealing | Annealing nativo em hardware D-Wave | D-Wave 2000Q, Advantage (5640 qubits) | 10–30 (direto), mais com embedding |
| Simulated Quantum Annealing | Simulação clássica do processo de annealing | CPU/GPU clássico | Variável |
| Reverse Annealing | Annealing reverso partindo de solução conhecida | D-Wave Advantage | 10–30 |
| D-Wave Hybrid Solver (Kerberos) | Pipeline híbrido com decomposição automática QA + clássico | D-Wave Leap / AWS Braket | Problemas maiores que o chip |
| D-Wave CQM Solver | Solver para Constrained Quadratic Model, aceita restrições diretamente | D-Wave Leap | Variável (centenas de variáveis) |
| Column Generation + QA | Geração de colunas assistida por annealing para problemas com restrições de desigualdade | D-Wave + Clássico | Variável |

**Formulação QUBO para TSP**: O TSP com N cidades requer N² variáveis binárias. A função objetivo combina a distância total com penalidades por violação de restrições (cada cidade visitada exatamente uma vez, em exatamente uma posição da rota).

---

### 2. Algoritmos Variacionais (Gate-Based)

**Princípio**: Circuitos quânticos parametrizados otimizados por um loop clássico. Adequados para hardware NISQ (Noisy Intermediate-Scale Quantum).

| Algoritmo | Descrição | Hardware Típico | Escala |
|-----------|-----------|----------------|--------|
| QAOA (Quantum Approximate Optimization Algorithm) | Circuito alternando operadores de custo e mixer | IBM Quantum, Google, Rigetti | 5–20 cidades |
| VQE (Variational Quantum Eigensolver) | Encontra autovalor mínimo via ansatz variacional | IBM Quantum | 5–15 cidades |
| QAOA+ / Warm-Start QAOA | QAOA inicializado com solução clássica | IBM Quantum | 5–25 cidades |
| CVaR-QAOA | QAOA com Conditional Value at Risk | Simuladores | 5–20 cidades |
| IQAOA (Indirect QAOA) | QAOA indireto com meta-otimização clássica e Quantum Alternating Operator Ansatz | IBM Quantum | Até 8 cidades (TSP) |
| Grover-Mixer QAOA | Variante do QAOA que usa Grover como mixer para restringir espaço de busca | IBM Quantum | 5–15 cidades |
| F-VQE (Filtering VQE) | VQE com filtragem, convergência mais rápida que QAOA e VQE padrão | IBM Quantum | Até 23 qubits |
| VarQITE | Variational Quantum Imaginary Time Evolution | IBM Quantum | 5–15 cidades |
| AAM-QAOA (Amplitude Amplification-Mixer QAOA) | Combina Quantum Tree Generator com Grover-mixer QAOA | Simuladores / IBM | Variável |
| VQA-PFS (Variational Quantum Algorithm - Preserving Feasible Space) | Operadores mistos + Hardware-Efficient Ansatz, supera QAOA/QAOA+ | IBM Quantum | Variável |
| pVSQA (Post-processing Variationally Scheduled QA) | Combina métodos variacionais com pós-processamento | Simuladores / IBM | Variável |

---

### 3. Algoritmos Gate-Based Exatos

| Algoritmo | Descrição | Complexidade | Escala |
|-----------|-----------|-------------|--------|
| Grover's Search | Busca não-estruturada com speedup quadrático | O(√N!) | Teórico (requer muitos qubits) |
| Grover's Adaptive Search (GAS) | Versão adaptativa de Grover com busca iterativa | IBM Quantum / Simuladores | Teórico / Pequena escala |
| HHL (Harrow-Hassidim-Lloyd) | Resolução de sistemas lineares | Exponencial em precisão | Teórico |
| Quantum Phase Estimation (QPE) | Estimativa de fase para encontrar autovalores; usado para codificar distâncias como fases no TSP | Requer circuitos profundos | Teórico |
| HOBO Encoding + Grover | Higher-Order Unconstrained Binary Optimization com Grover para reduzir qubits | IBM Quantum | Pequena escala |

---

### 4. Abordagens Híbridas (Clássica + Quântica) — Otimização

| Abordagem | Descrição | Vantagem |
|-----------|-----------|---------|
| Decomposição + QA | Divide TSP/VRP grande em sub-problemas, resolve cada um no quantum | Escalabilidade |
| QAOA + Solver Clássico | QAOA gera soluções parciais, solver clássico refina | Qualidade da solução |
| Quantum-Inspired Clássico | Algoritmos clássicos que imitam comportamento quântico (ex: Simulated Bifurcation, Digital Annealing) | Roda em hardware clássico |
| GNN + Quantum | Graph Neural Networks combinadas com processamento quântico | Generalização |
| Quantum Reinforcement Learning (QRL) | Circuitos quânticos substituem camadas de atenção em agentes de RL para VRP | Prova de conceito |
| Quantum Q-Learning | Circuitos parametrizados para aproximar Q-values em CVRP | 3–6 cidades |
| QACO (Quantum Ant Colony Optimization) | Algoritmo quântico de colônia de formigas combinado com K-means | Variável |
| QAmplifyNet | Rede neural híbrida quântica-clássica para previsão de demanda em supply chain | Previsão (não roteamento) |
| QSVM (Quantum Support Vector Machine) | SVM quântico aplicado a problemas de VRP | 3–4 cidades |
| HQAGO (Hybrid Quantum Search + Genetic Optimization) | Busca quântica com otimização genética, fixa qubits como bits clássicos | Variável |
| Hybrid QC-MILP/MIQP Decomposition | Decomposição em MILP/MIQP resolvido classicamente + QUBO no QA | Escala industrial |
| Path-Slicing + Quantum Local Search | Divide TSP em subproblemas via fatiamento de caminhos, resolve com QA | Variável |
| 2-Phase Heuristic (Clustering + Routing) | Fase 1: clustering clássico/quântico; Fase 2: roteamento como TSP | 10–30 cidades |
| DFJ Adaptive (Dantzig-Fulkerson-Johnson) | Eliminação adaptativa de subtours, reduz qubits necessários | Variável |
| QISS (Quantum Industrial Shift Scheduling) | Grover's Adaptive Search para scheduling industrial | Pequena escala |
| QCBR (Quantum Cases-Based Reasoning) | PQC + VQE para raciocínio baseado em casos em scheduling | Pequena escala |

---

### 5. Algoritmos Clássicos (Baseline de Comparação)

| Algoritmo | Tipo | Complexidade | Uso |
|-----------|------|-------------|-----|
| Força Bruta | Exato | O(N!) | Até ~15 cidades |
| Branch and Bound | Exato | Exponencial (podada) | Até ~30 cidades |
| Christofides | Aproximação | O(N³) | Garantia de 1.5x ótimo |
| LKH (Lin-Kernighan-Helsgott) | Heurística | Variável | Instâncias grandes |
| Nearest Neighbor | Heurística gulosa | O(N²) | Baseline simples |
| Genetic Algorithm | Metaheurística | Variável | Instâncias grandes |
| Simulated Annealing (Clássico) | Metaheurística | Variável | Comparação com QA |
| Tabu Search | Metaheurística | Variável | Baseline para JSP e NDP |
| Gurobi (MILP/MIP Solver) | Solver exato comercial | CPU clássico | Benchmark padrão para problemas QUBO |
| CPLEX | Solver exato comercial | CPU clássico | Comparação com soluções quânticas |
| Greedy Heuristic | Heurística gulosa | O(N²) | Baseline simples |
| ADMM (Alternating Direction Method of Multipliers) | Decomposição para otimização distribuída | CPU / híbrido | Variável |

---

### 6. Quantum Machine Learning (QML) — Inventário e Supply Chain

**Princípio**: Utiliza circuitos quânticos parametrizados (PQC) como modelos de aprendizado de máquina. O objetivo é explorar o espaço de Hilbert para codificar e processar dados clássicos de forma que circuitos quânticos atuem como camadas de redes neurais, kernels ou funções de valor.

#### 6.1 Algoritmos de Classificação e Regressão Quântica

| Algoritmo | Descrição | Tarefa em Supply Chain | Hardware Típico | Maturidade |
|-----------|-----------|----------------------|----------------|-----------|
| QSVM (Quantum Support Vector Machine) | Kernel quântico via estimativa de sobreposição de estados (fidelity kernel) para separação de classes | Classificação de risco de ruptura, categorização de SKUs | IBM Quantum, Simuladores PennyLane | NISQ — prova de conceito |
| QKE (Quantum Kernel Estimation) | Estimativa de kernels quânticos para uso em classificadores clássicos (SVM, regressão) | Previsão de demanda como tarefa de classificação | IBM Quantum, Qiskit Runtime | NISQ — pesquisa ativa |
| VQC (Variational Quantum Classifier) | Circuito parametrizado para classificação binária ou multiclasse | Detecção de anomalias em inventário, classificação de padrões de demanda | IBM Quantum, PennyLane | NISQ — amplamente estudado |
| QNN (Quantum Neural Network) | Rede neural implementada como circuito quântico com camadas variacionais (data re-uploading) | Previsão de demanda, otimização de nível de estoque | IBM Quantum, TensorFlow Quantum, PennyLane | NISQ — pesquisa ativa |
| Quantum Transfer Learning | Fine-tuning de QNNs pré-treinadas; camada clássica pré-processada + camada quântica variacional | Adaptação de modelos de previsão entre produtos/regiões | PennyLane + PyTorch | Híbrido — emergente |
| VQLS (Variational Quantum Linear Solver) | Resolve sistemas lineares Ax=b com circuito variacional; alternativa quântica ao HHL | Resolução de modelos de inventário baseados em otimização linear | IBM Quantum / Simuladores | NISQ — teórico/prova de conceito |
| Quantum Ridge Regression | Regressão linear via circuitos quânticos com regularização; usa amplitude encoding | Previsão de séries temporais de demanda (pequena dimensão) | Simuladores | Teórico |

#### 6.2 Algoritmos Generativos Quânticos

| Algoritmo | Descrição | Tarefa em Supply Chain | Hardware Típico | Maturidade |
|-----------|-----------|----------------------|----------------|-----------|
| qGAN (Quantum Generative Adversarial Network) | GAN híbrida com gerador quântico e discriminador clássico ou quântico | Geração de dados sintéticos de demanda; simulação de cenários | IBM Quantum, Qiskit / PennyLane | NISQ — pesquisa ativa |
| QBM (Quantum Boltzmann Machine) | Modelo generativo baseado em distribuição de Boltzmann implementado em circuito quântico | Modelagem de distribuições de demanda com incerteza | D-Wave / Simuladores | Annealing — prova de conceito |
| Quantum Autoencoder | Compressão de estados quânticos em subespaço menor; detecção de anomalias | Redução de dimensionalidade de features de demanda; detecção de outliers em estoque | IBM Quantum / Simuladores | NISQ — pesquisa ativa |
| Born Machine (Quantum Circuit Born Machine — QCBM) | Circuito quântico cujas medições seguem distribuição de Born; modelo probabilístico puro | Modelagem probabilística de demanda intermitente | IBM Quantum / Simuladores | NISQ — pesquisa ativa |

#### 6.3 Algoritmos de Aprendizado por Reforço Quântico

| Algoritmo | Descrição | Tarefa em Supply Chain | Hardware Típico | Maturidade |
|-----------|-----------|----------------------|----------------|-----------|
| VQC-RL (Variational Quantum Circuit RL) | Substitui rede neural de política por VQC em agente de RL | Política de reposição dinâmica de inventário (EOQ dinâmico) | IBM Quantum / PennyLane | NISQ — prova de conceito |
| Quantum Q-Learning | Tabela Q implementada como circuito quântico com amplificação de amplitude | Controle de inventário com estados discretos | Simuladores NISQ | Teórico / pequena escala |
| QRL com atenção quântica | Camadas de atenção de transformers substituídas por circuitos quânticos | Previsão de demanda com dependências temporais longas | IBM Quantum / Simuladores | NISQ — pesquisa ativa |
| Grover-Assisted RL | Uso de Grover para acelerar exploração do espaço de ações | Busca de política ótima em sistemas de inventário multi-produto | Teórico | Teórico |

#### 6.4 Algoritmos Quânticos para Séries Temporais e Previsão

| Algoritmo | Descrição | Tarefa em Supply Chain | Hardware Típico | Maturidade |
|-----------|-----------|----------------------|----------------|-----------|
| QLSTM (Quantum Long Short-Term Memory) | Células LSTM com portas substituídas por VQC; processa dependências temporais | Previsão de séries temporais de demanda | PennyLane + PyTorch | Híbrido — pesquisa ativa |
| Quantum Reservoir Computing | Dinâmica quântica de um circuito fixo usada como reservatório para processamento temporal | Previsão de demanda caótica/sazonal | IBM Quantum / Simuladores | Pesquisa ativa |
| QAmplifyNet | Rede neural híbrida quântica-clássica combinando VQC com LSTM clássico | Previsão de demanda em supply chain com dados históricos | IBM Quantum | Híbrido — emergente |
| Data Re-uploading QNN | Rede quântica com múltiplas reencoding de features ao longo do circuito | Regressão de demanda com sazonalidade | PennyLane | NISQ — pesquisa ativa |

#### 6.5 Otimização de Inventário com QML

| Abordagem | Descrição | Tarefa Específica | Hardware / Framework | Maturidade |
|-----------|-----------|------------------|--------------------|-----------|
| QUBO para EOQ/Reorder Point | Formulação da política ótima de inventário (Economic Order Quantity) como QUBO | Minimização de custo total de estoque com restrições de capacidade | D-Wave / IBM Quantum | NISQ — prova de conceito |
| Quantum Multi-Item Newsvendor | Reformulação do Newsvendor Problem como QUBO/Ising para múltiplos SKUs | Determinação de quantidade ótima de pedido com demanda incerta | D-Wave / Simuladores | Teórico |
| Quantum Portfolio Optimization (adaptado a inventário) | Frameworks de otimização de portfólio quântico (Markowitz quântico) adaptados para mix de SKUs | Balanceamento de capital em estoque multi-produto | IBM Quantum, Qiskit Finance | NISQ — pesquisa ativa |
| Hybrid QML + Classical Forecasting | Pipeline: previsão clássica (ARIMA, XGBoost) → ajuste fino com QNN/VQC | Aumento de acurácia em previsão de demanda de alta variabilidade | PennyLane + scikit-learn | Híbrido — emergente |
| Quantum-Classical Two-Stage | Estágio 1 (QML): previsão/classificação de demanda; Estágio 2 (clássico): otimização de inventário | Integração de previsão quântica com solver clássico (Gurobi) | IBM Quantum + Gurobi | Híbrido — pesquisa ativa |

---

## Hardware Quântico e Simuladores

### 7.1 Hardware Quântico — Gate-Based

| Hardware | Fabricante | Qubits (máx.) | Tecnologia | Acesso | Uso Principal em Supply Chain |
|----------|-----------|--------------|-----------|--------|------------------------------|
| IBM Eagle (r3) | IBM | 127 qubits | Supercondutores | IBM Quantum Platform (cloud) | QAOA, VQE, QML (VQC, QNN) |
| IBM Heron (r2) | IBM | 133 qubits | Supercondutores | IBM Quantum Platform | QAOA, VQE — menor ruído que Eagle |
| IBM Condor | IBM | 1121 qubits | Supercondutores | Pesquisa / IBM Quantum Network | Experimentos QML de maior escala |
| Google Sycamore | Google | 53–72 qubits | Supercondutores | Google Quantum AI (restrito) | Pesquisa de supremacia / QML |
| Google Willow | Google | 105 qubits | Supercondutores | Google Quantum AI | QEC, pesquisa avançada |
| IonQ Aria / Forte | IonQ | 25–36 qubits (AQ) | Íons aprisionados | AWS Braket, Azure Quantum | QML — alta fidelidade, baixo ruído |
| Rigetti Ankaa-2 | Rigetti | 84 qubits | Supercondutores | AWS Braket, Rigetti QCS | QAOA, VQE |
| Quantinuum H2 | Quantinuum | 32 qubits (alta fidelidade) | Íons aprisionados | Azure Quantum | VQC, QML — alta fidelidade |
| Oxford Quantum Circuits (OQC) | OQC | 32 qubits | Supercondutores | AWS Braket | QAOA, VQE |

### 7.2 Hardware Quântico — Annealing

| Hardware | Fabricante | Qubits (máx.) | Tecnologia | Acesso | Uso Principal em Supply Chain |
|----------|-----------|--------------|-----------|--------|------------------------------|
| D-Wave 2000Q | D-Wave | 2048 qubits | Supercondutores (annealing) | D-Wave Leap | TSP, VRP, bin packing — legado |
| D-Wave Advantage | D-Wave | 5000+ qubits | Supercondutores (annealing) | D-Wave Leap / AWS Braket | TSP, VRP, CVRP, inventário QUBO |
| D-Wave Advantage2 (prototype) | D-Wave | 7000+ qubits | Supercondutores (annealing) | D-Wave Leap (acesso limitado) | Problemas QUBO de maior escala |

### 7.3 Simuladores Quânticos

| Simulador | Framework / Fabricante | Tipo | Backend | Uso Principal em QML |
|-----------|----------------------|------|---------|---------------------|
| Qiskit Aer | IBM (Qiskit) | Simulador de circuito clássico | CPU/GPU (cuQuantum) | Simulação de VQC, QAOA, QNN, testes antes do hardware |
| Qiskit Statevector Simulator | IBM (Qiskit) | Statevector exato | CPU | Simulação ideal para circuitos pequenos (até ~30 qubits) |
| Qiskit Fake Backend | IBM (Qiskit) | Noise model realístico | CPU | Testes com ruído calibrado de hardware IBM real |
| PennyLane default.qubit | Xanadu (PennyLane) | Statevector exato | CPU/GPU (JAX, NumPy) | QML: diferenciação automática de VQC, QNN, QLSTM |
| PennyLane lightning.qubit | Xanadu (PennyLane) | Statevector acelerado | CPU (C++) | Simulação eficiente para training de QNN |
| PennyLane lightning.gpu | Xanadu (PennyLane) | Statevector em GPU | NVIDIA GPU (cuQuantum) | Training de QML em larga escala |
| TensorFlow Quantum (TFQ) | Google | Simulador integrado ao TF | CPU/GPU | QML: training de VQC com diferenciação quântica |
| Cirq Simulator | Google | Statevector / density matrix | CPU | Pesquisa de algoritmos quânticos Google |
| Amazon Braket Local Simulator | AWS | Statevector / tensor network | CPU/GPU | Testes locais antes de executar em hardware via Braket |
| Amazon Braket SV1 / DM1 / TN1 | AWS | Simuladores managed (cloud) | CPU/GPU distribuído | Simulação de circuitos médios-grandes (até 34–50 qubits) |
| Azure Quantum simulators | Microsoft | Vários (sparse, full state) | CPU/GPU | Integração com Azure ML + QML workflows |
| cuStateVec (NVIDIA cuQuantum) | NVIDIA | Statevector GPU | NVIDIA GPU | Aceleração de simulação para training QML |
| Qulacs | Osaka University | Statevector C++ | CPU/GPU | Backend rápido para PennyLane / Qiskit, QML |
| MQT DDSIM (Decision Diagram Sim.) | TU Munich | DD-based | CPU | Simulação eficiente de circuitos com estrutura regular |
| NetKet (VMC Quântico) | ETH Zurich / EPFL | Monte Carlo variacional | CPU/GPU | Modelos generativos quânticos (QBM, QCBM) |

### 7.4 Frameworks e Bibliotecas QML

| Framework | Fabricante / Comunidade | Linguagem | Integrações | Uso Principal |
|-----------|------------------------|-----------|------------|--------------|
| PennyLane | Xanadu | Python | PyTorch, TensorFlow, JAX, Qiskit, Braket | Framework principal para QML — diferenciação automática, VQC, QNN, QLSTM |
| Qiskit Machine Learning | IBM | Python | Scikit-learn, PyTorch | QSVM, QKE, VQC, QNN sobre IBM Quantum |
| TensorFlow Quantum (TFQ) | Google | Python | TensorFlow, Cirq | Training end-to-end de modelos híbridos quântico-clássicos |
| Torch Quantum (TorchQuantum) | MIT | Python | PyTorch | QNN, VQC com interface PyTorch nativa |
| tket (pytket) | Quantinuum | Python | Qiskit, Cirq, PennyLane | Compilação e otimização de circuitos para múltiplos backends |
| Qibo | TII / Multi-instituição | Python | TensorFlow, NumPy | Simulação e execução em hardware; QML variacional |
| Mitiq | Unitary Fund | Python | Qiskit, Cirq, Braket | Mitigação de erros em NISQ — essencial para QML em hardware real |
| OpenQASM 3 | IBM / Consórcio | Linguagem | Qiskit, tket | Representação intermediária de circuitos quânticos |

---

## Métricas de Comparação

### 8.1 Métricas para Otimização (TSP/VRP)

Ao comparar algoritmos nos artigos, registre:

1. **Qualidade da solução**: Razão entre solução encontrada e solução ótima conhecida (approximation ratio)
2. **Tempo de execução**: Wall-clock time (incluir tempo de compilação/transpilação para quânticos)
3. **Número de qubits**: Qubits lógicos vs. físicos necessários (N² variáveis binárias para TSP com N cidades)
4. **Profundidade do circuito**: Para gate-based (limita viabilidade em hardware NISQ)
5. **Número de cidades/nós**: Escala do problema testado
6. **Tipo de instância**: Aleatória, benchmark (TSPLIB), caso real de logística
7. **Taxa de sucesso (success rate)**: Fração de execuções que retornam solução factível
8. **Feasibility ratio**: Proporção de soluções que respeitam todas as restrições
9. **Optimality gap**: Diferença percentual entre solução encontrada e ótimo conhecido
10. **Sensibilidade a parâmetros**: Impacto de penalty λ, chain strength, profundidade p (QAOA)
11. **Robustez ao ruído**: Desempenho em hardware NISQ real vs. simulador ideal
12. **Tipo de abordagem**: Puro quântico vs. híbrido (horizontal hybrid quantum computing)
13. **Paradigma quântico**: QA (annealing) vs. GBC (gate-based) vs. Quantum-Inspired
14. **Embedding overhead**: Qubits físicos necessários para embedding no hardware (especialmente D-Wave)

### 8.2 Métricas para Quantum Machine Learning (QML)

#### Métricas de Desempenho Preditivo

| Métrica | Sigla | Descrição | Aplicação em Supply Chain |
|---------|-------|-----------|--------------------------|
| Mean Absolute Error | MAE | Erro absoluto médio entre previsão e valor real | Acurácia de previsão de demanda |
| Mean Absolute Percentage Error | MAPE | Erro percentual médio; interpretável por gestores | Benchmark de previsão de demanda |
| Root Mean Square Error | RMSE | Penaliza erros grandes; sensível a outliers | Previsão de séries de demanda com picos |
| Symmetric MAPE | sMAPE | Versão simétrica do MAPE, mais robusta | Comparação entre SKUs de escalas diferentes |
| R² (Coeficiente de Determinação) | R² | Variância explicada pelo modelo | Qualidade de ajuste em regressão de demanda |
| Accuracy / F1-Score / AUC-ROC | — | Métricas de classificação | Detecção de ruptura, classificação de risco |
| Cross-Entropy Loss | — | Loss de classificação probabilística | Treinamento de VQC/QNN para classificação |
| Mean Squared Error | MSE | Loss de regressão padrão | Treinamento de QNN para previsão contínua |

#### Métricas de Desempenho Quântico

| Métrica | Descrição | Relevância para QML |
|---------|-----------|-------------------|
| Circuit Depth (profundidade) | Número de camadas de portas quânticas; determina viabilidade NISQ | Circuitos mais profundos acumulam mais ruído; QML requer circuitos rasos |
| Circuit Width (largura) | Número de qubits utilizados | Limita escalabilidade; N features → N ou mais qubits |
| Number of Parameters | Número de parâmetros treináveis no PQC | Impacta capacidade e custo de treinamento clássico |
| Expressibility | Grau em que o PQC cobre o espaço de Hilbert | PQCs mais expressíveis têm maior capacidade de aprendizado |
| Entanglement Capability | Quantidade de entrelaçamento gerado pelo PQC | Correlaciona com expressibilidade e risco de barren plateau |
| Barren Plateau Score | Gradiente médio ao longo do treinamento; indica presença de platôs | Gradientes próximos de zero → treinamento falha; crítico para QNN deep |
| Quantum Kernel Alignment | Alinhamento entre kernel quântico e rótulos do problema | Qualidade do kernel quântico para QSVM/QKE |
| Fidelity Kernel Value | Produto interno quântico entre estados codificados | Base de cálculo para QSVM e QKE |
| Gate Error Rate | Taxa de erro por porta quântica (hardware NISQ) | Afeta diretamente acurácia de VQC/QNN em hardware real |
| T1 / T2 (coerência) | Tempo de relaxação e decoerência dos qubits | Limita profundidade máxima viável do circuito |

#### Métricas de Treinamento e Convergência

| Métrica | Descrição | Relevância para QML |
|---------|-----------|-------------------|
| Epochs / Iterations to Convergence | Número de iterações até estabilização do loss | Eficiência do treinamento clássico-quântico |
| Gradient Variance | Variância do gradiente durante o treinamento | Diagnóstico de barren plateaus |
| Classical Optimizer Calls | Número de chamadas ao circuito quântico pelo otimizador | Custo computacional total do loop híbrido |
| Shot Budget | Número de execuções do circuito para estimar gradientes | Custo de acesso ao hardware quântico |
| Training Time (Clássico + Quântico) | Wall-clock time total do pipeline híbrido | Comparação de viabilidade com ML clássico |
| Parameter Landscape Flatness | Curvatura do espaço de parâmetros | Barren plateaus causam landscapes planos |

#### Métricas de Comparação Quântico vs. Clássico

| Métrica | Descrição |
|---------|-----------|
| Quantum Advantage Ratio | Razão entre performance quântica e clássica (acurácia ou tempo) |
| Quantum Volume (QV) | Métrica IBM de capacidade geral do processador quântico; combina qubits, fidelidade e conectividade |
| CLOPS (Circuit Layer Operations per Second) | Velocidade de execução de camadas de circuito; relevante para QML iterativo |
| Classical Equivalence | Performance do QML comparada ao ML clássico equivalente (mesmo número de parâmetros) |
| Sample Complexity | Quantidade de amostras de treinamento necessárias para convergência |

### 8.3 Métricas Específicas por Problema

| Problema | Métricas Adicionais |
|----------|-------------------|
| VRP/CVRP | Número de veículos, capacidade, janelas de tempo, número de rotas |
| TSP/TSPTW | Custo total da rota, violação de time windows |
| Bin Packing | Número de bins utilizados, taxa de ocupação |
| Knapsack | Valor total, violação de capacidade |
| JSP/FJSP | Makespan, workload total, prioridade |
| Network Design | Custo de infraestrutura, cobertura de demanda |
| Fleet/TAP | Custo de manutenção, utilização de aeronaves |
| Previsão de Demanda (QML) | MAPE, RMSE, lead time coberto, horizonte de previsão |
| Controle de Inventário (QML) | Nível de serviço, fill rate, custo de carregamento, stockout rate |
| Classificação de Ruptura (QML) | Precision, Recall, F1-Score, AUC-ROC |
| Geração de Dados Sintéticos (qGAN/QCBM) | KL-divergence, Wasserstein distance entre distribuição real e gerada |

---

## Tendências Observadas na Literatura

### Tendências em Otimização (TSP/VRP)

- **QAOA e Quantum Annealing** são os mais estudados para TSP e VRP
- **Abordagens híbridas** crescem em popularidade (2021–presente) e dominam a literatura — a maioria das soluções publicadas são híbridas (Phillipson, 2025)
- **QA domina**: a maioria das publicações usa Quantum Annealing como paradigma principal, devido ao maior número de qubits disponíveis e ao full-stack oferecido pela D-Wave
- **QAOA e VQE** são o segundo paradigma mais usado, porém ainda muito limitados em performance
- **Grover's Search** é muito citado mas pouco implementado para TSP (requer muitos qubits)
- **D-Wave** domina os trabalhos experimentais com annealing (2000Q e Advantage com 5640 qubits)
- **IBM Quantum** domina gate-based experimental (até 127 qubits)
- **Gap significativo** entre escala teórica e experimental (artigos testam 5–30 cidades vs. TSPs reais com centenas/milhares)
- **Fluxo principal de pesquisa** começa por volta de 2020 (Phillipson, 2025)
- **Routing e Scheduling** são os tópicos mais cobertos; **Prediction/QML** tem poucos trabalhos e é identificado como lacuna
- **Metaheurísticas quânticas** (QACO, Quantum Genetic) estão emergindo como nova tendência
- **Quantum Reinforcement Learning** para VRP é ainda prova de conceito, mas demonstra potencial
- **Poucos artigos** demonstram vantagem clara sobre métodos clássicos — a maioria indica "potencial" futuro
- **Sensibilidade a parâmetros** (penalty λ, chain strength, profundidade p) é um desafio transversal pouco explorado

### Tendências em QML para Supply Chain / Inventário

- **PennyLane** é o framework dominante em pesquisa de QML, por suportar diferenciação automática e múltiplos backends
- **VQC e QNN** são os modelos QML mais estudados para tarefas de previsão e classificação
- **QSVM / QKE** têm respaldo teórico mais forte, mas kernels quânticos ainda não demonstram vantagem consistente sobre kernels clássicos em dados reais
- **Barren Plateaus** são o principal desafio técnico em training de QNN profundas — gradientes desaparecem exponencialmente com número de qubits
- **QLSTM e Quantum Reservoir Computing** são tendências emergentes para séries temporais de demanda
- **qGAN e QCBM** estão sendo explorados para geração de dados sintéticos de supply chain com distribuições complexas
- **QRL para controle de inventário** está em estágio inicial — poucos artigos, escalas mínimas
- **Lacuna identificada**: QML aplicado especificamente à otimização de inventário (níveis de estoque, políticas de reposição) é subrepresentado — a maioria dos trabalhos foca em routing ou previsão genérica
- **Codificação de dados** (amplitude encoding, angle encoding, IQP encoding) é um pré-requisito crítico e pouco padronizado na literatura
- **Hardware-efficient ansatz** é preferido para QML em NISQ por menor profundidade de circuito
- **Mitigação de erros** (via Mitiq, Zero-Noise Extrapolation) começa a ser adotada em experimentos QML em hardware real
- **Quantum advantage em QML** não foi demonstrado para problemas de supply chain — pesquisas apontam para vantagem em regimes específicos de dados de alta dimensão

---

## Referência Bibliográfica Principal

- Phillipson, F. (2025). "Quantum Computing in Logistics and Supply Chain Management - an Overview". Maastricht University / TNO. arXiv:2042.17520v2. — Overview de 80+ artigos cobrindo routing, network design, fleet maintenance, cargo loading, prediction e scheduling.
- Biamonte, J. et al. (2017). "Quantum Machine Learning". *Nature*, 549, 195–202. — Artigo seminal em QML.
- Cerezo, M. et al. (2021). "Variational Quantum Algorithms". *Nature Reviews Physics*, 3, 625–644. — Review de VQAs incluindo VQC e QNN.
- Schuld, M., & Killoran, N. (2019). "Quantum Machine Learning in Feature Hilbert Spaces". *Physical Review Letters*, 122, 040504. — Base teórica para QSVM e kernels quânticos.
- McClean, J. R. et al. (2018). "Barren Plateaus in Quantum Neural Network Training Landscapes". *Nature Communications*, 9, 4812. — Artigo de referência sobre barren plateaus em QNN.
- Jerbi, S. et al. (2023). "Quantum Machine Learning Beyond Kernel Methods". *Nature Communications*, 14, 517. — Análise crítica das limitações de QML atual.
- Bausch, J. (2020). "Recurrent Quantum Neural Networks". *NeurIPS 2020*. — Base para QLSTM.
