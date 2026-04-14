---
name: quantum-inventory-qml-research
description: "Skill para pesquisadores em Quantum Machine Learning (QML) aplicado a previsão e controle de inventário em logística e supply chain. Use esta skill sempre que o usuário mencionar: artigo científico sobre QML, previsão de demanda com computação quântica, controle de inventário quântico, quantum neural networks para supply chain, revisão exploratória de QML em logística, levantamento bibliográfico de algoritmos quânticos para previsão, busca em bases como Lens.org, pesquisa de palavras-chave acadêmicas, ou qualquer etapa de construção de artigo técnico-científico sobre QML para logística. Também dispare quando o usuário pedir tabelas de revisão bibliográfica, análise de distribuição de artigos, comparação de modelos clássicos vs quânticos vs híbridos para forecasting, ou formatação em linguagem acadêmica ABNT/IEEE. Útil para mestrado profissional, orientação de pesquisa, e entregas parciais ao orientador."
---

# Quantum Inventory & QML Research — Skill para Artigo Científico

## Visão Geral

Esta skill guia a construção de um artigo técnico-científico sobre **Quantum Machine Learning (QML) aplicado a previsão de demanda e controle de inventário** em logística e supply chain management. O fluxo segue etapas de entrega típicas de um Mestrado Profissional.

### Origem do Tema

O tema foi identificado como lacuna de pesquisa durante a Fase 1 (Revisão Exploratória) do projeto anterior sobre TSP quântico:
- A revisão bibliográfica de 3.696 artigos sobre TSP + Computação Quântica revelou que **QML + Supply Chain** possui apenas ~79 artigos — campo emergente com oportunidade de contribuição original
- O artigo de referência (Phillipson, 2025) confirma: "There are many papers on QML and prediction, however only one on a direct application within logistics and supply chain optimisation"
- Principais trabalhos identificados na lacuna: QAmplifyNet (Jahin et al.), Quantised Policy Iteration (Jiang et al.), capítulos de Sehrawat, Gutta et al., e Koushik et al.

---

## Contexto do Pesquisador

- **Programa**: Mestrado Profissional em Gestão de Tecnologia e Inovação
- **Instituição**: SENAI CIMATEC
- **Tema anterior**: TSP com Computação Quântica (Fase 1 concluída)
- **Tema atual**: QML para previsão de demanda e controle de inventário em logística
- **Área de aplicação**: Logística e Supply Chain Management
- **Entregável final**: Artigo técnico-científico
- **Fluxo**: Entregas parciais ao professor orientador

---

## Etapas do Projeto

O artigo é construído em etapas sequenciais. Identifique em qual etapa o usuário está e execute as instruções correspondentes.

### Etapa 1 — Revisão Exploratória

Esta é a etapa de levantamento bibliográfico. Siga o checklist abaixo:

#### 1.1 Definição de Palavras-Chave

Monte combinações de palavras-chave em inglês (padrão acadêmico internacional). Leia o arquivo `references/keywords_guide.md` para a lista completa de termos sugeridos. As combinações devem cruzar três eixos:

| Eixo | Exemplos de termos |
|------|-------------------|
| Problema | "Demand Forecasting", "Inventory Control", "Backorder Prediction", "Supply Chain Forecasting" |
| Tecnologia | "Quantum Machine Learning", "Quantum Neural Network", "Variational Quantum Circuit", "Hybrid Quantum-Classical" |
| Aplicação | "Supply Chain Management", "Logistics", "Inventory Management", "Warehouse" |

Gere uma tabela de palavras-chave vs. total de artigos encontrados:

| # | String de Busca | Base | Filtro | Total de Artigos |
|---|----------------|------|--------|-----------------|
| 1 | "Quantum Machine Learning" AND "Demand Forecasting" | Lens.org | Scholarly Works | — |
| 2 | "Quantum Neural Network" AND "Supply Chain" | Lens.org | Scholarly Works | — |
| ... | ... | ... | ... | — |

O campo "Total de Artigos" deve ser preenchido pelo pesquisador após executar a busca.

#### 1.2 Busca em Bases Acadêmicas

Bases recomendadas (em ordem de prioridade):
1. **Lens.org** — Filtro: "Scholarly Works" (base principal)
2. **IEEE Xplore** — Conferências e journals de computação
3. **ACM Digital Library** — Algoritmos e machine learning
4. **arXiv** — Preprints recentes (quant-ph, cs.LG, cs.AI)
5. **Scopus / Web of Science** — Métricas de impacto

Para cada base, registre: número total de resultados, filtros aplicados, período coberto.

#### 1.3 Distribuição dos Artigos

Analise e produza visualizações (tabelas ou gráficos) de:
- Distribuição por **ano de publicação** (tendência temporal)
- Distribuição por **tipo** (journal, conferência, preprint, capítulo de livro)
- Distribuição por **país/instituição** de origem
- Distribuição por **base de dados** de origem
- Distribuição por **subárea** (demand forecasting, inventory control, predictive maintenance, backorder)

#### 1.4 Mapeamento de Algoritmos e Modelos QML

Classifique os algoritmos e modelos QML encontrados em:

| Categoria | Algoritmos/Modelos | Frequência nos Artigos |
|-----------|-------------------|----------------------|
| Quantum Neural Networks (QNN) | QAmplifyNet, VQC, Parameterized Quantum Circuits | — |
| Quantum Kernel Methods | QSVM, Quantum Kernel Estimation | — |
| Quantum Reinforcement Learning | Quantised Policy Iteration, QDRL | — |
| Hybrid Quantum-Classical | Quantum Transfer Learning, Hybrid QNN | — |
| Quantum-Inspired | Quantum-Inspired Neural Networks, Tensor Networks | — |
| Clássico (baseline) | LSTM, ARIMA, Random Forest, XGBoost, Classical NN | — |

Marque os **mais utilizados** e **menos utilizados** na literatura para previsão em logística.

#### 1.5 Hardware e Simuladores

Mapeie os computadores quânticos e simuladores citados nos artigos:

| Hardware / Simulador | Fabricante | Tipo | Qubits (máx.) | Artigos que citam |
|---------------------|-----------|------|---------------|------------------|
| IBM Quantum (Eagle/Heron) | IBM | Gate-based | 127–133 | — |
| Qiskit / Qiskit Aer | IBM | Framework/Simulador | variável | — |
| PennyLane | Xanadu | Framework | variável | — |
| Amazon Braket | AWS | Cloud/Simulador | variável | — |
| Cirq | Google | Framework | variável | — |
| qBraid | qBraid | Plataforma Cloud | variável | — |
| ... | ... | ... | ... | — |

#### 1.6 Tabela-Resumo da Revisão

Consolide tudo em uma tabela-resumo por artigo:

| # | Autores | Ano | Título | Modelo QML | Hardware/Sim. | Qubits | Problema Logístico | Métricas (F1/Acc/MSE) | Abordagem | Base |
|---|---------|-----|--------|-----------|--------------|--------|-------------------|----------------------|-----------|------|
| 1 | — | — | — | — | — | — | — | — | Quântica/Híbrida | — |

---

### Etapa 2 — Fundamentação Teórica

Após a revisão exploratória, construa a seção teórica do artigo:

1. **Previsão de Demanda e Controle de Inventário**: Definição do problema, métodos clássicos (ARIMA, LSTM, ML), desafios com dados desbalanceados e séries temporais complexas
2. **Computação Quântica**: Conceitos fundamentais (qubit, superposição, emaranhamento, portas quânticas, circuitos parametrizados)
3. **Quantum Machine Learning**: VQC, Quantum Kernels, QNN, Quantum Transfer Learning — explicação e aplicabilidade a problemas de previsão
4. **Sistemas Híbridos Quantum-Classical**: Arquitetura híbrida para ML (ex: QAmplifyNet), vantagens em datasets pequenos/desbalanceados, limitações atuais (número de qubits, ruído)
5. **Contexto Logístico**: Aplicações em demand forecasting, inventory control, backorder prediction, predictive maintenance em supply chain

Use linguagem técnica de artigo científico. Consulte `references/writing_style.md` para o guia de estilo.

---

### Etapa 3 — Metodologia

Descreva a metodologia da revisão sistemática/exploratória:
- Protocolo de busca (strings, bases, filtros, critérios de inclusão/exclusão)
- Critérios de seleção dos artigos
- Método de análise (qualitativo, quantitativo, bibliométrico)
- Ferramentas utilizadas (Lens.org, Python/pandas, Streamlit, etc.)
- Justificativa da escolha do tema (lacuna identificada na revisão de TSP)

---

### Etapa 4 — Resultados e Discussão

Apresente os achados da revisão:
- Tendências identificadas (crescimento de publicações em QML para supply chain)
- Gaps na literatura (escassez de aplicações diretas de QML em previsão logística)
- Comparação de desempenho: modelos QML vs. clássicos vs. híbridos (métricas: F1, AUC-ROC, accuracy, MSE)
- Análise de viabilidade: tamanho dos datasets, número de qubits necessários, desempenho em dados desbalanceados
- Limitações atuais do hardware quântico para ML em escala real
- Implicações para logística e supply chain management
- Oportunidades de contribuição original

---

### Etapa 5 — Montagem Final do Artigo

Estrutura padrão do artigo científico:

```
1. Título
2. Resumo / Abstract
3. Palavras-chave / Keywords
4. Introdução
5. Fundamentação Teórica
6. Metodologia
7. Resultados e Discussão
8. Conclusão
9. Referências Bibliográficas
```

Ao gerar o documento final:
- Leia o skill `docx` em `/mnt/skills/public/docx/SKILL.md` para criar o .docx
- Use formatação acadêmica (fonte Times New Roman 12pt, espaçamento 1.5, margens 2.5cm)
- Siga normas ABNT ou IEEE conforme orientação do professor
- Inclua todas as tabelas geradas nas etapas anteriores

---

## Instruções de Estilo e Linguagem

- Use **terceira pessoa** e **voz passiva** quando possível ("foi realizado", "observou-se")
- Evite linguagem coloquial; priorize termos técnicos
- Cite autores no formato (AUTOR, ANO) para ABNT ou [número] para IEEE
- Mantenha parágrafos concisos e conectados por transições lógicas
- Use siglas definidas na primeira ocorrência: "Quantum Machine Learning (QML)"
- Consulte `references/writing_style.md` para exemplos detalhados

---

## Geração de Arquivos

Quando o usuário pedir para gerar documentos:

- **Tabelas de revisão** → Gere como `.docx` ou `.xlsx` (leia o skill correspondente)
- **Artigo completo** → Gere como `.docx` (leia `/mnt/skills/public/docx/SKILL.md`)
- **Apresentação para orientador** → Gere como `.pptx` (leia `/mnt/skills/public/pptx/SKILL.md`)
- **Scripts de análise** → Gere em Python (pandas, matplotlib)

---

## Referências Bundled

| Arquivo | Quando ler |
|---------|-----------|
| `references/keywords_guide.md` | Ao definir palavras-chave (Etapa 1.1) |
| `references/algorithms_reference.md` | Ao mapear algoritmos (Etapa 1.4) |
| `references/writing_style.md` | Ao redigir qualquer seção do artigo |
| `scripts/analysis_template.py` | Quando o usuário pedir análise bibliométrica |

## Artigos-Chave Identificados (Phillipson, 2025 — Seção 3.6)

| Autores | Foco | Modelo/Abordagem |
|---------|------|-----------------|
| Jahin et al. [69] | Backorder prediction em SCM | QAmplifyNet (hybrid quantum-classical NN), F1=94%/75%, AUC-ROC=79.85% |
| Jiang et al. [71] | Inventory control | Quantised Policy Iteration, IBM Qiskit + qBraid |
| Sehrawat [140] | Demand prediction em supply chain | QML para previsão de demanda |
| Gutta et al. [60] | Supply chain forecasting | AI + QML integrado |
| Koushik et al. [78] | Predictive maintenance em supply chain | Deep learning (CNN, RNN) para manutenção preditiva |
