# Quantum Machine Learning Aplicado a Supply Chain e Inventário — Revisão Bibliográfica Sistemática

Revisão bibliográfica sistemática seguindo o protocolo **PRISMA-ScR** (Preferred Reporting Items for Systematic reviews and Meta-Analyses extension for Scoping Reviews) sobre a aplicação de **Quantum Machine Learning (QML)** a problemas de Supply Chain Management, com foco em **predição de backorder**, **previsão de demanda** e **controle de inventário**.

**Programa:** Mestrado Profissional em Gestão de Tecnologia e Inovação — SENAI CIMATEC
**Status:** Fase 1 (Exploração Bibliográfica) concluída · Fase 2 (Full-text Review) em andamento

---

## 1. Contexto e Motivação

A gestão de supply chain envolve decisões sob incerteza em múltiplas dimensões — demanda volátil, lead-times variáveis, restrições de capacidade, e risco de ruptura (*backorder*/*stockout*). Modelos clássicos de Machine Learning (XGBoost, LSTM, Random Forest) dominam o estado-da-arte em previsão de demanda e classificação de risco de ruptura, mas enfrentam limites de escalabilidade e representação em regimes de alta dimensionalidade ou forte correlação não-linear entre features.

**Quantum Machine Learning (QML)** — arquiteturas como *Quantum Neural Networks* (QNN), *Variational Quantum Classifiers* (VQC), *Quantum Support Vector Machines* (QSVM), *Quantum Kernels* e *Quantum Reinforcement Learning* (QRL) — propõe-se a explorar espaços de Hilbert de dimensionalidade exponencial para codificação de features e cálculo de kernels, oferecendo potencial *speedup* e capacidade representacional adicional mesmo no regime atual de *Noisy Intermediate-Scale Quantum* (NISQ).

Esta revisão mapeia o estado-da-arte da interseção **QML × Supply Chain / Inventory Management**, identificando lacunas que possam justificar contribuição original da dissertação.

---

## 2. Objetivos

### Objetivo geral
Mapear, caracterizar e sintetizar a literatura que aplica QML a problemas de supply chain — com ênfase em previsão de demanda, controle de inventário e predição de backorder — e identificar oportunidades de pesquisa original.

### Objetivos específicos
1. Construir um corpus bibliográfico reprodutível a partir da base Lens.org via 35 *search strings* booleanas.
2. Aplicar triagem automatizada em duas fases (metadados + abstract) seguindo PRISMA-ScR, com critérios de exclusão (CE-1 a CE-5) explícitos.
3. Classificar automaticamente os artigos elegíveis em 13 categorias de `tipo_problema`.
4. Realizar *full-text review* dos elegíveis para extração estruturada (método QML, baseline clássico, dataset, métricas, hardware, resultado).
5. Publicar um **dashboard Streamlit** como artefato reproduzível que documente todo o pipeline e permita exploração interativa do corpus em cada etapa.

---

## 3. Pipeline da Pesquisa

```
 Extração Lens.org           Deduplicação              Análise                Triagem                Revisão
 (35 strings)          →    (DOI + Título)        →   Bibliométrica    →    PRISMA-ScR       →    Bibliográfica
 ─────────────              ─────────────             ────────────          ────────────           ────────────
 3.774 registros            2.471 únicos              Perfil do              1.231 → 261            261 artigos
 brutos                     (1.303 removidos)         corpus                 elegíveis              full-text review
```

| Etapa | Entrada | Saída | Script | CSV |
|---|---|---|---|---|
| 0. Busca | 35 *search strings* no Lens.org | 35 CSVs brutos (`string-NN.csv`) | — | `data/export_lens/` |
| 1. Deduplicação | 3.774 brutos | 2.471 únicos | `src/deduplicar_artigos.py` | `artigos_unicos.csv`, `resumo_deduplicacao.csv` |
| 2. Bibliometria | 2.471 únicos | Perfil agregado (produção, impacto, temas) | `src/analise_bibliometrica.py` | `data/resultados_bibliometria/` |
| 3. Triagem PRISMA | 1.231 únicos (após remoção de strings ruidosas) | 261 elegíveis | `src/triagem_artigos.py` + `src/classificar_problema.py` | `artigos_unicos_triagem.csv` |
| 4. Revisão | 261 elegíveis | Extração manual | `src/gerar_tabela_revisao.py` (geração) + preenchimento manual | `tabela_revisao_bibliografica.xlsx` |

---

## 4. Critérios de Exclusão (PRISMA-ScR)

| Código | Critério | Fase | Descrição |
|---|---|---|---|
| **CE-1** | Otimização quântica pura | 1 e 2 | Artigos de otimização combinatória (QAOA, QA) sem componente de ML. |
| **CE-2** | Apenas trabalho futuro | 2 | QML mencionado apenas na seção de *future work*, sem experimento. |
| **CE-3** | Domínio fora de escopo | 1 e 2 | Domínios não-supply-chain (medical imaging, drug discovery, finance, etc.) **com safety net** — revogado se texto também mencionar SC/logística/inventário. |
| **CE-3 (forte)** | Domínio claro no título | 1 | *Hard excludes* no título (blockchain, patent review, nanotechnology, women in quantum, drug-target, road traffic, etc.). **Sem safety net** — não é revogado por menção a supply chain. |
| **CE-5** | Tipo de publicação não-substantivo | 1 | Editorials, posters, erratum, *book reviews*. |

**Refinamento iterativo (5 iterações):** Iter. 1 original (~27% precisão) → Iter. 2 remoção das strings #10–#14 (~58%) → Iter. 3 dedup cross-DOI (~80%) → Iter. 4 CE-3 forte (~88%) → Iter. 5 revisão manual (~90%+).

---

## 5. Dashboard Interativo

O dashboard Streamlit é a **interface principal** de exploração do corpus e documentação viva do pipeline. Organizado em 7 abas narrativas que seguem a lógica do processo de pesquisa:

1. **🏠 Pipeline** — Funil macro (3.774 → 2.471 → 261 → N revisados) + KPIs globais.
2. **🔎 Estratégia de Busca** — Volume por string, heatmap 35×35 de co-ocorrência, tabela de referência das strings.
3. **🧹 Deduplicação** — KPIs, mini-funil, detalhamento das remoções (DOI, título, cross-DOI).
4. **📚 Análise Bibliométrica** — Produção temporal, tipos de publicação, Open Access, Top 20 mais citados (com *Citações/Ano* ajustado), Top 30 Fields of Study, leaderboard por *Citações/Ano*, WordCloud de keywords.
5. **✅ Triagem PRISMA-ScR** — Funil de 3 estágios, exclusões por critério (CE-1 a CE-5), evolução das 5 iterações (dual-axis), distribuição por `tipo_problema`, tabela filtrável dos elegíveis.
6. **📖 Revisão Bibliográfica** — Progresso do preenchimento manual, síntese por `relevancia_final` / `metodo_qml` / `hardware`, heatmap de concordância `tipo_problema_auto` × `problema_validado`, tabela com filtros por revisão e exportação do corpus de alta relevância.
7. **🎯 Conclusões & Próximos Passos** — Síntese dos achados e roadmap da pesquisa.

### Executar localmente

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar o dashboard
streamlit run src/dashboard_bibliometrico.py
```

O dashboard fica disponível em `http://localhost:8501`.

### Integração ao vivo com a planilha de revisão

A aba **Revisão Bibliográfica** lê diretamente `data/tabela_revisao_bibliografica.xlsx`. O `mtime` (file modification time) do arquivo é usado como chave do cache Streamlit — **basta salvar a planilha no Excel e recarregar (`R`) o dashboard** para ver os novos preenchimentos. Não é necessário limpar cache manualmente.

---

## 6. Estrutura do Repositório

```
quantum_inventory_qml_research/
├── README.md                                  Este arquivo
├── requirements.txt                           Dependências Python
│
├── data/                                      Dados da pesquisa
│   ├── export_lens/                           35 CSVs brutos do Lens.org (string-01..35.csv)
│   ├── artigos_unicos.csv                     2.471 artigos pós-deduplicação
│   ├── artigos_unicos_triagem.csv             2.471 artigos com decisões PRISMA-ScR
│   ├── resumo_deduplicacao.csv                KPIs da deduplicação
│   ├── resumo_por_string.csv                  35 strings com código, descrição e volume
│   ├── tabela_revisao_bibliografica.xlsx      Planilha viva da revisão manual (fonte de verdade)
│   └── resultados_bibliometria/               Outputs agregados da análise bibliométrica
│
├── src/                                       Código-fonte
│   ├── deduplicar_artigos.py                  Etapa 1 — Deduplicação (DOI → título → cross-DOI)
│   ├── analise_bibliometrica.py               Etapa 2 — Análise bibliométrica agregada
│   ├── triagem_artigos.py                     Etapa 3 — Triagem PRISMA-ScR (Fase 1 + Fase 2)
│   ├── classificar_problema.py                Etapa 3 — Classificação em 13 tipos_problema
│   ├── gerar_tabela_revisao.py                Etapa 4 — Gera planilha inicial da revisão
│   └── dashboard_bibliometrico.py             Dashboard Streamlit (7 abas)
│
├── docs/                                      Documentação e protocolos
│   ├── protocolo_triagem.md                   Protocolo detalhado da triagem PRISMA-ScR
│   ├── protocolo_revisao_bibliografica.md     Protocolo da extração manual (full-text)
│   ├── resumo_triagem_artigos.md              Resumo estatístico das 5 iterações
│   ├── resumo_pesquisa_bibliografica.md       Narrativa metodológica geral
│   ├── diagrama_prisma_scr.md                 Diagrama PRISMA-ScR em Mermaid
│   ├── pesquisa_palavras_chave_inventory_qml.xlsx   Planilha de construção das 35 strings
│   └── referencia_bibliografica/              PDFs dos artigos lidos
│
├── ai/                                        Contexto para agentes de IA (Skills)
│   ├── SKILL.md                               Definição da skill quantum-tsp-research
│   ├── algorithms_reference.md                Referência de algoritmos QML
│   ├── keywords_guide.md                      Guia de keywords por domínio
│   └── writing_style.md                       Estilo de redação científica
│
└── artefatos/                                 Outputs de análise
    └── resultados_bibliografia/               Tabelas e gráficos exportados
```

---

## 7. Stack Técnica

- **Python 3.11+**
- **Streamlit 1.30+** — dashboard interativo
- **pandas 2.0+**, **numpy 1.24+** — manipulação de dados
- **Plotly 5.18+** — visualizações interativas
- **wordcloud + matplotlib** — nuvem de palavras
- **openpyxl 3.1+** — leitura/escrita de XLSX
- **Lens.org** — base bibliográfica de origem (registros acadêmicos + patentes)

---

## 8. Reprodutibilidade

Para reproduzir o pipeline completo do zero a partir dos CSVs brutos:

```bash
# 1. Deduplicação (35 CSVs brutos → artigos_unicos.csv)
python src/deduplicar_artigos.py

# 2. Análise bibliométrica (artigos_unicos.csv → resultados_bibliometria/)
python src/analise_bibliometrica.py

# 3. Triagem PRISMA-ScR (artigos_unicos.csv → artigos_unicos_triagem.csv)
python src/triagem_artigos.py

# 4. Classificação por tipo de problema (atualiza artigos_unicos_triagem.csv)
python src/classificar_problema.py

# 5. Geração da planilha de revisão (primeira vez apenas)
python src/gerar_tabela_revisao.py

# 6. Dashboard
streamlit run src/dashboard_bibliometrico.py
```

Todos os scripts são idempotentes e podem ser executados independentemente — cada um consome um CSV/XLSX de entrada e produz um CSV/XLSX de saída determinístico.

---

## 9. Resultados Parciais (Fase 1)

- **3.774 registros brutos** extraídos do Lens.org via 35 *search strings*.
- **2.471 artigos únicos** após deduplicação (DOI + título + cross-DOI).
- **1.303 duplicatas** removidas (~34,5% de sobreposição entre strings).
- **1.231 artigos** pós-remoção das strings #10–#14 (Iter. 2).
- **261 elegíveis** (21,2% do corpus refinado) após triagem PRISMA-ScR em 2 fases.
- **Precisão estimada ~90%+** do corpus elegível (verificada por inspeção manual).
- **53 artigos no núcleo CI-2** (backorder prediction + demand forecasting + inventory control) — 20,3% dos elegíveis.

Os detalhes quantitativos de cada etapa estão em `docs/resumo_triagem_artigos.md` e são visualizáveis interativamente no dashboard.

---

## 10. Próximos Passos

**Curto prazo (4 semanas)** — Revisão Bibliográfica
1. Full-text review dos 261 elegíveis, priorizando núcleo CI-2.
2. Preenchimento de `tabela_revisao_bibliografica.xlsx` conforme protocolo.
3. Validação do classificador automático (`tipo_problema_auto` × `problema_validado`).

**Médio prazo (2–3 meses)** — Síntese e Análise
4. Consolidação do corpus de síntese (`relevancia_final = alta`).
5. Análise comparativa QML × Clássico por tipo de problema.
6. Mapeamento de lacunas de pesquisa (cruzamento `tipo_problema × metodo_qml × resultado`).

**Longo prazo** — Experimentação e Redação
7. Prova-de-conceito em backorder prediction (baseline clássico + pipeline QML NISQ).
8. Redação do artigo de revisão sistemática PRISMA-ScR.
9. Publicação do dashboard como artefato reproduzível.

---

## 11. Autor e Orientação

**Autor:** Reynan Cardoso Souza
**Programa:** Mestrado Profissional em Gestão de Tecnologia e Inovação
**Instituição:** SENAI CIMATEC
**Ano:** 2025–2026
**Linha de pesquisa:** Computação Quântica aplicada à Indústria 4.0 — Quantum Machine Learning para Supply Chain Management

---

## 12. Licença e Citação

Projeto acadêmico. Para citar este trabalho (formato BibTeX provisório):

```bibtex
@misc{souza2026qml-supply-chain,
  author = {Souza, Reynan Cardoso},
  title  = {Quantum Machine Learning Aplicado a Supply Chain e Inventário:
            Revisão Bibliográfica Sistemática PRISMA-ScR},
  year   = {2026},
  note   = {Mestrado Profissional — SENAI CIMATEC},
  howpublished = {\url{https://github.com/reynancs/quantum_supply_chain_research}}
}
```
