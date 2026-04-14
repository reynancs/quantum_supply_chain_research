# Guia de Palavras-Chave — QML + Previsão e Controle de Inventário em Logística

## Origem do Tema

Este guia substitui o anterior (TSP + Computação Quântica) após a identificação de lacuna na Fase 1:
- **Lacuna**: "QML para previsão em logística" — apenas ~79 artigos em QML + Supply Chain
- **Fonte**: Phillipson (2025), Seção 3.6 — "Prediction and Inventory Control"
- **Motivação**: "There are many papers on QML and prediction, however only one on a direct application within logistics and supply chain optimisation"

## Eixos de Busca

As palavras-chave devem combinar pelo menos 2 dos 3 eixos abaixo usando operador AND.

### Eixo 1 — Problema (Previsão e Controle em Logística)
- "Demand Forecasting"
- "Demand Prediction"
- "Inventory Control"
- "Inventory Optimization"
- "Inventory Management"
- "Backorder Prediction"
- "Supply Chain Forecasting"
- "Predictive Maintenance"
- "Time Series Forecasting"
- "Stock Management"
- "Supply Chain Disruption"
- "Lead Time Prediction"
- "Sales Forecasting"

### Eixo 2 — Tecnologia (QML e Computação Quântica)
- "Quantum Machine Learning"
- "Quantum Neural Network" / "QNN"
- "Variational Quantum Circuit" / "VQC"
- "Quantum Kernel"
- "Quantum Support Vector Machine" / "QSVM"
- "Parameterized Quantum Circuit" / "PQC"
- "Quantum Transfer Learning"
- "Quantum Reservoir Computing"
- "Quantum Reinforcement Learning"
- "Hybrid Quantum-Classical"
- "Quantum Computing"
- "Quantum-Inspired"
- "Quantum Deep Learning"
- "Pennylane"
- "Qiskit"

### Eixo 3 — Aplicação (Logística e Supply Chain)
- "Supply Chain Management"
- "Supply Chain"
- "Logistics"
- "Supply Chain Optimization"
- "Warehouse Management"
- "Distribution Network"
- "Operations Management"
- "E-commerce"
- "Retail"
- "Manufacturing"
- "Route Optimization"
- "Load Balancing"
- "Vehicle Routing"
- "Supplier Risk Management"
- "Supplier Risk"
- "Supplier Selection"

## Combinações Recomendadas (prioridade alta para baixa)

### Prioridade Alta — QML + Previsão/Inventário + Logística (tema central)

Strings que combinam diretamente QML com previsão ou inventário em contexto logístico. Estas são as mais relevantes para o artigo.

| # | String de Busca | Base | Filtro | Total de Artigos |
|---|----------------|------|--------|-----------------|
| 1 | "Quantum Machine Learning" AND "Supply Chain" | Lens.org | Scholarly Works | — |
| 2 | "Quantum Machine Learning" AND "Demand Forecasting" | Lens.org | Scholarly Works | — |
| 3 | "Quantum Machine Learning" AND "Inventory" | Lens.org | Scholarly Works | — |
| 4 | "Quantum Machine Learning" AND "Logistics" | Lens.org | Scholarly Works | — |
| 5 | "Quantum Neural Network" AND "Supply Chain" | Lens.org | Scholarly Works | — |
| 6 | "Quantum Computing" AND "Demand Forecasting" | Lens.org | Scholarly Works | — |
| 7 | "Quantum Computing" AND "Demand Prediction" | Lens.org | Scholarly Works | — |
| 8 | "Hybrid Quantum" AND "Supply Chain" AND "Prediction" | Lens.org | Scholarly Works | — |
| 9 | "Quantum Computing" AND "Inventory Control" | Lens.org | Scholarly Works | — |

### Prioridade Média — QML + Previsão (contexto mais amplo)

Strings que capturam QML aplicado a previsão em contextos mais específicos ou supply chain sem especificar previsão. Ampliam o corpus e contextualizam o estado-da-arte.

> **Nota (2026-04-11):** As strings #10-#14 foram removidas após análise de precisão na triagem. Essas strings amplas (QML + Time Series/Forecasting/Prediction, sem termo de supply chain) retornaram 98,3% de falsos positivos — artigos de QML aplicado a clima, finanças, saúde, energia e outros domínios fora do escopo. Apenas 1,7% (7 de 421 artigos exclusivos) eram relevantes para supply chain. A remoção trata a causa raiz do ruído no corpus em vez de expandir critérios de exclusão indefinidamente.

| # | String de Busca | Base | Filtro | Total de Artigos |
|---|----------------|------|--------|-----------------|
| ~~10~~ | ~~"Quantum Machine Learning" AND "Time Series"~~ | — | — | REMOVIDA |
| ~~11~~ | ~~"Quantum Machine Learning" AND "Forecasting"~~ | — | — | REMOVIDA |
| ~~12~~ | ~~"Quantum Neural Network" AND "Forecasting"~~ | — | — | REMOVIDA |
| ~~13~~ | ~~"Variational Quantum" AND "Forecasting"~~ | — | — | REMOVIDA |
| ~~14~~ | ~~"Quantum Machine Learning" AND "Prediction"~~ | — | — | REMOVIDA |
| 15 | "Quantum Reinforcement Learning" AND "Inventory" | Lens.org | Scholarly Works | — |
| 16 | "Quantum Computing" AND "Backorder" | Lens.org | Scholarly Works | — |
| 17 | "Quantum Computing" AND "Supply Chain Management" | Lens.org | Scholarly Works | — |
| 18 | "Quantum Kernel" AND "Time Series" | Lens.org | Scholarly Works | — |

### Prioridade Baixa — Complementares e Exploratórias

Strings mais amplas ou nicho que complementam a busca. Incluem quantum-inspired, hardware específico e aplicações adjacentes.

| # | String de Busca | Base | Filtro | Total de Artigos |
|---|----------------|------|--------|-----------------|
| 19 | "Quantum Computing" AND "Predictive Maintenance" AND "Supply Chain" | Lens.org | Scholarly Works | — |
| 20 | "Quantum-Inspired" AND "Demand Forecasting" | Lens.org | Scholarly Works | — |
| 21 | "Quantum Reservoir Computing" AND "Time Series" | Lens.org | Scholarly Works | — |
| 22 | "Quantum Support Vector Machine" AND "Forecasting" | Lens.org | Scholarly Works | — |
| 23 | "Quantum Computing" AND "Supply Chain Resilience" | Lens.org | Scholarly Works | — |
| 24 | "Quantum" AND "Inventory Optimization" AND "Machine Learning" | Lens.org | Scholarly Works | — |
| 25 | "Quantum Machine Learning" AND "Classification" AND "Supply Chain" | Lens.org | Scholarly Works | — |
| 26 | "QAmplifyNet" AND "Backorder Prediction" | Lens.org | Scholarly Works | — |
| 27 | "Hybrid Quantum Neural Networks" AND "Backorder Prediction" | Lens.org | Scholarly Works | — |
| 28 | "Hybrid Quantum Neural Networks" AND "Supply Chain" | Lens.org | Scholarly Works | — |

### Rastreamento por Área de Aplicação ML em Supply Chain

Strings para mapear o volume de pesquisa QML por área de aplicação. Objetivo: identificar lacunas comparando o volume entre áreas.

| # | Área de Aplicação | String de Busca | Base | Filtro | Total de Artigos |
|---|-------------------|----------------|------|--------|-----------------|
| 29 | Demand Forecasting | "Quantum" AND "Demand Forecasting" AND "Supply Chain" | Lens.org | Scholarly Works | — |
| 30 | Inventory Optimization | "Quantum" AND "Inventory Optimization" | Lens.org | Scholarly Works | — |
| 31 | Route Optimization | "Quantum" AND "Route Optimization" AND "Supply Chain" | Lens.org | Scholarly Works | — |
| 32 | Route Optimization | "Quantum Machine Learning" AND "Vehicle Routing" | Lens.org | Scholarly Works | — |
| 33 | Load Balancing | "Quantum" AND "Load Balancing" AND "Logistics" | Lens.org | Scholarly Works | — |
| 34 | Supplier Risk Management | "Quantum" AND "Supplier Risk" | Lens.org | Scholarly Works | — |
| 35 | Supplier Risk Management | "Quantum Computing" AND "Supplier Risk Management" | Lens.org | Scholarly Works | — |

## Justificativa por String

| # | Justificativa |
|---|---------------|
| 1 | Reproduz a string #26 do TSP que identificou a lacuna (79 artigos). String âncora do novo tema |
| 2 | Cruza QML diretamente com demand forecasting — tema central do artigo |
| 3 | QML + Inventory captura trabalhos como Jiang et al. (quantised policy iteration para inventory control) |
| 4 | QML + Logistics amplia o escopo para capturar aplicações logísticas diversas |
| 5 | QNN é a arquitetura principal (ex: QAmplifyNet de Jahin et al.) |
| 6–7 | Quantum Computing + Demand (forecasting/prediction) — captura trabalhos que não usam o termo "QML" |
| 8 | Abordagens híbridas com foco em previsão — tendência dominante na área |
| 9 | Inventory control com quantum computing — captura Jiang et al. e trabalhos similares |
| 10–14 | **REMOVIDAS** — precisão de 1,7% para supply chain; 98,3% falsos positivos (QML aplicado a clima, finanças, saúde, energia etc.) |
| 15 | QRL para inventário — abordagem emergente identificada em Phillipson (2025) |
| 16 | Backorder prediction — problema específico abordado por Jahin et al. com QAmplifyNet |
| 17 | String ampla que captura o overview de Phillipson (2025) e similares |
| 18 | Quantum Kernels para séries temporais — método QML alternativo |
| 19 | Predictive maintenance em supply chain — captura Koushik et al. |
| 20 | Quantum-Inspired para demand forecasting — alternativa sem hardware quântico real |
| 21 | Quantum Reservoir Computing para séries temporais — abordagem QML pouco explorada |
| 22 | QSVM para forecasting — kernel methods quânticos aplicados a previsão |
| 23 | Supply chain resilience — tema crescente pós-pandemia com potencial para QML |
| 24–25 | Combinações exploratórias para capturar artigos com nomenclatura variada |
| 26 | QAmplifyNet — busca-referência para o artigo de Jahin et al. (backorder prediction); retornou 4 artigos |
| 27–28 | Hybrid QNN — variações de nomenclatura do modelo de Jahin et al.; retornaram 0 artigos |
| 29 | Demand Forecasting — área com maior volume esperado; baseline para comparar entre áreas |
| 30 | Inventory Optimization — captura Jiang et al. e variações de nomenclatura |
| 31–32 | Route Optimization / Vehicle Routing — adjacente ao TSP, sobreposição com otimização combinatória quântica |
| 33 | Load Balancing — termo secundário de Route Optimization; volume esperado baixo em logística |
| 34–35 | Supplier Risk Management — área com lacuna esperada; cobre avaliação de risco, seleção de fornecedores e Quantum Computing amplo |

## Filtros Recomendados por Base

### Lens.org
- Document Type: "Scholarly Works"
- Subject: Computer Science, Physics, Operations Research, Business
- Year: 2018–2026 (QML para logística é campo muito recente)
- Open Access: filtrar separadamente para ver disponibilidade

### IEEE Xplore
- Content Type: Conferences, Journals
- Topic: Quantum Computing, Machine Learning, Supply Chain

### arXiv
- Categorias: quant-ph, cs.LG, cs.AI, cs.ET
- Período: últimos 5 anos (campo muito recente)

## Dicas de Busca

1. Use aspas para termos compostos exatos: "Quantum Machine Learning"
2. Use OR para sinônimos: ("Demand Forecasting" OR "Demand Prediction")
3. Comece com buscas amplas e refine progressivamente
4. Registre o número exato de resultados para cada string no momento da busca
5. Anote a data da busca (os resultados mudam com o tempo)
6. **Atenção**: como o campo é emergente, espere volumes baixos em muitas strings — isso é evidência da lacuna
7. Strings com 0–10 resultados são tão informativas quanto strings com centenas (documentam o gap)
