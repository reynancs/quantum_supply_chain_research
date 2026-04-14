"""
Script de Classificacao por Tipo de Problema — Pos-Triagem

Classifica artigos que passaram pela Fase 2 da triagem (fase2_decisao == 'incluir')
por tipo de problema de supply chain/logistica abordado.

Taxonomia (aplicada em ordem de prioridade — mais especifico primeiro):
    1. backorder_prediction    — predicao de backorder (CI-2)
    2. demand_forecasting      — previsao de demanda (CI-2)
    3. inventory_control       — controle/otimizacao de inventario (CI-2)
    4. routing_transportation  — VRP, TSP, roteamento, transporte, last-mile
    5. scheduling_production   — scheduling, job shop, production planning
    6. supplier_procurement    — selecao de fornecedor, compras, sourcing
    7. risk_resilience         — risco, resiliencia, disruption em SC
    8. sustainability_sc       — supply chain sustentavel/verde/carbon
    9. supply_chain_general    — catch-all SC (gestao geral, sem foco especifico)
   10. outros                  — nao classificado (apenas QML sem ancora clara em SC)

Logica: matching por regex com word boundary no TITULO + ABSTRACT. A primeira
categoria (em ordem de prioridade) que casa e atribuida como `tipo_problema`.
Artigos excluidos na triagem recebem `tipo_problema = 'nao_avaliado'`.

Como usar:
    python src/classificar_problema.py

Entrada: data/artigos_unicos_triagem.csv
Saida:   data/artigos_unicos_triagem.csv (sobrescrito com nova coluna `tipo_problema`)
"""

import os
import re
import pandas as pd


# ============================================================
# CONFIGURACAO — Caminhos
# ============================================================

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO = os.path.join(PASTA_PROJETO, "data", "artigos_unicos_triagem.csv")


# ============================================================
# TAXONOMIA — Regras de classificacao em ordem de prioridade
# ============================================================
#
# Cada categoria e definida por uma lista de palavras-chave. A primeira
# categoria (em ordem da lista) que casar com titulo+abstract sera atribuida.
#
# Priorizacao: problemas mais especificos (backorder, demand, inventory) vem
# antes de categorias amplas (supply_chain_general). Isso garante que um
# artigo de "demand forecasting for supply chain" seja classificado como
# demand_forecasting (mais informativo), nao supply_chain_general.

TAXONOMIA = [
    (
        "backorder_prediction",
        [
            "backorder", "back order", "back-order",
            "stockout prediction", "stock-out prediction",
        ],
    ),
    (
        "demand_forecasting",
        [
            "demand forecast", "demand forecasting", "demand prediction",
            "sales forecast", "sales forecasting", "sales prediction",
            "forecasting demand", "predicting demand",
            "consumer demand", "customer demand",
            "load forecasting for supply",  # nicho
        ],
    ),
    (
        "inventory_control",
        [
            "inventory control", "inventory management",
            "inventory optimization", "inventory optimisation",
            "inventory policy", "inventory planning",
            "stock control", "stock management", "stock optimization",
            "replenishment policy", "replenishment",
            "safety stock", "reorder point",
            "(s,S) policy", "order quantity",
            "inventory level", "inventory routing",
        ],
    ),
    (
        "routing_transportation",
        [
            "vehicle routing", "vrp",
            "travelling salesman", "traveling salesman", "tsp",
            "last mile", "last-mile",
            "route optimization", "route optimisation", "routing problem",
            "freight routing", "freight transport", "freight transportation",
            "transportation planning", "transportation problem",
            "fleet management", "fleet optimization",
            "delivery route", "delivery planning",
            "shipment", "shipping",
        ],
    ),
    (
        "scheduling_production",
        [
            "job shop", "job-shop", "jobshop",
            "flow shop", "flow-shop", "flowshop",
            "production scheduling", "production planning",
            "manufacturing scheduling", "manufacturing planning",
            "machine scheduling", "resource scheduling",
            "lot sizing", "lot-sizing",
            "assembly line", "line balancing",
        ],
    ),
    (
        "supplier_procurement",
        [
            "supplier selection", "supplier evaluation",
            "supplier management", "vendor selection",
            "procurement", "sourcing strategy", "strategic sourcing",
            "purchasing decision",
        ],
    ),
    (
        "risk_resilience",
        [
            "supply chain risk", "supply chain resilience",
            "supply chain disruption", "sc disruption",
            "risk management in supply", "risk assessment in supply",
            "supply chain attack", "supply chain security",
            "counterfeit detection",
            "supply chain vulnerab",
        ],
    ),
    (
        "sustainability_sc",
        [
            "sustainable supply chain", "green supply chain",
            "carbon emission", "carbon footprint", "carbon-neutral",
            "circular economy", "circular supply",
            "closed-loop supply", "closed loop supply",
            "reverse logistics",
            "decarbonization", "decarbonisation",
        ],
    ),
    (
        "predictive_maintenance",
        [
            "predictive maintenance", "prognosis",
            "health management", "condition monitoring",
            "fault detection", "fault diagnosis",
            "remaining useful life", "rul prediction",
            "equipment reliability",
        ],
    ),
    (
        "supply_chain_general",
        [
            "supply chain", "supply-chain",
            "logistics", "logistic",
            "warehouse", "warehousing",
            "distribution network", "distribution center",
            "order fulfillment", "order fulfilment",
            "e-commerce logistics", "omnichannel",
        ],
    ),
    (
        "industry40_smart_mfg",
        [
            "industry 4.0", "industry 5.0",
            "smart manufacturing", "smart factory",
            "digital twin", "digital transformation",
            "cyber-physical system", "cyber physical system",
            "iiot", "industrial iot", "industrial internet of things",
        ],
    ),
    (
        "qml_method_review",
        [
            "review of quantum machine learning",
            "quantum machine learning: a review",
            "new trends in quantum",
            "survey of quantum", "survey on quantum",
            "benchmark quantum", "benchmarking quantum",
            "quantum reservoir computing",
            "variational quantum circuit",
            "quantum kernel method",
        ],
    ),
]

# Ordem final (para documentacao e iteracao)
ORDEM_CATEGORIAS = [cat for cat, _ in TAXONOMIA]
ORDEM_CATEGORIAS.append("outros")


# ============================================================
# UTILITARIOS — compilacao de regex e matching
# ============================================================

def _compilar(palavras):
    padroes = []
    for p in palavras:
        padroes.append(re.compile(r"\b" + re.escape(p) + r"\b", re.IGNORECASE))
    return padroes


TAXONOMIA_COMPILADA = [(cat, _compilar(kws)) for cat, kws in TAXONOMIA]


def _classificar(texto):
    """Retorna a primeira categoria cuja keyword casa com `texto`, ou 'outros'."""
    if not texto:
        return "outros"
    for categoria, padroes in TAXONOMIA_COMPILADA:
        for padrao in padroes:
            if padrao.search(texto):
                return categoria
    return "outros"


# ============================================================
# MAIN
# ============================================================

def main():
    if not os.path.exists(ARQUIVO):
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {ARQUIVO}\n"
            "Execute primeiro: python src/triagem_artigos.py"
        )

    df = pd.read_csv(ARQUIVO)
    print(f"Lidos {len(df)} artigos de {os.path.basename(ARQUIVO)}")

    if "fase2_decisao" not in df.columns:
        raise ValueError(
            "Coluna 'fase2_decisao' nao existe. Execute primeiro triagem_artigos.py"
        )

    # Inicializa com nao_avaliado
    df["tipo_problema"] = "nao_avaliado"

    # Classifica apenas os incluidos
    mask = df["fase2_decisao"] == "incluir"
    total = int(mask.sum())
    print(f"\nClassificando {total} artigos incluidos...\n")

    for idx in df.index[mask]:
        titulo = str(df.at[idx, "Title"]) if pd.notna(df.at[idx, "Title"]) else ""
        abstract = ""
        if "Abstract" in df.columns and pd.notna(df.at[idx, "Abstract"]):
            abstract = str(df.at[idx, "Abstract"])
        texto = titulo + " " + abstract
        df.at[idx, "tipo_problema"] = _classificar(texto)

    # Resumo
    incluidos = df[mask]
    print("=" * 60)
    print("  RESUMO — Classificacao por Tipo de Problema")
    print("=" * 60)
    print(f"  Total classificados: {total}\n")

    dist = incluidos["tipo_problema"].value_counts()
    for cat in ORDEM_CATEGORIAS:
        n = int(dist.get(cat, 0))
        if n > 0:
            pct = 100 * n / total
            print(f"  {cat:28s}: {n:3d} ({pct:5.1f}%)")

    # Salva
    df.to_csv(ARQUIVO, index=False)
    print(f"\nArquivo salvo: {ARQUIVO}")
    print(f"Nova coluna adicionada: tipo_problema")


if __name__ == "__main__":
    main()
