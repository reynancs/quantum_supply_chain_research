"""
Dashboard Bibliometrico — Fase 1 (Exploracao Bibliografica)

Dashboard interativo em Streamlit para explorar os 2.471 artigos
unicos identificados na pesquisa bibliografica sobre QML em Supply Chain / Inventario.

Como usar:
    streamlit run src/dashboard_bibliometrico.py

Dependencias:
    pip install streamlit pandas plotly numpy wordcloud matplotlib pycountry openpyxl

Estrutura do arquivo:
    1. Imports e configuracao da pagina
    2. Constantes (cores, strings de busca, mapeamentos)
    3. Carregamento de dados (CSV → DataFrame pandas)
    4. Filtros (sidebar com widgets interativos)
    5. KPIs (metricas resumo no topo)
    6. Abas do dashboard (6 abas organizadas por etapas da pesquisa bibliografica)
    7. Funcao main() que orquestra tudo
"""

import os
from datetime import datetime
# streamlit (st): framework web para dashboards em Python.
#   Cada vez que o usuario interage com um widget, o script inteiro re-executa.
#   Documentacao: https://docs.streamlit.io
import streamlit as st
# pandas (pd): manipulacao de dados tabulares (DataFrames = tabelas).
import pandas as pd
# plotly.express (px): graficos interativos de alto nivel (bar, scatter, pie, etc.)
#   Documentacao: https://plotly.com/python/plotly-express/
import plotly.express as px
# plotly.graph_objects (go): graficos de baixo nivel (Heatmap, Scatterpolar/radar, etc.)
#   Usado quando px nao oferece o tipo de grafico desejado.
import plotly.graph_objects as go
import numpy as np
# WordCloud: gera imagens de nuvem de palavras a partir de frequencias.
from wordcloud import WordCloud
# matplotlib: usado apenas para renderizar a WordCloud como imagem.
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Backend sem interface grafica (necessario para servidores)
# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================

# st.set_page_config() DEVE ser o primeiro comando Streamlit do script.
# Define o titulo da aba do navegador, icone, e layout.
# layout="wide" usa toda a largura da tela (padrao e "centered").
# Para alterar o titulo da pagina, modifique page_title abaixo.
st.set_page_config(
    page_title="Análise Bibliométrica - QML Supply Chain",  # Titulo da aba do navegador
    page_icon=":bar_chart:",       # Icone da aba (emoji ou URL de imagem)
    layout="wide",                  # "wide" = largura total | "centered" = coluna central
    initial_sidebar_state="expanded",  # Sidebar aberta ao carregar
)

# ============================================================
# PALETA DE CORES
# ============================================================
# Para alterar as cores do dashboard, modifique os valores hexadecimais (#RRGGBB) abaixo.
# Use sites como https://colorhunt.co ou https://coolors.co para escolher paletas.

# CORES: dicionario principal de cores usadas em todo o dashboard.
# Referenciado como CORES["primary"], CORES["danger"], etc.
CORES = {
    "primary": "#0077B6",     # Azul principal — usado na maioria dos graficos
    "secondary": "#00B4D8",   # Azul claro — graficos secundarios
    "accent": "#90E0EF",      # Azul muito claro — destaques sutis
    "highlight": "#CAF0F8",   # Azul pastel — fundos e escalas de cor
    "dark": "#03045E",        # Azul escuro — textos e contrastes fortes
    "success": "#70AD47",     # Verde — Open Access, itens positivos
    "warning": "#FFC000",     # Amarelo — alertas, criterios de selecao
    "danger": "#ED7D31",      # Laranja — prioridade Alta, destaques criticos
}

# PALETTE: lista de cores para graficos com muitas categorias (10 cores).
# Plotly usa estas cores ciclicamente quando ha mais categorias que cores.
PALETTE = ["#0077B6", "#00B4D8", "#48CAE4", "#90E0EF", "#023E8A",
           "#0096C7", "#ADE8F4", "#70AD47", "#FFC000", "#ED7D31"]

# PALETTE_PUB_TYPE: cor fixa para cada tipo de publicacao.
# Usado no grafico de barras empilhadas "Publicacoes ao Longo do Tempo".
# Para adicionar um novo tipo, adicione uma entrada "tipo": "#COR" aqui.
PALETTE_PUB_TYPE = {
    "journal article": "#0077B6",
    "preprint": "#03045E",
    "conference proceedings article": "#48CAE4",
    "book chapter": "#90E0EF",
    "book": "#ADE8F4",
    "dissertation": "#70AD47",
    "report": "#0096C7",
    "other": "#A5A5A5",
}

STRINGS_BUSCA = {
    # --- Alta (#1-#9) ---
    1:  '"Quantum Machine Learning" AND "Supply Chain"',
    2:  '"Quantum Machine Learning" AND "Demand Forecasting"',
    3:  '"Quantum Machine Learning" AND "Inventory"',
    4:  '"Quantum Machine Learning" AND "Logistics"',
    5:  '"Quantum Neural Network" AND "Supply Chain"',
    6:  '"Quantum Computing" AND "Demand Forecasting"',
    7:  '"Quantum Computing" AND "Demand Prediction"',
    8:  '"Hybrid Quantum" AND "Supply Chain" AND "Prediction"',
    9:  '"Quantum Computing" AND "Inventory Control"',
    # Strings 10-14 removidas: precisao de 1.7% para supply chain (98.3% falsos positivos)
    # --- Media (#15-#18) ---
    15: '"Quantum Reinforcement Learning" AND "Inventory"',
    16: '"Quantum Computing" AND "Backorder"',
    17: '"Quantum Computing" AND "Supply Chain Management"',
    18: '"Quantum Kernel" AND "Time Series"',
    # --- Baixa (#19-#25) ---
    19: '"Quantum Computing" AND "Predictive Maintenance" AND "Supply Chain"',
    20: '"Quantum-Inspired" AND "Demand Forecasting"',
    21: '"Quantum Reservoir Computing" AND "Time Series"',
    22: '"Quantum Support Vector Machine" AND "Forecasting"',
    23: '"Quantum Computing" AND "Supply Chain Resilience"',
    24: '"Quantum" AND "Inventory Optimization" AND "Machine Learning"',
    25: '"Quantum Machine Learning" AND "Classification" AND "Supply Chain"',
    # --- Buscas-referencia (#26-#28) ---
    26: '"QAmplifyNet" AND "Backorder Prediction"',
    27: '"Hybrid Quantum Neural Networks" AND "Backorder Prediction"',
    28: '"Hybrid Quantum Neural Networks" AND "Supply Chain"',
    # --- Rastreamento por area de aplicacao ML em Supply Chain (#29-#35) ---
    29: '"Quantum" AND "Demand Forecasting" AND "Supply Chain"',
    30: '"Quantum" AND "Inventory Optimization"',
    31: '"Quantum" AND "Route Optimization" AND "Supply Chain"',
    32: '"Quantum Machine Learning" AND "Vehicle Routing"',
    33: '"Quantum" AND "Load Balancing" AND "Logistics"',
    34: '"Quantum" AND "Supplier Risk"',
    35: '"Quantum Computing" AND "Supplier Risk Management"',
}

# PRIORIDADES: classifica cada string de busca (1-35) por relevancia ao tema central.
# Alta  = QML + previsao/inventario diretamente em supply chain
# Media = contexto ampliado (time series, forecasting geral, areas comparativas)
# Baixa = exploratórias, nichos, buscas-referencia especificas
PRIORIDADES = {
    # Prioridade Alta (#1-#9): tema central
    1: "Alta", 2: "Alta", 3: "Alta", 4: "Alta", 5: "Alta",
    6: "Alta", 7: "Alta", 8: "Alta", 9: "Alta",
    # Strings 10-14 removidas
    # Prioridade Media (#15-#18): contexto ampliado
    15: "Media", 16: "Media", 17: "Media", 18: "Media",
    # Prioridade Baixa (#19-#28): exploratórias e buscas-referencia
    19: "Baixa", 20: "Baixa", 21: "Baixa", 22: "Baixa", 23: "Baixa",
    24: "Baixa", 25: "Baixa", 26: "Baixa", 27: "Baixa", 28: "Baixa",
    # Rastreamento por area de aplicacao ML em Supply Chain (#29-#35)
    29: "Alta",  30: "Alta",  # Demand Forecasting (#29) + Inventory Optimization (#30)
    31: "Media", 32: "Media",               33: "Baixa",  # Route Optimization (#31-#32) + Load Balancing (#33)
    34: "Media", 35: "Media",                             # Supplier Risk (#34-#35)
}



COR_PRIORIDADE = {
    "Alta": CORES["danger"],
    "Media": CORES["primary"],
    "Baixa": "#A5A5A5",
}

# AREA_APLICACAO: classifica cada string em uma area tematica para uso no
# grafico de bolhas "Artigos Mais Citados ao Longo do Tempo" (aba Impacto).
# Para alterar a classificacao de uma string, mude o valor aqui.
# Para adicionar uma nova area, adicione tambem em COR_AREA abaixo.
#
# Areas de aplicacao ML em Supply Chain (projeto QML-Inventory):
#   Demand Forecasting     : #2, #6, #7, #20, #29
#   Inventory Optimization : #3, #9, #15, #16, #24, #30
#   Supply Chain/Logistica : #1, #4, #5, #8, #17, #19, #23, #25, #28
#   Metodos QML            : #18, #21, #22, #26, #27
#   Route Optimization     : #31, #32
#   Load Balancing         : #33
#   Supplier Risk          : #34, #35
#   Nota: strings 10-14 removidas (precisao 1.7% para supply chain)
AREA_APLICACAO = {
    # Demand Forecasting — previsao de demanda em supply chain
    2: "Demand Forecasting",  6: "Demand Forecasting",  7: "Demand Forecasting",
    20: "Demand Forecasting",
    29: "Demand Forecasting",
    # Inventory Optimization — controle e otimizacao de inventario/estoque
    3: "Inventory Optimization",  9: "Inventory Optimization", 15: "Inventory Optimization",
    16: "Inventory Optimization", 24: "Inventory Optimization",
    30: "Inventory Optimization",
    # Supply Chain / Logistica — gestao geral de cadeia de suprimentos
    1: "Supply Chain/Logística",  4: "Supply Chain/Logística",  5: "Supply Chain/Logística",
    8: "Supply Chain/Logística", 17: "Supply Chain/Logística", 19: "Supply Chain/Logística",
    23: "Supply Chain/Logística", 25: "Supply Chain/Logística", 28: "Supply Chain/Logística",
    # Metodos QML — arquiteturas e tecnicas de Quantum Machine Learning
    18: "Métodos QML", 21: "Métodos QML", 22: "Métodos QML",
    26: "Métodos QML", 27: "Métodos QML",
    # Route Optimization — otimizacao de rotas e roteamento de veiculos
    31: "Route Optimization", 32: "Route Optimization",
    # Load Balancing — balanceamento de carga em logistica
    33: "Load Balancing",
    # Supplier Risk — gestao de risco e selecao de fornecedores
    34: "Supplier Risk", 35: "Supplier Risk",
}

COR_AREA = {
    "Demand Forecasting":    "#E64646",  # vermelho  — area principal do projeto
    "Inventory Optimization": "#0077B6", # azul      — controle de inventario
    "Supply Chain/Logística": "#70AD47", # verde     — logistica geral
    "Métodos QML":            "#9B59B6", # roxo      — arquiteturas e metodos
    "Route Optimization":     "#ED7D31", # laranja   — roteamento
    "Load Balancing":         "#F4A460", # areia     — balanceamento de carga
    "Supplier Risk":          "#5D6D7E", # cinza     — risco de fornecedores
}


# ============================================================
# CARREGAMENTO DE DADOS
# ============================================================
# Fonte de dados principal: data/artigos_unicos.csv (2.471 artigos deduplicados)
# Fonte de dados secundaria: data/base_algoritmos_abordagens.csv (algoritmos QML catalogados)
#   → usada apenas na aba "Algoritmos e Abordagens" (desabilitada até o CSV estar disponível)
# Fonte auxiliar: docs/pesquisa_palavras_chave_inventory_qml.xlsx
#   → usada apenas na aba "Strings de Busca" para exibir strings completas

# Caminho raiz do projeto (um nivel acima de src/)
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# @st.cache_data: decorator do Streamlit que faz CACHE dos dados carregados.
# Como o Streamlit re-executa o script inteiro a cada interacao do usuario,
# sem cache o CSV seria relido do disco toda vez. Com cache, le apenas 1 vez.
# Para forcar recarregamento, clique no botao "Clear Cache" no menu do Streamlit
# ou reinicie o servidor.
@st.cache_data
def carregar_dados():
    """Carrega o CSV principal e prepara colunas derivadas.

    Retorna um DataFrame pandas com as colunas do CSV original mais:
    - strings_lista: lista de inteiros com os numeros das strings de busca de cada artigo
    - prioridade: "Alta", "Media" ou "Baixa" (baseada na primeira string)
    """
    caminho = os.path.join(PASTA_PROJETO, "data", "artigos_unicos.csv")
    # dtype=str: le todas as colunas como texto para evitar erros de tipo
    df = pd.read_csv(caminho, dtype=str)

    # Converter colunas de texto para numeros (pd.to_numeric com errors="coerce"
    # converte valores invalidos para NaN em vez de dar erro)
    df["Publication Year"] = pd.to_numeric(df["Publication Year"], errors="coerce")
    df["Citing Works Count"] = pd.to_numeric(df["Citing Works Count"], errors="coerce").fillna(0).astype(int)
    df["Citing Patents Count"] = pd.to_numeric(df["Citing Patents Count"], errors="coerce").fillna(0).astype(int)
    df["qtd_strings"] = pd.to_numeric(df["qtd_strings"], errors="coerce").fillna(1).astype(int)

    # Converter data de publicacao para formato datetime (permite eixo temporal nos graficos)
    df["Date Published"] = pd.to_datetime(df["Date Published"], errors="coerce")

    # Coluna "strings_origem" contem "1;3;7" (separado por ";").
    # Aqui convertemos para lista Python [1, 3, 7] para facilitar filtros.
    df["strings_lista"] = df["strings_origem"].fillna("").apply(
        lambda x: [int(float(s.strip())) for s in x.split(";") if s.strip() and s.strip() != "nan"]
    )

    # Atribui prioridade ao artigo baseada na primeira string de origem
    df["prioridade"] = df["strings_lista"].apply(
        lambda lst: PRIORIDADES.get(lst[0], "Baixa") if lst else "Baixa"
    )

    # Padronizar tipos de publicacao (minusculas, sem espacos extras)
    df["Publication Type"] = df["Publication Type"].fillna("other").str.lower().str.strip()

    return df


# ============================================================
# CARREGAMENTO — TRIAGEM PRISMA-ScR
# ============================================================
# Fonte: data/artigos_unicos_triagem.csv
# Gerado por: src/triagem_artigos.py + src/classificar_problema.py

# Mapa de cores para tipo_problema (alinhado com src/gerar_tabela_revisao.py)
CORES_TIPO_PROBLEMA = {
    # Verde (nucleo CI-2)
    "backorder_prediction":     "#70AD47",
    "demand_forecasting":       "#7FBF5C",
    "inventory_control":        "#8FCD6F",
    # Azul (SC especifico)
    "routing_transportation":   "#0077B6",
    "scheduling_production":    "#1E87C2",
    "supplier_procurement":     "#3497CE",
    "risk_resilience":          "#4AA7DA",
    "sustainability_sc":        "#61B7E6",
    "predictive_maintenance":   "#77C7F2",
    # Amarelo (catch-all SC)
    "supply_chain_general":     "#FFC000",
    # Cinza (baixa prioridade / generico)
    "industry40_smart_mfg":     "#B0B0B0",
    "qml_method_review":        "#989898",
    "outros":                   "#7F7F7F",
    "nao_avaliado":             "#D9D9D9",
}

# Ordem hierarquica para graficos de barras
ORDEM_TIPO_PROBLEMA = [
    "backorder_prediction", "demand_forecasting", "inventory_control",
    "routing_transportation", "scheduling_production", "supplier_procurement",
    "risk_resilience", "sustainability_sc", "predictive_maintenance",
    "supply_chain_general", "industry40_smart_mfg", "qml_method_review",
    "outros",
]

# Mapa de cores para motivos de exclusao
CORES_MOTIVO_EXCLUSAO = {
    "CE-1": "#ED7D31",          # laranja
    "CE-2": "#FFC000",          # amarelo
    "CE-3": "#0077B6",          # azul
    "CE-3 (forte)": "#03045E",  # azul escuro
    "CE-5": "#7F7F7F",          # cinza
}

# Evolucao das 5 iteracoes de triagem (docs/resumo_triagem_artigos.md §6.3)
EVOLUCAO_TRIAGEM = pd.DataFrame({
    "iteracao": ["Iter. 1\n(original)", "Iter. 2\n(sem strings 10-14)",
                 "Iter. 3\n(dedup cross-DOI)", "Iter. 4\n(CE-3 forte, 04-13)",
                 "Iter. 5\n(revisão manual, 04-14)"],
    "corpus": [2471, 1299, 1231, 1231, 1231],
    "elegiveis": [1154, 408, 312, 289, 261],
    "precisao_estimada": [27.0, 58.0, 80.0, 87.5, 90.0],
})


@st.cache_data
def carregar_dados_triagem():
    """Carrega data/artigos_unicos_triagem.csv (1.231 artigos com decisoes PRISMA-ScR)."""
    caminho = os.path.join(PASTA_PROJETO, "data", "artigos_unicos_triagem.csv")
    df = pd.read_csv(caminho, dtype=str)

    df["Publication Year"] = pd.to_numeric(df["Publication Year"], errors="coerce")
    df["Citing Works Count"] = pd.to_numeric(df["Citing Works Count"], errors="coerce").fillna(0).astype(int)

    # Normalizar motivo_exclusao (NaN vira string vazia — representa elegivel)
    df["motivo_exclusao"] = df["motivo_exclusao"].fillna("")
    df["tipo_problema"] = df["tipo_problema"].fillna("nao_avaliado")

    return df


# ============================================================
# CARREGAMENTO — REVISAO BIBLIOGRAFICA
# ============================================================
# Fonte: data/tabela_revisao_bibliografica.csv
# Gerado por: src/gerar_tabela_revisao.py

CORES_RELEVANCIA = {
    "alta":     "#70AD47",  # verde
    "media":    "#FFC000",  # amarelo
    "baixa":    "#ED7D31",  # laranja
    "excluir":  "#C0392B",  # vermelho
}

CORES_RESULTADO_QML = {
    "melhor":         "#70AD47",  # verde
    "equivalente":    "#FFC000",  # amarelo
    "pior":           "#ED7D31",  # laranja
    "nao_comparado":  "#A5A5A5",  # cinza
}

CORES_HARDWARE = {
    "simulator":    "#0077B6",
    "real_quantum": "#70AD47",
    "both":         "#9B59B6",
}


@st.cache_data
def carregar_dados_revisao(_mtime: float = 0.0):
    """Carrega data/tabela_revisao_bibliografica.xlsx (261 artigos elegiveis).

    A planilha Excel e a fonte de verdade — o pesquisador preenche os campos
    manuais (relevancia_final, metodo_qml, etc.) diretamente nela durante o
    full-text review. O CSV homonimo fica como backup/gerado inicial.

    O parametro _mtime (file modification time) integra o cache-key do
    @st.cache_data: sempre que a planilha e salva, o mtime muda e o cache e
    automaticamente invalidado, sem necessidade de limpar cache manualmente.

    Campos manuais podem estar vazios — o dashboard precisa lidar graciosamente
    com NaN/string vazia.
    """
    caminho_xlsx = os.path.join(PASTA_PROJETO, "data", "tabela_revisao_bibliografica.xlsx")
    caminho_csv = os.path.join(PASTA_PROJETO, "data", "tabela_revisao_bibliografica.csv")
    if os.path.exists(caminho_xlsx):
        df = pd.read_excel(caminho_xlsx, dtype=str)
    else:
        df = pd.read_csv(caminho_csv, dtype=str)

    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["citing_works"] = pd.to_numeric(df["citing_works"], errors="coerce").fillna(0).astype(int)

    # Colunas manuais — normalizar para string vazia (facilita contagens)
    colunas_manuais = [
        "revisado", "relevancia_final", "problema_validado",
        "metodo_qml", "metodo_qml_detalhe", "baseline_classico",
        "dataset_nome", "dataset_tamanho", "dataset_fonte",
        "metricas", "resultado_qml_vs_classico", "diferenca_percentual",
        "hardware", "hardware_detalhe", "n_qubits",
        "limitacoes", "tipo_contribuicao", "contribuicao_para_sc", "notas",
    ]
    for c in colunas_manuais:
        if c in df.columns:
            df[c] = df[c].fillna("").astype(str).str.strip()

    return df


# ============================================================
# FILTROS (SIDEBAR)
# ============================================================
# A sidebar e o painel lateral esquerdo do Streamlit.
# Todos os widgets aqui filtram o DataFrame globalmente,
# afetando TODAS as abas do dashboard (exceto "Algoritmos e Abordagens"
# que usa sua propria fonte de dados e filtros).
#
# Para ADICIONAR UM NOVO FILTRO:
#   1. Crie o widget na sidebar (st.sidebar.slider, multiselect, radio, etc.)
#   2. Adicione a logica de filtragem na secao "Aplicar filtros" (mask &= ...)
#   3. O filtro sera aplicado automaticamente em todas as abas

def criar_filtros(df):
    """Cria widgets de filtro na sidebar e retorna o DataFrame filtrado.

    Args:
        df: DataFrame completo com todos os artigos

    Returns:
        DataFrame filtrado conforme selecoes do usuario na sidebar
    """
    # st.sidebar.header(): exibe um titulo na barra lateral
    st.sidebar.header("Filtros")

    # --- Widget: Slider de periodo ---
    # st.sidebar.slider() cria uma barra deslizante. Com value=(min, max),
    # cria um slider de INTERVALO (duas alças). Retorna uma tupla (inicio, fim).
    anos_validos = df["Publication Year"].dropna()
    ano_min = int(anos_validos.min())
    ano_max = int(anos_validos.max())
    ano_range = st.sidebar.slider(
        "Periodo (Ano)",                          # Label exibido ao usuario
        min_value=ano_min, max_value=ano_max,     # Limites do slider
        value=(2018, ano_max),                    # Valor inicial (intervalo padrao)
    )

    # --- Widget: Multiselect de tipo de publicacao ---
    # st.sidebar.multiselect() cria um dropdown onde o usuario pode selecionar
    # multiplas opcoes. Retorna uma lista com os itens selecionados.
    # Se nada for selecionado, retorna lista vazia [] (interpretado como "todos").
    tipos = sorted(df["Publication Type"].unique())
    tipos_selecionados = st.sidebar.multiselect(
        "Tipo de Publicação",
        options=tipos,               # Lista de opcoes disponiveis
        default=None,                # Nenhum selecionado por padrao
        placeholder="Todos os tipos", # Texto quando nada selecionado
    )

    # --- Widget: Multiselect de string de busca ---
    strings_opcoes = [f"String-{num:02d}" for num in sorted(STRINGS_BUSCA.keys())]
    strings_selecionadas = st.sidebar.multiselect(
        "String de Busca",
        options=strings_opcoes,
        default=None,
        placeholder="Todas",
    )

    # --- Widget: Multiselect de prioridade ---
    prioridades_sel = st.sidebar.multiselect(
        "Prioridade da String",
        options=["Alta", "Media", "Baixa"],
        default=None,
        placeholder="Todas",
    )

    # --- Widget: Radio buttons para Open Access ---
    # st.sidebar.radio() cria botoes de opcao unica (apenas 1 selecionado).
    # horizontal=True coloca os botoes lado a lado em vez de empilhados.
    oa_opcao = st.sidebar.radio(
        "Open Access",
        options=["Todos", "Sim", "Não"],
        horizontal=True,
    )

    # --- Widget: Slider simples de citacoes minimas ---
    # Diferente do slider de periodo, este tem apenas UMA alça (valor unico).
    cit_max = min(int(df["Citing Works Count"].max()), 500)
    cit_min = st.sidebar.slider(
        "Minimo de Citações",
        min_value=0, max_value=cit_max, value=0,  # value=0 → sem filtro inicial
    )

    # -----------------------------------------------
    # APLICAR FILTROS
    # -----------------------------------------------
    # Tecnica: cria uma mascara booleana (True/False para cada linha).
    # Comeca com tudo True e vai aplicando AND (&=) com cada filtro.
    # No final, df[mask] retorna apenas as linhas que passaram em TODOS os filtros.
    mask = pd.Series(True, index=df.index)

    # Filtro de periodo: mantem artigos no intervalo OU sem ano definido
    mask &= df["Publication Year"].between(ano_range[0], ano_range[1]) | df["Publication Year"].isna()

    # Filtro de tipo: so aplica se o usuario selecionou algo
    if tipos_selecionados:
        mask &= df["Publication Type"].isin(tipos_selecionados)

    # Filtro de string: mantem artigos que pertencem a QUALQUER string selecionada
    if strings_selecionadas:
        nums_sel = [int(s.replace("String-", "")) for s in strings_selecionadas]
        mask &= df["strings_lista"].apply(
            lambda lst: any(n in lst for n in nums_sel)
        )

    # Filtro de prioridade
    if prioridades_sel:
        mask &= df["prioridade"].isin(prioridades_sel)

    # Filtro de Open Access
    if oa_opcao == "Sim":
        mask &= df["Is Open Access"].astype(str).str.lower() == "true"
    elif oa_opcao == "Não":
        mask &= df["Is Open Access"].astype(str).str.lower() == "false"

    # Filtro de citacoes minimas
    if cit_min > 0:
        mask &= df["Citing Works Count"] >= cit_min

    # .copy() cria uma copia independente para evitar SettingWithCopyWarning
    return df[mask].copy()


# ============================================================
# METRICAS KPI (cartoes com numeros no topo da pagina)
# ============================================================

def exibir_kpis(df, df_dedup=None):
    """Exibe cartoes de metricas KPI no topo da pagina.

    Fonte de dados:
      - data/artigos_unicos.csv (filtrado) → metricas do dataset filtrado
      - data/resumo_deduplicacao.csv → metricas do processo de deduplicacao
    """
    # ---- Linha 1: Metricas do dataset filtrado ----
    # st.columns(6) cria 6 colunas lado a lado na pagina.
    # Cada coluna pode receber widgets independentes.
    # Para alterar o numero de KPIs, mude o numero e ajuste as variaveis col.
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    total = len(df)
    anos = df["Publication Year"].dropna()
    citacoes = df["Citing Works Count"].sum()
    media_cit = df["Citing Works Count"].mean()
    oa_pct = (df["Is Open Access"].astype(str).str.lower() == "true").sum() / max(total, 1) * 100
    paises = df["Source Country"].dropna().nunique()

    # st.metric() exibe um cartao com label e valor numerico destacado.
    # Pode receber um terceiro parametro "delta" para mostrar variacao (ex: +10%).
    col1.metric("Total de Artigos", f"{total:,}")
    col2.metric("Periodo", f"{int(anos.min())}-{int(anos.max())}" if len(anos) > 0 else "N/A")
    col3.metric("Total de Citações", f"{citacoes:,}")
    col4.metric("Media Citações", f"{media_cit:.1f}")
    col5.metric("Open Access", f"{oa_pct:.1f}%")
    col6.metric("Paises", f"{paises}")

    # ---- Linha 2: Metricas de deduplicacao ----
    # Fonte: data/resumo_deduplicacao.csv — estatisticas do processo de limpeza dos dados
    if df_dedup is not None and not df_dedup.empty:
        st.divider()
        st.caption("📊 Estatísticas de Deduplicação")
        d1, d2, d3, d4, d5, d6 = st.columns(6)
        row = df_dedup.iloc[0]  # CSV tem apenas 1 linha de dados

        d1.metric("Total Bruto", f"{int(row['total_bruto']):,}")
        d2.metric("Total Único", f"{int(row['total_unico']):,}")
        d3.metric("Removidos", f"{int(row['total_removido']):,}")
        d4.metric("Removidos (DOI)", f"{int(row['removidos_por_doi']):,}")
        d5.metric("Removidos (Título)", f"{int(row['removidos_por_titulo']):,}")
        d6.metric("Sobreposição", f"{row['taxa_sobreposicao_pct']:.1f}%")


# ============================================================
# ABA 1 — VISAO GERAL (unificada: produção, composição, fontes e autores)
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado pela sidebar)
# Organizada em 4 blocos visuais:
#   Bloco 1 — Produção ao Longo do Tempo (temporal)
#   Bloco 2 — Composição do Corpus (tipos + open access)
#   Bloco 3 — Fontes e Autores (journals + autores)
#   Bloco 4 — Editoras (publishers)

def aba_visao_geral(df):
    """Panorama geral do corpus: produção temporal, composição, fontes e autores."""

    # ═════════════════════════════════════════════════════════
    # BLOCO 1 — PRODUCAO AO LONGO DO TEMPO
    # ═════════════════════════════════════════════════════════
    st.markdown("### 📈 Produção ao Longo do Tempo")
    st.caption(
        "Evolução anual do corpus por tipo de publicação. Indica crescimento do tema e "
        "distribuição entre canais (journals, preprints, conferências)."
    )

    df_tempo = df.dropna(subset=["Publication Year"]).copy()
    df_tempo["Ano"] = df_tempo["Publication Year"].astype(int)

    tipos_principais = ["journal article", "preprint", "conference proceedings article",
                        "book chapter", "book", "dissertation", "report"]
    df_tempo["Tipo"] = df_tempo["Publication Type"].apply(
        lambda x: x if x in tipos_principais else "other"
    )

    contagem = df_tempo.groupby(["Ano", "Tipo"]).size().reset_index(name="Contagem")

    fig = px.bar(
        contagem, x="Ano", y="Contagem", color="Tipo",
        color_discrete_map=PALETTE_PUB_TYPE,
        labels={"Contagem": "Número de Artigos", "Ano": "Ano de Publicação", "Tipo": "Tipo"},
    )
    fig.update_layout(
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=420,
        plot_bgcolor="white",
    )
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, width="stretch")

    st.divider()

    # ═════════════════════════════════════════════════════════
    # BLOCO 2 — COMPOSICAO DO CORPUS (tipos + open access)
    # ═════════════════════════════════════════════════════════
    st.markdown("### 🧩 Composição do Corpus")
    st.caption(
        "Distribuição dos artigos por tipo de publicação e status de acesso aberto."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Tipos de Publicação**")
        contagem_tipo = df["Publication Type"].value_counts().head(8)
        fig_tipo = px.pie(
            values=contagem_tipo.values,
            names=contagem_tipo.index,
            color=contagem_tipo.index,
            color_discrete_map=PALETTE_PUB_TYPE,
            hole=0.4,
        )
        fig_tipo.update_traces(textposition="inside", textinfo="percent+label")
        fig_tipo.update_layout(height=380, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_tipo, width="stretch")

    with col2:
        st.markdown("**Open Access**")
        oa = df["Is Open Access"].astype(str).str.lower()
        oa_counts = oa.value_counts()
        labels_oa = ["Open Access" if "true" in k else "Acesso Restrito" for k in oa_counts.index]
        cores_oa = [CORES["success"] if "true" in k else CORES["primary"] for k in oa_counts.index]

        fig_oa = px.pie(
            values=oa_counts.values,
            names=labels_oa,
            color_discrete_sequence=cores_oa,
            hole=0.4,
        )
        fig_oa.update_traces(textposition="inside", textinfo="percent+label")
        fig_oa.update_layout(height=380, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_oa, width="stretch")

    st.divider()

    # ═════════════════════════════════════════════════════════
    # BLOCO 3 — FONTES E AUTORES
    # ═════════════════════════════════════════════════════════
    st.markdown("### 📚 Fontes e Autores")
    st.caption(
        "Principais veículos de publicação (periódicos/conferências) e autores mais produtivos "
        "do corpus. Indicadores de concentração temática e atores-chave da área."
    )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Top 15 Journals / Fontes**")
        contagem_src = df["Source Title"].fillna("Não informado").value_counts().head(15)
        fig_src = px.bar(
            x=contagem_src.values, y=contagem_src.index,
            orientation="h",
            color_discrete_sequence=[CORES["secondary"]],
            labels={"x": "Número de Artigos", "y": ""},
        )
        fig_src.update_layout(
            height=500, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        fig_src.update_traces(text=contagem_src.values, textposition="outside")
        st.plotly_chart(fig_src, width="stretch")

    with col4:
        st.markdown("**Top 20 Autores Mais Ativos**")
        todos_autores = []
        for autores in df["Author/s"].dropna():
            for autor in str(autores).split(";"):
                autor = autor.strip()
                if autor:
                    todos_autores.append(autor)
        contagem_autores = pd.Series(todos_autores).value_counts().head(20)

        fig_autores = px.bar(
            x=contagem_autores.values, y=contagem_autores.index,
            orientation="h",
            color_discrete_sequence=[CORES["accent"]],
            labels={"x": "Número de Artigos", "y": ""},
        )
        fig_autores.update_layout(
            height=500, plot_bgcolor="white",
            yaxis=dict(autorange="reversed"),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        fig_autores.update_traces(text=contagem_autores.values, textposition="outside")
        st.plotly_chart(fig_autores, width="stretch")

    st.divider()

    # ═════════════════════════════════════════════════════════
    # BLOCO 4 — EDITORAS (publishers)
    # ═════════════════════════════════════════════════════════
    st.markdown("### 🏢 Editoras (Publishers)")
    st.caption("Top 10 editoras que concentram a produção do corpus.")

    contagem_pub = df["Publisher"].fillna("Não informado").value_counts().head(10)
    fig_pub = px.bar(
        x=contagem_pub.values, y=contagem_pub.index,
        orientation="h",
        color_discrete_sequence=[CORES["primary"]],
        labels={"x": "Número de Artigos", "y": ""},
    )
    fig_pub.update_layout(
        height=400, plot_bgcolor="white",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig_pub.update_traces(text=contagem_pub.values, textposition="outside")
    st.plotly_chart(fig_pub, width="stretch")


# ============================================================
# ABA 3 — IMPACTO E CITACOES
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado)
# Graficos: bubble chart (scatter com tamanho), histograma, tabela top 20

def _calcular_citacoes_por_ano(df):
    """Adiciona a coluna `citacoes_por_ano` ao DataFrame.

    Formula: Citing Works Count / max(ano_atual - Publication Year, 1)

    Rationale: artigos mais antigos acumulam citacoes naturalmente ao longo dos anos,
    mascarando trabalhos recentes potencialmente relevantes. Normalizar pelo tempo
    desde a publicacao expoe a 'velocidade de citacao' — artigos que atraem atencao
    rapidamente da comunidade mesmo sendo recentes.

    Retorna uma copia do df com a nova coluna.
    """
    ano_atual = datetime.now().year
    out = df.copy()
    anos_desde_pub = (ano_atual - out["Publication Year"]).clip(lower=1)
    out["citacoes_por_ano"] = (out["Citing Works Count"] / anos_desde_pub).round(2)
    return out


def aba_relevancia_ajustada(df):
    """Leaderboard horizontal dos artigos com maior relevancia ajustada pela idade.

    Cada barra = um artigo, ordenado por citacoes/ano (desc). Artigos recentes
    com alta velocidade de citacao aparecem naturalmente no topo ao lado dos
    classicos consolidados — o que seria impossivel em um ranking por citacoes
    totais (onde artigos antigos dominam mecanicamente).
    """
    st.subheader("Top 30 por Citações/Ano")
    st.caption(
        "Métrica: **citações ÷ anos desde a publicação**. Ranking dos 30 artigos com "
        "maior velocidade média de citação — permite enxergar trabalhos recentes de "
        "alto impacto emergente ao lado de clássicos já consolidados, corrigindo o viés "
        "temporal do ranking por citações totais. A cor identifica o Field of Study principal. "
        "A linha tracejada marca a média de citações/ano do corpus."
    )

    df_base = df.dropna(subset=["Publication Year"]).copy()
    df_base = df_base[df_base["Citing Works Count"] > 0]
    if df_base.empty:
        st.info("Sem artigos com citações nos filtros atuais.")
        return

    df_base = _calcular_citacoes_por_ano(df_base)
    media_corpus = float(df_base["citacoes_por_ano"].mean())
    df_top = df_base.nlargest(30, "citacoes_por_ano").copy()

    # Field of Study principal (Top-10 + Outros) com mesma paleta do segundo bubble chart
    def _primary_field(val):
        if pd.isna(val):
            return "Não informado"
        parts = [p.strip() for p in str(val).split(";") if p.strip()]
        return parts[0] if parts else "Não informado"

    df_top["Field of Study"] = df_top["Fields of Study"].apply(_primary_field)
    top_fields = df_top["Field of Study"].value_counts().head(10).index.tolist()
    df_top["Field of Study"] = df_top["Field of Study"].where(
        df_top["Field of Study"].isin(top_fields), "Outros"
    )

    paleta_fields = [
        "#E63946", "#1D3557", "#2A9D8F", "#F4A261", "#9B5DE5",
        "#06A77D", "#FFBE0B", "#FF006E", "#3A86FF", "#8D5524", "#A5A5A5",
    ]
    cor_map = {f: paleta_fields[i] for i, f in enumerate(top_fields)}
    cor_map["Outros"] = paleta_fields[-1]

    # Rotulo da barra: "Titulo (ano)" truncado para 70 caracteres
    df_top["rotulo"] = (
        df_top["Title"].str[:70]
        + " — "
        + df_top["Publication Year"].astype(int).astype(str)
    )
    # Garantir unicidade do rotulo (em caso de titulos identicos)
    df_top["rotulo"] = df_top["rotulo"] + " [" + df_top.index.astype(str) + "]"

    df_top["hover"] = (
        df_top["Title"].str[:100] + "<br>"
        + df_top["Author/s"].fillna("").str.split(";").str[0]
        + " (" + df_top["Publication Year"].astype(int).astype(str) + ")"
        + "<br>Citações totais: " + df_top["Citing Works Count"].astype(int).astype(str)
        + "<br>Citações/ano: " + df_top["citacoes_por_ano"].round(1).astype(str)
        + "<br>Field: " + df_top["Field of Study"]
    )

    # Ordenar DECRESCENTE para a lista ranqueada.
    df_top = df_top.sort_values("citacoes_por_ano", ascending=False).reset_index(drop=True)
    # Em barras horizontais do Plotly, para que o MAIOR valor apareça no TOPO do eixo Y,
    # precisamos forcar a ordem das categorias via `category_orders`. Sem isso, quando
    # `color=` e usado, Plotly cria traces por cor e reagrupa as barras, sobrescrevendo
    # qualquer ordenacao no DataFrame.
    ordem_y = df_top["rotulo"].tolist()[::-1]  # invertido: 1o item = base do eixo Y

    fig = px.bar(
        df_top,
        x="citacoes_por_ano",
        y="rotulo",
        color="Field of Study",
        color_discrete_map=cor_map,
        orientation="h",
        hover_name="hover",
        labels={"citacoes_por_ano": "Citações / Ano", "rotulo": ""},
        category_orders={
            "rotulo": ordem_y,
            "Field of Study": top_fields + ["Outros"],
        },
        text=df_top["citacoes_por_ano"].round(1).astype(str),
    )
    fig.update_traces(textposition="outside", cliponaxis=False)

    # Linha tracejada vertical na media do corpus (referencia visual)
    fig.add_vline(
        x=media_corpus,
        line_dash="dash",
        line_color="#444444",
        line_width=2,
        annotation_text=f"Média corpus: {media_corpus:.1f}",
        annotation_position="top",
        annotation_font_size=11,
        annotation_font_color="#444444",
    )

    # Legenda VERTICAL a DIREITA do grafico, fora da area de plotagem.
    # Tentativas anteriores (legenda acima ou abaixo) ficavam sobrepostas porque
    # o Plotly ancora em coordenadas 'paper' e a area de plot ocupa quase todo o
    # espaco quando ha 30 barras longas. Legenda lateral com margem direita ampla
    # (r=240) garante que ela NUNCA se sobreponha aos dados.
    fig.update_layout(
        height=820,
        plot_bgcolor="white",
        yaxis=dict(tickfont=dict(size=11), categoryorder="array", categoryarray=ordem_y),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.02,
            title_text="Field of Study",
            font=dict(size=11),
            bgcolor="rgba(255,255,255,0.9)",
        ),
        margin=dict(l=10, r=240, t=40, b=40),
    )
    st.plotly_chart(fig, width="stretch")


def aba_impacto(df):
    """Analise de citacoes: bubble chart por area, histograma e ranking."""

    # --- Bubble chart (grafico de bolhas) ---
    # Usa px.scatter() com parametro size= para criar bolhas proporcionais.
    # Cada bolha e um artigo; tamanho = numero de citacoes.
    # Cor = Area de Aplicacao (derivada da string de busca do artigo).
    st.subheader("Artigos Mais Citados ao Longo do Tempo")
    st.caption(
        "Top 200 artigos com mais citações, posicionados pela data de publicação. "
        "O tamanho da bolha é proporcional ao número de citações e a cor representa o "
        "Field of Study principal. Permite identificar marcos (outliers), ondas temáticas "
        "e a maturação da área ao longo do tempo."
    )

    df_bubble = df.dropna(subset=["Date Published"]).copy()
    df_bubble = df_bubble[df_bubble["Citing Works Count"] > 0]

    # .nlargest(200, ...): pega os 200 artigos mais citados.
    # Para mostrar mais ou menos bolhas, altere este numero.
    df_bubble_top = df_bubble.nlargest(200, "Citing Works Count")

    # Classificar por Field of Study principal (primeiro campo em "Fields of Study", ; separado).
    # Mantem apenas os Top-10 campos mais frequentes; o restante vira "Outros" para evitar
    # uma legenda poluida com dezenas de categorias.
    def _primary_field(val):
        if pd.isna(val):
            return "Não informado"
        parts = [p.strip() for p in str(val).split(";") if p.strip()]
        return parts[0] if parts else "Não informado"

    df_bubble_top["Field of Study"] = df_bubble_top["Fields of Study"].apply(_primary_field)
    top_fields = df_bubble_top["Field of Study"].value_counts().head(10).index.tolist()
    df_bubble_top["Field of Study"] = df_bubble_top["Field of Study"].where(
        df_bubble_top["Field of Study"].isin(top_fields), "Outros"
    )

    # Criar label de hover
    df_bubble_top["hover"] = (
        df_bubble_top["Title"].str[:80] + "<br>" +
        df_bubble_top["Author/s"].fillna("").str.split(";").str[0] +
        " (" + df_bubble_top["Publication Year"].astype(int).astype(str) + ")" +
        "<br>Citações: " + df_bubble_top["Citing Works Count"].astype(str) +
        "<br>Field: " + df_bubble_top["Field of Study"]
    )

    # px.scatter(): grafico de dispersao. Com size= vira grafico de bolhas.
    #   size: tamanho das bolhas proporcional ao numero de citacoes
    #   color: Field of Study principal (Top-10 + Outros)
    # Paleta qualitativa de alto contraste — cada Field recebe um matiz bem distinto
    # (Plotly "Bold" = 11 cores vivas bem separadas no espectro, ideais para categorias
    # nao ordenadas). Ultima posicao reservada para "Outros" em cinza neutro.
    paleta_fields = [
        "#E63946",  # vermelho
        "#1D3557",  # azul marinho
        "#2A9D8F",  # teal
        "#F4A261",  # laranja
        "#9B5DE5",  # roxo
        "#06A77D",  # verde
        "#FFBE0B",  # amarelo
        "#FF006E",  # rosa
        "#3A86FF",  # azul royal
        "#8D5524",  # marrom
        "#A5A5A5",  # cinza — reservado para "Outros"
    ]
    cor_map = {f: paleta_fields[i] for i, f in enumerate(top_fields)}
    cor_map["Outros"] = paleta_fields[-1]

    fig = px.scatter(
        df_bubble_top,
        x="Date Published",
        y="Citing Works Count",
        size="Citing Works Count",
        color="Field of Study",
        color_discrete_map=cor_map,
        hover_name="hover",
        size_max=40,
        labels={"Date Published": "Data de Publicação", "Citing Works Count": "Citações"},
        category_orders={"Field of Study": top_fields + ["Outros"]},
    )
    fig.update_layout(
        height=500, plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, width="stretch")


def aba_top_citados(df):
    """Tabela ranqueada dos 100 artigos mais citados, com campo de pesquisa e keywords.

    Separada de `aba_impacto` para permitir reordenacao na aba unificada
    'Impacto e Temas de Pesquisa' (tabela vem APOS treemap + wordcloud).
    """
    st.subheader("Top 100 Artigos Mais Citados")
    st.caption(
        "Ranking dos 100 artigos com maior contagem de citações do corpus filtrado. "
        "Inclui Campo de Pesquisa (Fields of Study) e Keywords para contextualizar o "
        "alinhamento temático dos trabalhos mais influentes — útil para identificar "
        "referências obrigatórias da área."
    )

    # Calcular citacoes/ano no corpus filtrado antes de ranquear
    df_calc = _calcular_citacoes_por_ano(df)

    colunas_fonte = ["Title", "Author/s", "Publication Year", "DOI",
                     "Citing Works Count", "citacoes_por_ano",
                     "Fields of Study", "Keywords"]
    df_top = df_calc.nlargest(100, "Citing Works Count")[colunas_fonte].copy()
    df_top.columns = ["Titulo", "Autores", "Ano", "DOI", "Citações",
                      "Citações/Ano", "Campo de Pesquisa", "Keywords"]

    df_top["Autores"] = df_top["Autores"].fillna("").str.split(";").str[0]
    df_top["Titulo"] = df_top["Titulo"].str[:80]
    df_top["Ano"] = df_top["Ano"].fillna(0).astype(int)
    df_top["Citações/Ano"] = df_top["Citações/Ano"].round(1)
    # Percentual de citacoes em relacao ao total do dataset filtrado
    df_top["Citações(%)"] = (df_top["Citações"] / df["Citing Works Count"].sum() * 100).round(1).astype(str) + "%"

    # Fields of Study e Keywords sao multi-valor separados por ";".
    # Substitui separador por virgula + espaco para leitura mais natural na tabela.
    for col in ("Campo de Pesquisa", "Keywords"):
        df_top[col] = df_top[col].fillna("—").astype(str).str.replace(";", ", ", regex=False)

    # Reordenar colunas: identificacao | metricas | contexto tematico
    df_top = df_top[["Titulo", "Autores", "Ano", "Citações", "Citações/Ano", "Citações(%)",
                     "Campo de Pesquisa", "Keywords", "DOI"]]

    st.dataframe(
        df_top.reset_index(drop=True),
        height=740,
        width="stretch",
        use_container_width=True,
        column_config={
            "Titulo": st.column_config.TextColumn(width="medium"),
            "Citações/Ano": st.column_config.NumberColumn(
                width="small",
                help="Citações ÷ anos desde a publicação — relevância ajustada pela idade do artigo",
                format="%.1f",
            ),
            "Campo de Pesquisa": st.column_config.TextColumn(width="medium"),
            "Keywords": st.column_config.TextColumn(width="large"),
        },
    )


# ============================================================
# ABA 4 — CAMPOS DE ESTUDO
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado)
# Colunas usadas: "Fields of Study" (multi-valor, separado por ";") e "Keywords"
# Graficos: treemap (Plotly) + nuvem de palavras (matplotlib/WordCloud)

def aba_treemap_fields(df):
    """Treemap dos 30 campos de estudo mais frequentes."""
    st.subheader("Top 30 - Fields of Study")
    st.caption(
        "Treemap dos 30 campos de estudo mais frequentes no corpus (Fields of Study "
        "é multi-valor — cada artigo pode contribuir para vários campos). "
        "O tamanho e a intensidade de cor refletem a frequência, destacando os domínios "
        "dominantes e revelando a natureza interdisciplinar da literatura."
    )
    todos_campos = []
    for campos in df["Fields of Study"].dropna():
        for campo in str(campos).split(";"):
            campo = campo.strip()
            if campo:
                todos_campos.append(campo)

    contagem = pd.Series(todos_campos).value_counts().head(30).reset_index()
    contagem.columns = ["Campo", "Frequencia"]

    fig = px.treemap(
        contagem,
        path=["Campo"],
        values="Frequencia",
        color="Frequencia",
        color_continuous_scale=["#CAF0F8", "#0077B6", "#03045E"],
    )
    fig.update_layout(height=600, plot_bgcolor="white")
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig, width="stretch")


def aba_wordcloud_keywords(df):
    """Nuvem de palavras das keywords mais frequentes."""
    st.subheader("Nuvem de Palavras — Keywords")
    keywords_preenchidos = df["Keywords"].dropna()
    cobertura = len(keywords_preenchidos) / len(df) * 100
    st.caption(f"Cobertura: {cobertura:.1f}% dos artigos possuem keywords")

    todas_kw = []
    for kws in keywords_preenchidos:
        for kw in str(kws).split(";"):
            kw = kw.strip()
            if kw:
                todas_kw.append(kw)

    if todas_kw:
        freq_kw = dict(pd.Series(todas_kw).value_counts().head(100))
        wc = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis",
            max_words=80,
            prefer_horizontal=0.7,
            min_font_size=10,
            max_font_size=80,
            relative_scaling=0.5,
        ).generate_from_frequencies(freq_kw)

        fig_wc, ax_wc = plt.subplots(figsize=(10, 6))
        ax_wc.imshow(wc, interpolation="bilinear")
        ax_wc.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(fig_wc)
        plt.close(fig_wc)
    else:
        st.info("Nenhum keyword disponivel com os filtros atuais.")


# ============================================================
# ABA — ESTRATÉGIA DE BUSCA (STRINGS)
# ============================================================
# Fonte de dados: data/artigos_unicos.csv (filtrado) + docs/pesquisa_palavras_chave_inventory_qml.xlsx
# A planilha Excel e usada apenas para exibir as strings completas na tabela de referencia.
# Graficos: barras por string, barras de sobreposicao, heatmap de coocorrencia

def aba_strings(df):
    """Analise das strings de busca: volume, sobreposicao e coocorrencia."""

    # --- Volume por String ---
    st.subheader("Volume de Artigos por String de Busca")
    st.caption(
        "Número de artigos únicos recuperados por cada uma das 35 strings booleanas "
        "aplicadas no Lens.org, coloridas por prioridade (Alta/Média/Baixa). "
        "Permite avaliar a produtividade de cada combinação de termos e identificar "
        "strings dominantes versus strings de nicho."
    )

    contagem = {}
    for _, row in df.iterrows():
        for s in row["strings_lista"]:
            contagem[s] = contagem.get(s, 0) + 1

    dados_string = []
    for num in sorted(contagem.keys()):
        dados_string.append({
            "String": f"#{num}",
            "Descrição": STRINGS_BUSCA.get(num, ""),
            "Artigos": contagem[num],
            "Prioridade": PRIORIDADES.get(num, "Baixa"),
        })
    df_strings = pd.DataFrame(dados_string)

    fig = px.bar(
        df_strings, x="String", y="Artigos",
        color="Prioridade",
        color_discrete_map=COR_PRIORIDADE,
        hover_data=["Descrição"],
        labels={"Artigos": "Artigos Únicos"},
    )
    fig.update_layout(
        height=450, plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig.update_traces(texttemplate="%{y}", textposition="outside")
    st.plotly_chart(fig, width="stretch")

    # --- Sobreposicao + Heatmap ---
    #col1, col2 = st.columns(2)

    #with col1:
    st.subheader("Sobreposição entre Strings")
    st.caption(
        "Distribuição de quantos artigos aparecem em 1, 2, 3+ strings de busca simultaneamente. "
        "Quanto maior a barra de valores baixos (=1), mais específicas e complementares são as "
        "strings; barras à direita indicam alta redundância entre combinações de termos."
    )
    contagem_overlap = df["qtd_strings"].value_counts().sort_index()
    fig_overlap = px.bar(
        x=contagem_overlap.index.astype(str),
        y=contagem_overlap.values,
        color_discrete_sequence=[CORES["primary"]],
        labels={"x": "Aparece em N strings", "y": "Qtd Artigos"},
    )
    fig_overlap.update_layout(height=600, plot_bgcolor="white")
    fig_overlap.update_traces(
        text=[f"{v} ({v/len(df)*100:.1f}%)" for v in contagem_overlap.values],
        textposition="outside",
    )
    st.plotly_chart(fig_overlap, width="stretch")

    #with col2:
    # Heatmap de coocorrencia: mostra quantos artigos aparecem em AMBAS as strings.
    # go.Heatmap(): grafico de calor (matrix). Usado quando px nao tem o tipo.
    #   z: matriz 2D de valores | x, y: labels dos eixos
    #   colorscale: gradiente de cores [[posicao, cor], ...]
    #   text/texttemplate: exibe valores dentro das celulas
    st.subheader("Coocorrência entre Strings")
    st.caption("Quantos artigos compartilham cada par de strings")

    # Construir matriz de coocorrencia
    strings_presentes = sorted(set(s for lst in df["strings_lista"] for s in lst))
    n = len(strings_presentes)
    idx_map = {s: i for i, s in enumerate(strings_presentes)}
    matriz = np.zeros((n, n), dtype=int)

    for lst in df["strings_lista"]:
        if len(lst) > 1:
            for i in range(len(lst)):
                for j in range(i + 1, len(lst)):
                    si, sj = lst[i], lst[j]
                    if si in idx_map and sj in idx_map:
                        matriz[idx_map[si]][idx_map[sj]] += 1
                        matriz[idx_map[sj]][idx_map[si]] += 1

    labels_str = [f"#{s}" for s in strings_presentes]

    fig_heat = go.Figure(data=go.Heatmap(
        z=matriz,
        x=labels_str,
        y=labels_str,
        colorscale=[[0, "#FFFFFF"], [0.2, "#CAF0F8"], [0.5, "#48CAE4"], [1, "#03045E"]],
        text=matriz,
        texttemplate="%{text}",
        textfont={"size": 8},
    ))
    fig_heat.update_layout(
        height=600,
        xaxis=dict(tickangle=45),
    )
    st.plotly_chart(fig_heat, width="stretch")

    # --- Tabela de Referência das Strings de Busca ---
    st.divider()
    st.subheader("Referência — Strings de Busca Utilizadas")
    st.caption("Fonte: Levantamento bibliográfico no Lens.org (filtro: Scholarly Works)")

    dados_ref = []
    for num in sorted(STRINGS_BUSCA.keys()):
        dados_ref.append({
            "Código": f"String-{num:02d}",
            "Descrição Resumida": STRINGS_BUSCA[num],
            "Prioridade": PRIORIDADES.get(num, "Baixa"),
        })
    df_ref = pd.DataFrame(dados_ref)

    # Carregar strings completas da planilha
    try:
        caminho_xlsx = os.path.join(PASTA_PROJETO, "docs", "pesquisa_palavras_chave_inventory_qml.xlsx")
        df_xlsx = pd.read_excel(caminho_xlsx, sheet_name="Palavras-Chave vs Artigos", header=None)
        strings_completas = {}
        totais = {}
        for _, row in df_xlsx.iterrows():
            try:
                num = int(row.iloc[0])
                if num >= 1:
                    strings_completas[num] = str(row.iloc[1]).strip()
                    totais[num] = int(row.iloc[5]) if pd.notna(row.iloc[5]) else 0
            except (ValueError, TypeError):
                continue

        df_ref["String de Busca Completa"] = df_ref["Código"].apply(
            lambda x: strings_completas.get(
                int(x.replace("String-", "")),
                STRINGS_BUSCA.get(int(x.replace("String-", "")), ""),  # fallback para STRINGS_BUSCA
            )
        )
        df_ref["Total Bruto"] = df_ref["Código"].apply(
            lambda x: totais.get(int(x.replace("String-", "")), 0)
        )
    except Exception:
        df_ref["String de Busca Completa"] = df_ref["Descrição Resumida"]
        df_ref["Total Bruto"] = 0

    st.dataframe(
        df_ref[["Código", "String de Busca Completa", "Prioridade", "Total Bruto"]].reset_index(drop=True),
        height=600,
        width="stretch",
        column_config={
            "Código": st.column_config.TextColumn(width="small"),
            "String de Busca Completa": st.column_config.TextColumn(width="large"),
            "Prioridade": st.column_config.TextColumn(width="small"),
            "Total Bruto": st.column_config.NumberColumn(width="small")
        },
    )



# ============================================================
# ABA 8 — TRIAGEM PRISMA-ScR
# ============================================================
# Fonte de dados: data/artigos_unicos_triagem.csv
# Protocolo: docs/protocolo_triagem.md | Resumo: docs/resumo_triagem_artigos.md

def exibir_kpis_triagem(df_t):
    """KPIs contextuais para a aba Triagem PRISMA-ScR."""
    total = len(df_t)
    excl_f1 = int((df_t["fase1_decisao"] == "excluir").sum())
    incl_f1 = int((df_t["fase1_decisao"] == "incluir").sum())
    excl_f2 = int((df_t["fase2_decisao"] == "excluir").sum())
    elegiveis = int((df_t["fase2_decisao"] == "incluir").sum())
    taxa_elegibilidade = 100 * elegiveis / max(total, 1)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Corpus Único", f"{total:,}")
    col2.metric("Fase 1 — Incluídos", f"{incl_f1:,}", delta=f"-{excl_f1}", delta_color="inverse")
    col3.metric("Fase 2 — Excluídos", f"{excl_f2:,}")
    col4.metric("Elegíveis (CI-2)", f"{elegiveis:,}")
    col5.metric("Taxa Elegibilidade", f"{taxa_elegibilidade:.1f}%")
    col6.metric(
        "Precisão Estimada",
        "~90%+",
        help=(
            "Proporção dos elegíveis que são verdadeiros positivos (de fato dentro do escopo "
            "QML × supply chain/inventário). Estimada por inspeção manual dos elegíveis ao "
            "final da Iter. 5 (2026-04-14): ~26 falsos positivos em 261 → ~90% de precisão."
        ),
    )


def aba_triagem_prisma(df_t):
    """Aba: Triagem PRISMA-ScR — diagrama de fluxo e estatísticas da triagem."""
    st.subheader("Fluxo de Triagem PRISMA-ScR")
    st.caption(
        "Processo automatizado de classificação dos 1.231 artigos únicos em duas fases: "
        "metadados (título + tipo + fields of study) e abstract. "
    )

    with st.expander("ℹ️ Como a **Precisão Estimada (~90%+)** foi calculada"):
        st.markdown(
            """
**O que mede.** Precisão estimada é a proporção dos artigos **elegíveis** (que passaram em todos os critérios automáticos) que de fato correspondem ao escopo da pesquisa — QML aplicado a supply chain, logística, inventário ou previsão de demanda. Em termos formais:

> **Precisão = Verdadeiros Positivos ÷ (Verdadeiros Positivos + Falsos Positivos)**

Não é precisão de classificador treinado — é uma métrica de **qualidade do corpus triado**, estimada por inspeção humana.

**Como foi calculada.** Ao final de cada iteração de refinamento, uma **revisão manual** foi feita sobre o conjunto de elegíveis daquela rodada, contando quantos artigos eram de fato do escopo vs. quantos eram falsos positivos (domínios fora de escopo que escaparam das regras automáticas). A razão verdadeiros/total alimenta a coluna "Precisão Estimada" da tabela de iterações:

| Iter. | Elegíveis | FP identificados | Precisão |
|---|---:|---:|---:|
| 1 (original) | 1.154 | ~840 | ~27% |
| 2 (sem strings 10–14) | 408 | ~170 | ~58% |
| 3 (dedup cross-DOI) | 312 | ~60 | ~80% |
| 4 (CE-3 forte, 04-13) | 289 | ~35 | ~88% |
| **5 (revisão manual, 04-14)** | **261** | **~26** | **~90%+** |

**Por que "~90%+" e não um número exato.** A estimativa da Iter. 5 veio da segunda revisão manual (2026-04-14), que identificou 24 falsos positivos adicionais em 14 domínios e realimentou as listas de keywords. Como alguns falsos positivos residuais podem existir em domínios ainda não cobertos pelas regras, o valor é reportado como **"~90%+"** — limite inferior conservador. A validação final ocorrerá na **Revisão Bibliográfica (full-text review)**, onde cada um dos 261 será lido integralmente; a taxa real de verdadeiros positivos será então conhecida e registrada em `relevancia_final` (`alta` / `média` / `baixa` / `excluir`).

**Fonte dos números.** `docs/resumo_triagem_artigos.md` §6.3 (Evolução da Triagem) e `data/resumo_triagem.csv`. Código: `src/triagem_artigos.py`.
"""
        )

    # --- Grafico 1: Funil / Sankey do fluxo PRISMA-ScR ---
    total = len(df_t)
    excl_f1 = int((df_t["fase1_decisao"] == "excluir").sum())
    incl_f1 = int((df_t["fase1_decisao"] == "incluir").sum())
    excl_f2 = int((df_t["fase2_decisao"] == "excluir").sum())
    elegiveis = int((df_t["fase2_decisao"] == "incluir").sum())

    col_f, col_b = st.columns([1, 1])

    with col_f:
        st.markdown("**Funil PRISMA-ScR**")
        fig_funil = go.Figure(go.Funnel(
            y=["Corpus único", "Incluídos Fase 1", "Elegíveis Fase 2"],
            x=[total, incl_f1, elegiveis],
            textinfo="value+percent initial",
            marker=dict(color=[CORES["primary"], CORES["secondary"], CORES["success"]]),
        ))
        fig_funil.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_funil, width="stretch")

    with col_b:
        st.markdown("**Exclusões por Critério**")
        motivos = df_t[df_t["motivo_exclusao"] != ""]["motivo_exclusao"].value_counts().reset_index()
        motivos.columns = ["Critério", "Quantidade"]
        fig_motivos = px.bar(
            motivos, x="Quantidade", y="Critério", orientation="h",
            color="Critério", color_discrete_map=CORES_MOTIVO_EXCLUSAO,
            text="Quantidade",
        )
        fig_motivos.update_traces(textposition="outside")
        fig_motivos.update_layout(
            height=380, showlegend=False, plot_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
            yaxis=dict(categoryorder="total ascending"),
        )
        st.plotly_chart(fig_motivos, width="stretch")

    st.caption(
        f"CE-1: otimização pura · CE-2: apenas trabalho futuro · CE-3: domínio fora de escopo · "
        f"CE-3 (forte): domínio claro no título (sem safety net) · CE-5: tipo de publicação não-substantivo"
    )

    with st.expander("ℹ️ Diferença entre CE-3 e CE-3 (forte)"):
        st.markdown(
            """
**CE-3 — Domínio fora de escopo (*com safety net*)**
Aplicado sobre **título + Fields of Study** (Fase 1) ou **abstract** (Fase 2). O artigo é excluído quando há
correspondência com palavras de domínios fora do escopo (ex.: *medical imaging*, *drug discovery*, *image classification*, *finance*)
**E** não há menção simultânea a termos de supply chain / logística / inventário (`palavras_dominio_manter`).
Essa *safety net* protege trabalhos legitimamente cross-domain — por exemplo, um artigo que aplique uma técnica
originalmente de `image classification` a `demand forecasting` é mantido por citar o domínio-alvo.

**CE-3 (forte) — Domínio claro no título (*sem safety net*)**
Aplicado exclusivamente ao **título** na Fase 1. Lista de palavras *hard exclude* (ex.: *blockchain*, *patent review*,
*nanotechnology*, *women in quantum*, *road traffic*, *drug-target interaction*) em que a presença no título é
considerada evidência **inequívoca** de outra área de pesquisa. A regra **não** é revogada por menção a supply chain —
mesmo que o abstract cite *supply chain*, o artigo é excluído se o título deixa claro que o objeto de estudo é outro domínio.
Motivo: evita falsos positivos de surveys/reviews multi-domínio que apenas citam supply chain como exemplo.

**Resumo da diferença**

| Aspecto | CE-3 | CE-3 (forte) |
|---|---|---|
| Onde procura | Título + Fields of Study / Abstract | Apenas no título |
| Revogável por `dominio_manter`? | **Sim** (safety net ativa) | **Não** (hard exclude) |
| Fase | Fase 1 e Fase 2 | Apenas Fase 1 |
| Lista de keywords | `palavras_dominio_excluir` | `palavras_dominio_excluir_forte` |
"""
        )

    st.divider()

    # --- Grafico 2: Evolucao das iteracoes ---
    st.subheader("Evolução do Refinamento (5 Iterações)")
    st.caption(
        "Cada iteração refinou os critérios de exclusão via revisão manual → expansão de keywords. "
        "A queda de elegíveis acompanha o aumento da precisão estimada."
    )

    fig_ev = go.Figure()
    fig_ev.add_trace(go.Bar(
        x=EVOLUCAO_TRIAGEM["iteracao"], y=EVOLUCAO_TRIAGEM["elegiveis"],
        name="Elegíveis", marker_color=CORES["primary"], yaxis="y",
        text=EVOLUCAO_TRIAGEM["elegiveis"], textposition="outside",
    ))
    fig_ev.add_trace(go.Scatter(
        x=EVOLUCAO_TRIAGEM["iteracao"], y=EVOLUCAO_TRIAGEM["precisao_estimada"],
        name="Precisão Estimada (%)", mode="lines+markers+text",
        marker=dict(size=10, color=CORES["danger"]), line=dict(width=3, color=CORES["danger"]),
        text=[f"{p:.0f}%" for p in EVOLUCAO_TRIAGEM["precisao_estimada"]],
        textposition="top center", yaxis="y2",
    ))
    fig_ev.update_layout(
        height=420, plot_bgcolor="white",
        yaxis=dict(title="Artigos Elegíveis", side="left"),
        yaxis2=dict(title="Precisão Estimada (%)", side="right", overlaying="y", range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_ev, width="stretch")

    with st.expander("ℹ️ O que aconteceu em cada iteração"):
        st.markdown(
            """
- **Iter. 1 — Original (2.471 → 1.154 elegíveis, ~27% precisão).**
  Primeira rodada da triagem automática sobre o corpus único completo, com conjunto inicial de keywords para CE-1/CE-2/CE-3/CE-5. Alta taxa de falsos positivos — muitos artigos de domínios fora de escopo passavam por não conterem keywords específicas de exclusão.

- **Iter. 2 — Remoção das strings 10–14 (1.299 → 408 elegíveis, ~58% precisão).**
  Identificou-se que as strings de busca 10 a 14 eram excessivamente genéricas (termos amplos de *machine learning* + *optimization*) e estavam injetando ruído no corpus. Foram excluídas da consolidação, reduzindo o corpus bruto de 2.471 → 1.299 antes de reexecutar a triagem.

- **Iter. 3 — Deduplicação cross-DOI (1.231 → 312 elegíveis, ~80% precisão).**
  Adição da etapa 5 do pipeline de deduplicação (título normalizado entre artigos com DOIs diferentes), removendo 68 pares preprint↔journal que estavam inflando elegíveis duplicados. Triagem reexecutada sobre o corpus definitivo de 1.231 artigos únicos.

- **Iter. 4 — CE-3 forte (1.231 → 289 elegíveis, ~88% precisão), 2026-04-13.**
  Introdução da lista `palavras_dominio_excluir_forte` — *hard excludes* no título (blockchain, patent review, nanotechnology, drug-target, road traffic, women in quantum, etc.) sem safety net de `palavras_dominio_manter`. Eliminou surveys e reviews multi-domínio que apenas tangenciavam supply chain.

- **Iter. 5 — Revisão manual (1.231 → 261 elegíveis, ~90% precisão), 2026-04-14.**
  Passada manual sobre os 289 elegíveis da Iter. 4 para capturar falsos positivos residuais (artigos cujo título/abstract escapavam das regras automáticas). Keywords encontradas na revisão foram realimentadas nas listas de exclusão, fechando o ciclo e estabelecendo o corpus final de **261 artigos elegíveis** para a revisão bibliográfica.
"""
        )

    st.divider()

    # --- Grafico 3: Distribuicao por tipo_problema dos elegiveis ---
    st.subheader("Distribuição dos 261 Elegíveis por Tipo de Problema")
    st.caption(
        "Classificação automática via `src/classificar_problema.py` (regex com word boundary em Title+Abstract). "
        "Verde = núcleo CI-2 (alvo primário) · Azul = SC específico · Amarelo = catch-all · Cinza = genérico."
    )

    elegiveis_df = df_t[df_t["fase2_decisao"] == "incluir"]
    dist = elegiveis_df["tipo_problema"].value_counts().reset_index()
    dist.columns = ["tipo_problema", "Quantidade"]
    dist["tipo_problema"] = pd.Categorical(dist["tipo_problema"], categories=ORDEM_TIPO_PROBLEMA, ordered=True)
    dist = dist.sort_values("tipo_problema")

    fig_tipo = px.bar(
        dist, x="tipo_problema", y="Quantidade",
        color="tipo_problema", color_discrete_map=CORES_TIPO_PROBLEMA,
        text="Quantidade",
    )
    fig_tipo.update_traces(textposition="outside")
    fig_tipo.update_layout(
        height=450, showlegend=False, plot_bgcolor="white",
        xaxis=dict(title="Tipo de Problema", tickangle=-30),
        yaxis=dict(title="Número de Artigos"),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_tipo, width="stretch")

    # Destaque núcleo CI-2
    nucleo_ci2 = int(dist[dist["tipo_problema"].isin([
        "backorder_prediction", "demand_forecasting", "inventory_control"
    ])]["Quantidade"].sum())
    total_eleg = int(dist["Quantidade"].sum())
    st.info(
        f"**Núcleo CI-2 (alvo primário):** {nucleo_ci2} artigos "
        f"({100 * nucleo_ci2 / max(total_eleg, 1):.1f}% dos elegíveis) — "
        f"predição de backorder, forecasting de demanda e controle de inventário."
    )

    st.divider()

    # --- Tabela detalhada dos elegíveis ---
    st.subheader("Lista de Artigos Elegíveis")
    filtro_tipo = st.multiselect(
        "Filtrar por tipo de problema",
        options=ORDEM_TIPO_PROBLEMA,
        default=None,
        placeholder="Todos",
        key="triagem_filtro_tipo",
    )

    df_tab = elegiveis_df.copy()
    if filtro_tipo:
        df_tab = df_tab[df_tab["tipo_problema"].isin(filtro_tipo)]

    df_tab = _calcular_citacoes_por_ano(df_tab)
    colunas_tab = ["Title", "Author/s", "Publication Year", "Source Title",
                   "Citing Works Count", "citacoes_por_ano", "tipo_problema", "DOI"]
    df_tab = df_tab[colunas_tab].rename(columns={
        "Title": "Título", "Author/s": "Autores", "Publication Year": "Ano",
        "Citing Works Count": "Citações",
        "citacoes_por_ano": "Citações/Ano",
        "tipo_problema": "Tipo Problema",
    }).sort_values("Citações", ascending=False)
    df_tab["Ano"] = df_tab["Ano"].apply(lambda x: str(int(x)) if pd.notna(x) else "N/D")
    df_tab["Citações/Ano"] = df_tab["Citações/Ano"].round(1)

    st.dataframe(
        df_tab.reset_index(drop=True),
        height=400,
        use_container_width=True,
        column_config={
            "Citações/Ano": st.column_config.NumberColumn(
                width="small",
                help="Citações ÷ anos desde a publicação — relevância ajustada pela idade do artigo",
                format="%.1f",
            ),
        },
    )


# ============================================================
# ABA 9 — REVISAO BIBLIOGRAFICA
# ============================================================
# Fonte de dados: data/tabela_revisao_bibliografica.csv
# Protocolo: docs/protocolo_revisao_bibliografica.md
# Gerado por: src/gerar_tabela_revisao.py

def exibir_kpis_revisao(df_r):
    """KPIs contextuais para a aba Revisão Bibliográfica."""
    total = len(df_r)
    revisados = int((df_r["revisado"] == "sim").sum())
    pct_revisado = 100 * revisados / max(total, 1)
    alta = int((df_r["relevancia_final"] == "alta").sum())
    excluidos = int((df_r["relevancia_final"] == "excluir").sum())

    # Concordancia tipo_problema_auto vs problema_validado (entre os revisados)
    revs = df_r[df_r["revisado"] == "sim"]
    revs_validados = revs[revs["problema_validado"] != ""]
    if len(revs_validados) > 0:
        concord = 100 * int((revs_validados["tipo_problema_auto"] == revs_validados["problema_validado"]).sum()) / len(revs_validados)
        concord_str = f"{concord:.0f}%"
    else:
        concord_str = "N/D"

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Elegíveis", f"{total:,}")
    col2.metric("Revisados", f"{revisados}/{total}")
    col3.metric("Progresso", f"{pct_revisado:.1f}%")
    col4.metric("Relev. Alta", f"{alta}")
    col5.metric("Excluídos FT", f"{excluidos}", help="Falsos positivos identificados no full-text review")
    col6.metric("Concord. Automática", concord_str,
                help="Precisão da classificação automática (tipo_problema_auto == problema_validado)")


def _grafico_distribuicao(df_col, cores_map, titulo, ordem=None):
    """Helper: cria barra horizontal de distribuicao para colunas de extracao manual."""
    if df_col.dropna().empty or (df_col == "").all():
        return None
    dist = df_col[df_col != ""].value_counts().reset_index()
    dist.columns = [titulo, "Quantidade"]
    if ordem:
        dist[titulo] = pd.Categorical(dist[titulo], categories=ordem, ordered=True)
        dist = dist.sort_values(titulo)
    fig = px.bar(
        dist, x="Quantidade", y=titulo, orientation="h",
        color=titulo, color_discrete_map=cores_map,
        text="Quantidade",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        height=260, showlegend=False, plot_bgcolor="white",
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(categoryorder="total ascending"),
    )
    return fig


def aba_revisao_bibliografica(df_r):
    """Aba: Revisão Bibliográfica — progresso e síntese da extração manual."""
    st.subheader("Extração Manual de Dados — Full-Text Review")
    st.caption(
        "Acompanhamento do preenchimento de `data/tabela_revisao_bibliografica.xlsx` durante a "
        "leitura de texto completo. Protocolo: `docs/protocolo_revisao_bibliografica.md`. "
        "Recarregue o dashboard (Clear Cache → Rerun) para atualizar após novos preenchimentos."
    )

    total = len(df_r)
    revisados = int((df_r["revisado"] == "sim").sum())
    pct = revisados / max(total, 1)

    # --- Barra de progresso visual ---
    st.markdown(f"**Progresso da revisão:** {revisados}/{total} artigos ({100 * pct:.1f}%)")
    st.progress(pct)

    if revisados == 0:
        st.warning(
            "⚠️ Nenhum artigo foi revisado ainda (`revisado = sim`). "
            "Os gráficos abaixo serão populados conforme o preenchimento manual avançar. "
            "Abra `data/tabela_revisao_bibliografica.xlsx` e inicie a extração seguindo o protocolo."
        )

    st.divider()

    # --- Linha 1: relevancia + resultado_qml ---
    st.subheader("Síntese da Revisão")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Relevância Final** (decisão humana)")
        fig = _grafico_distribuicao(
            df_r["relevancia_final"], CORES_RELEVANCIA, "relevancia_final",
            ordem=["alta", "media", "baixa", "excluir"],
        )
        if fig:
            st.plotly_chart(fig, width="stretch")
        else:
            st.caption("— aguardando preenchimento —")

    with c2:
        st.markdown("**QML vs Baseline Clássico**")
        fig = _grafico_distribuicao(
            df_r["resultado_qml_vs_classico"], CORES_RESULTADO_QML, "resultado_qml_vs_classico",
            ordem=["melhor", "equivalente", "pior", "nao_comparado"],
        )
        if fig:
            st.plotly_chart(fig, width="stretch")
        else:
            st.caption("— aguardando preenchimento —")

    # --- Linha 2: metodo_qml + hardware ---
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("**Método QML**")
        fig = _grafico_distribuicao(
            df_r["metodo_qml"], {}, "metodo_qml",
        )
        if fig:
            fig.update_traces(marker_color=CORES["primary"])
            st.plotly_chart(fig, width="stretch")
        else:
            st.caption("— aguardando preenchimento —")

    with c4:
        st.markdown("**Tipo de Hardware**")
        fig = _grafico_distribuicao(
            df_r["hardware"], CORES_HARDWARE, "hardware",
            ordem=["simulator", "real_quantum", "both"],
        )
        if fig:
            st.plotly_chart(fig, width="stretch")
        else:
            st.caption("— aguardando preenchimento —")

    st.divider()

    # --- Concordancia tipo_problema_auto vs problema_validado ---
    st.subheader("Concordância da Classificação Automática")
    st.caption(
        "Compara `tipo_problema_auto` (classificação automática por regex em Title+Abstract) com "
        "`problema_validado` (validação humana após leitura do texto completo). "
        "Mede a precisão do pipeline automatizado de classificação."
    )

    revs = df_r[(df_r["revisado"] == "sim") & (df_r["problema_validado"] != "")]
    if len(revs) == 0:
        st.info(
            "Preencha a coluna `problema_validado` em pelo menos 1 artigo revisado para "
            "calcular a concordância com a classificação automática."
        )
    else:
        concord_count = int((revs["tipo_problema_auto"] == revs["problema_validado"]).sum())
        discord_count = len(revs) - concord_count
        concord_pct = 100 * concord_count / len(revs)

        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("Revisados com validação", f"{len(revs)}")
        cc2.metric("Concordantes", f"{concord_count}", delta=f"{concord_pct:.1f}%")
        cc3.metric("Discordantes", f"{discord_count}")

        # Heatmap de confusao
        confusao = pd.crosstab(
            revs["tipo_problema_auto"], revs["problema_validado"],
        )
        fig_conf = px.imshow(
            confusao, text_auto=True, aspect="auto",
            color_continuous_scale="Blues",
            labels=dict(x="Problema Validado (manual)", y="Tipo Problema Auto", color="Artigos"),
        )
        fig_conf.update_layout(height=450, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_conf, width="stretch")

    st.divider()

    # --- Tabela filtravel e export ---
    st.subheader("Artigos — Filtros e Exportação")

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        filtro_rel = st.multiselect(
            "Relevância Final",
            options=["alta", "media", "baixa", "excluir"],
            default=None, placeholder="Todas",
            key="revisao_filtro_rel",
        )
    with col_f2:
        filtro_tipo_auto = st.multiselect(
            "Tipo de Problema (auto)",
            options=ORDEM_TIPO_PROBLEMA,
            default=None, placeholder="Todos",
            key="revisao_filtro_tipo",
        )
    with col_f3:
        # Filtro pelo campo 'revisado' da planilha (valores: 'sim', 'nao', '' = pendente)
        filtro_revisado = st.multiselect(
            "Revisado",
            options=["sim", "nao", "pendente"],
            default=None, placeholder="Todos",
            key="revisao_filtro_revisado",
            help=(
                "Filtra pelo campo `revisado` da planilha. "
                "`sim` = artigos já lidos · `nao` = selecionados mas ainda não lidos · "
                "`pendente` = campo em branco (não selecionado para leitura)."
            ),
        )
    with col_f4:
        apenas_revisados = st.radio(
            "Status de revisão",
            options=["Todos", "Apenas revisados", "Apenas pendentes"],
            horizontal=False, key="revisao_filtro_status",
        )

    df_tab = df_r.copy()
    if filtro_rel:
        df_tab = df_tab[df_tab["relevancia_final"].isin(filtro_rel)]
    if filtro_tipo_auto:
        df_tab = df_tab[df_tab["tipo_problema_auto"].isin(filtro_tipo_auto)]
    if filtro_revisado:
        # Normalizar: "pendente" no filtro = string vazia na coluna
        valores_rev = [("" if v == "pendente" else v) for v in filtro_revisado]
        df_tab = df_tab[df_tab["revisado"].fillna("").isin(valores_rev)]
    if apenas_revisados == "Apenas revisados":
        df_tab = df_tab[df_tab["revisado"] == "sim"]
    elif apenas_revisados == "Apenas pendentes":
        df_tab = df_tab[df_tab["revisado"] != "sim"]

    st.caption(f"**{len(df_tab)} artigo(s)** após filtros.")

    colunas_exibir = [
        "titulo", "autores_completo", "ano", "venue", "tipo_problema_auto",
        "revisado", "relevancia_final", "problema_validado",
        "metodo_qml", "baseline_classico", "resultado_qml_vs_classico",
        "hardware", "citing_works", "doi",
    ]
    colunas_exibir = [c for c in colunas_exibir if c in df_tab.columns]

    df_exibir = df_tab[colunas_exibir].copy()
    df_exibir["ano"] = df_exibir["ano"].apply(
        lambda x: str(int(x)) if pd.notna(x) else "N/D"
    )

    st.dataframe(df_exibir.reset_index(drop=True), height=420, use_container_width=True)

    # --- Export subset alta ---
    st.markdown("**Exportar corpus de síntese (`relevancia_final = alta`)**")
    df_alta = df_r[df_r["relevancia_final"] == "alta"]
    if len(df_alta) == 0:
        st.caption("— Nenhum artigo marcado como `alta` relevância ainda —")
    else:
        csv_bytes = df_alta.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"⬇ Baixar {len(df_alta)} artigos (alta relevância) — CSV",
            data=csv_bytes,
            file_name="corpus_sintese_alta_relevancia.csv",
            mime="text/csv",
        )


# ============================================================
# ABA — CONCLUSÕES E PRÓXIMOS PASSOS
# ============================================================
# Narrativa de fechamento: consolida o que foi aprendido ate aqui no pipeline
# PRISMA-ScR e lista o roadmap da revisao bibliografica completa.

def aba_conclusoes(df_dedup, df_triagem, df_revisao):
    """Síntese dos achados do pipeline e roadmap da revisão bibliográfica."""
    # --- KPIs de fechamento ---
    total_bruto = int(df_dedup["total_bruto"].iloc[0]) if df_dedup is not None and "total_bruto" in df_dedup.columns else 0
    total_unicos = int(df_dedup["total_unico"].iloc[0]) if df_dedup is not None and "total_unico" in df_dedup.columns else 0
    elegiveis = int((df_triagem["fase2_decisao"] == "incluir").sum()) if "fase2_decisao" in df_triagem.columns else 0
    revisados = int((df_revisao["revisado"] == "sim").sum()) if "revisado" in df_revisao.columns else 0
    alta_rel = int((df_revisao["relevancia_final"] == "alta").sum()) if "relevancia_final" in df_revisao.columns else 0

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Registros Brutos", f"{total_bruto:,}")
    k2.metric("Corpus Único", f"{total_unicos:,}")
    k3.metric("Elegíveis (PRISMA-ScR)", f"{elegiveis:,}")
    k4.metric("Revisados (Full-Text)", f"{revisados:,}")
    k5.metric("Alta Relevância", f"{alta_rel:,}")
    st.divider()

    # --- Conclusões ---
    st.subheader("📌 Conclusões até o Momento")
    st.markdown(
        f"""
**1. Pipeline PRISMA-ScR automatizado é viável em QML × Supply Chain.**
A redução de **{total_bruto:,} registros brutos → {total_unicos:,} únicos → {elegiveis:,} elegíveis**
({100 * elegiveis / max(total_bruto, 1):.1f}% do bruto) demonstra que uma triagem por regras
(CE-1 a CE-5) aplicada a título + abstract + Fields of Study consegue isolar o escopo temático
com **precisão estimada ~90%+** após 5 iterações de refinamento.

**2. O gargalo da literatura QML é a contaminação cross-domain.**
O critério CE-3 (domínio fora de escopo) — em suas duas variantes (padrão e forte) — foi
responsável por **51% das exclusões**. O campo QML atrai pesquisadores de física, saúde, finanças
e energia que reutilizam as mesmas arquiteturas (QNN, VQC, QSVM) em problemas distintos. Sem
a filtragem agressiva por domínio, o corpus seria dominado por trabalhos fora de supply chain.

**3. A qualidade das strings de busca pesa mais que a sofisticação do filtro.**
A remoção das strings #10–#14 (Iter. 2) cortou o corpus pela metade com perda mínima de
relevantes — um único ajuste na fonte superou várias rodadas de tuning dos critérios de exclusão.
Lição: **investir na construção da string antes de sofisticar a triagem**.

**4. Loops humano-no-processo são indispensáveis.**
As Iterações 4 e 5 mostram que a inspeção manual de amostras detecta padrões de falsos positivos
que o protocolo inicial não antecipa (ex.: LNG, farmácia, química quântica, comunicação quântica,
COVID, manutenção veicular). A realimentação das keywords nas listas de exclusão elevou a precisão
de ~80% para ~90%+ em duas passadas.

**5. O núcleo CI-2 está identificado e é compacto.**
Dos {elegiveis:,} elegíveis, **53 artigos (20,3%)** concentram o alvo primário da pesquisa
(backorder prediction, demand forecasting, inventory control). Essa densidade é **positiva** —
um corpus enxuto e bem caracterizado permite uma revisão bibliográfica profunda dentro do prazo
do mestrado, sem sacrificar cobertura.

**6. O dashboard é a fonte única de verdade do progresso.**
A integração direta com `tabela_revisao_bibliografica.xlsx` (via `mtime` como cache-key)
permite que o preenchimento manual da revisão apareça ao vivo no dashboard, fechando o
ciclo extração → análise → comunicação.
"""
    )
    st.divider()

    # --- Próximos Passos ---
    st.subheader("🚀 Próximos Passos")
    st.markdown(
        """
**Revisão Bibliográfica**

1. **Full-text review dos 261 elegíveis**, em ordem de prioridade por `tipo_problema`

2. **Preenchimento da planilha `tabela_revisao_bibliografica.xlsx`**

3. **Validação da classificação automática** (`tipo_problema_auto` vs. `problema_validado`) —
   calcular concordância final e reportar no dashboard como métrica de qualidade do classificador.

**Síntese e Análise**

4. **Consolidação do corpus de síntese** (`relevancia_final = alta`) — exportar via botão
   do dashboard e produzir a tabela final do artigo/dissertação.

5. **Análise comparativa QML vs. Clássico** por tipo de problema:
   - Agregação de métricas (`diferenca_percentual`) por `metodo_qml`, `hardware`, `dataset_tamanho`.
   - Identificação de padrões: quando QML supera clássico? (número de qubits, tamanho de dataset, regime NISQ vs. fault-tolerant).

6. **Mapeamento de lacunas de pesquisa** — cruzar `tipo_problema` × `metodo_qml` ×
   `resultado_qml_vs_classico` para identificar combinações sub-representadas que justifiquem
   contribuição original.

**Prototipação**

7. **Prova-de-conceito em tema á ser definido** — implementar baseline clássico (XGBoost/LightGBM)
   + pipeline QML (QSVM ou VQC) em um dataset público (Kaggle Back Order / UCI Online Retail)
   e comparar métricas sob constraints NISQ (≤ 20 qubits, ruído real).

8. **Redação do artigo de revisão sistemática** seguindo o template PRISMA-ScR
   (checklist completo + diagrama de fluxo atualizado + tabela de síntese).

9. **Publicação do dashboard como artefato reproduzível** — README com instruções de execução,
   dependências fixadas (`requirements.txt` / `pyproject.toml`), exemplos dos CSVs de entrada.
"""
    )
    st.divider()

    # --- Riscos e Pontos de Atenção ---
    st.subheader("⚠️ Riscos e Pontos de Atenção")
    st.markdown(
        """
- **Falsos positivos residuais na triagem.** Apesar da precisão estimada de ~90%+, ~26 artigos dos 261
  ainda podem ser fora de escopo. Serão filtrados no full-text review via `relevancia_final = excluir`.
- **Falsos negativos não observáveis.** Artigos descartados nas fases 1/2 não são auditáveis em massa;
  risco mitigado pelas 5 iterações e pela lista `palavras_dominio_manter` (safety net).
- **Viés de idioma.** A triagem e as strings são em inglês — trabalhos relevantes em chinês/alemão/etc.
  que o Lens.org indexa podem estar sub-representados.
- **Viés de recência de citações.** Artigos recentes têm poucas citações por falta de tempo, não por falta
  de relevância — mitigado pela métrica `Citações/Ano` já presente no dashboard.
- **Drift do escopo NISQ.** Hardware quântico evolui rapidamente; resultados publicados em 2021–2022
  podem estar obsoletos em 2026 (mais qubits, menos ruído). Tratar como contexto histórico na síntese.
"""
    )


# ============================================================
# ABA — HOME (VISÃO DO PIPELINE)
# ============================================================
# Storytelling de entrada: funil macro da pesquisa em um unico visual.
# Fontes: resumo_deduplicacao.csv + artigos_unicos_triagem.csv + tabela_revisao_bibliografica.csv

def aba_home(df_dedup, df_triagem, df_revisao):
    """Visao geral do pipeline de pesquisa: funil macro das 4 etapas."""
    # Montar valores do funil a partir das fontes reais
    total_bruto = int(df_dedup["total_bruto"].iloc[0]) if df_dedup is not None and "total_bruto" in df_dedup.columns else 0
    total_unicos = int(df_dedup["total_unico"].iloc[0]) if df_dedup is not None and "total_unico" in df_dedup.columns else len(df_triagem)
    elegiveis = int((df_triagem["fase2_decisao"] == "incluir").sum()) if "fase2_decisao" in df_triagem.columns else len(df_revisao)
    revisados = int((df_revisao["revisado"].astype(str).str.lower().isin(["true", "sim", "1"])).sum()) if "revisado" in df_revisao.columns else 0

    # KPIs fixos de contexto no topo (padrao das demais abas: cards -> divider -> visual)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Etapa 0 — Busca", f"{total_bruto:,}", help="Registros brutos das 35 strings de busca no Lens.org")
    col2.metric("Etapa 1 — Deduplicação", f"{total_unicos:,}", help="Após remoção de duplicatas por DOI + título")
    col3.metric("Etapa 3 — Elegíveis", f"{elegiveis:,}", help="Após triagem PRISMA-ScR em duas fases")
    col4.metric("Etapa 4 — Revisados", f"{revisados:,}", help="Artigos com full-text extraído manualmente")
    st.divider()

    st.subheader("Pipeline da Revisão Bibliográfica")
    st.caption(
        "Da busca bruta ao corpus revisado — visão macro das 4 etapas do pipeline. "
        "Selecione a aba correspondente para explorar cada etapa em detalhe."
    )

    estagios = ["Busca bruta (Lens.org)", "Únicos (pós-dedup)", "Elegíveis (PRISMA-ScR)", "Revisados (full-text)"]
    valores = [total_bruto, total_unicos, elegiveis, revisados]

    fig_funil = go.Figure(go.Funnel(
        y=estagios,
        x=valores,
        textinfo="value+percent initial",
        marker=dict(color=[CORES["accent"], CORES["secondary"], CORES["primary"], CORES["dark"]]),
    ))
    fig_funil.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_funil, width="stretch")


# ============================================================
# ABA — ETAPA 1: DEDUPLICAÇÃO
# ============================================================
# Fonte: resumo_deduplicacao.csv (1 linha de metricas) + artigos_unicos.csv

def aba_deduplicacao(df_dedup, df_unicos):
    """KPIs e mini-funil da etapa de deduplicação."""
    st.subheader("Etapa 1 — Deduplicação do Corpus")
    st.caption(
        "Remoção de duplicatas por DOI (match exato) e por título (fuzzy match). "
        "Artigos aparecendo em múltiplas strings de busca são contabilizados uma única vez."
    )

    if df_dedup is None or df_dedup.empty:
        st.warning("`data/resumo_deduplicacao.csv` não encontrado.")
        return

    row = df_dedup.iloc[0]
    total_bruto = int(row.get("total_bruto", 0))
    total_unico = int(row.get("total_unico", len(df_unicos)))
    removidos = int(row.get("total_removido", total_bruto - total_unico))
    rem_doi = int(row.get("removidos_por_doi", 0))
    rem_tit = int(row.get("removidos_por_titulo", 0))
    rem_cross = int(row.get("removidos_por_titulo_cross_doi", 0))
    taxa_sobrep = float(row.get("taxa_sobreposicao_pct", 0.0))

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros Brutos", f"{total_bruto:,}")
    col2.metric("Artigos Únicos", f"{total_unico:,}", delta=f"-{removidos} duplicatas", delta_color="inverse")
    col3.metric("Removidos por DOI", f"{rem_doi:,}")
    col4.metric("Taxa de Sobreposição", f"{taxa_sobrep:.1f}%",
                help="Percentual do corpus bruto que era redundante entre strings de busca")

    st.markdown("")

    # Mini-funil de deduplicacao
    col_esq, col_dir = st.columns([2, 1])
    with col_esq:
        st.markdown("##### Fluxo da Deduplicação")
        estagios = ["Registros brutos", "Após dedup por DOI", "Após dedup por título"]
        valores = [total_bruto, max(total_bruto - rem_doi, 0), total_unico]
        fig = go.Figure(go.Funnel(
            y=estagios, x=valores,
            textinfo="value+percent initial",
            marker=dict(color=[CORES["accent"], CORES["secondary"], CORES["primary"]]),
        ))
        fig.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, width="stretch")

    with col_dir:
        st.markdown("##### Detalhamento das Remoções")
        det = pd.DataFrame({
            "Critério": ["DOI duplicado", "Título duplicado", "Título (cross-DOI)"],
            "Removidos": [rem_doi, rem_tit, rem_cross],
        })
        fig_det = px.bar(det, x="Removidos", y="Critério", orientation="h",
                        color_discrete_sequence=[CORES["danger"]])
        fig_det.update_layout(height=320, plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_det, width="stretch")
        st.caption("**Título (cross-DOI):** artigos com DOIs diferentes mas mesmo título.")


# ============================================================
# ABA — ETAPA 2: ANÁLISE BIBLIOMÉTRICA DO CORPUS ÚNICO
# ============================================================
# Agrupa Visao Geral + Impacto e Citacoes + Campos de Estudo em sub-abas.
# Fonte: artigos_unicos.csv (2.471 artigos) filtrado pela sidebar.

def aba_bibliometria(df):
    """Caracterização bibliométrica do corpus único — produção, impacto, temas."""
    st.caption(
        "Caracterização do corpus único (2.471 artigos pós-deduplicação). "
        "Use os filtros da sidebar para restringir por período, tipo, string, prioridade, etc."
    )

    sub1, sub2 = st.tabs([
        "📈 Produção e Perfil",
        "🏆 Impacto e Temas de Pesquisa",
    ])
    with sub1:
        aba_visao_geral(df)
    with sub2:
        # Ordem narrativa:
        #   1. Bubble "Artigos Mais Citados ao Longo do Tempo" (citacoes totais)
        #   2. Treemap "Top 30 - Fields of Study"
        #   3. Leaderboard "Relevancia Ajustada — Top 30 por Citacoes/Ano"
        #   4. Tabela "Top 20 Artigos Mais Citados" (com Citacoes/Ano, Campo e Keywords)
        #   5. WordCloud "Nuvem de Palavras — Keywords"
        aba_impacto(df)
        st.divider()
        aba_treemap_fields(df)
        st.divider()
        aba_relevancia_ajustada(df)
        st.divider()
        aba_top_citados(df)
        st.divider()
        aba_wordcloud_keywords(df)


# ============================================================
# EXECUCAO PRINCIPAL
# ============================================================
# Fluxo do Streamlit: o script inteiro e re-executado de cima para baixo
# toda vez que o usuario interage com qualquer widget (slider, multiselect, etc.).
# O @st.cache_data garante que os CSVs nao sejam relidos do disco a cada re-execucao.

def main():
    # st.title(): titulo grande da pagina (equivale a <h1> em HTML).
    st.title("Análise Bibliométrica — QML Supply Chain")
    st.caption(
        "Pipeline de revisão sistemática PRISMA-ScR: 1.792 artigos brutos → 1.231 únicos → "
        "261 elegíveis para full-text review. Quantum Machine Learning aplicado a previsão de "
        "demanda e controle de inventário em Supply Chain | Mestrado Profissional — SENAI CIMATEC"
    )

    # 1. Carregar dados (3 fontes, todas cacheadas)
    df = carregar_dados()
    df_triagem = carregar_dados_triagem()
    # Usa mtime do xlsx como parte do cache-key → planilha salva invalida cache
    caminho_revisao_xlsx = os.path.join(PASTA_PROJETO, "data", "tabela_revisao_bibliografica.xlsx")
    mtime_revisao = (
        os.path.getmtime(caminho_revisao_xlsx)
        if os.path.exists(caminho_revisao_xlsx) else 0.0
    )
    df_revisao = carregar_dados_revisao(mtime_revisao)

    # 1b. Carregar estatisticas de deduplicacao (CSV com 1 linha de metricas)
    try:
        df_dedup = pd.read_csv(os.path.join(PASTA_PROJETO, "data", "resumo_deduplicacao.csv"))
    except FileNotFoundError:
        df_dedup = None

    # 2. Filtros da sidebar (afetam a aba de Analise Bibliometrica).
    #    Os dados de triagem e revisao possuem seus proprios filtros internos.
    df_filtrado = criar_filtros(df)

    # 5. Abas de navegacao organizadas por ETAPAS da pesquisa bibliografica.
    #    Storytelling linear: do universo bruto ao corpus revisado.
    #    - Home:            funil macro das 4 etapas
    #    - Etapa 0:         Estrategia de Busca (35 strings, volume, sobreposicao)
    #    - Etapa 1:         Deduplicacao (KPIs + mini-funil)
    #    - Etapa 2:         Analise Bibliometrica (producao, impacto, temas)
    #    - Etapa 3:         Triagem PRISMA-ScR (2.471 -> 261 elegiveis)
    #    - Etapa 4:         Revisao Bibliografica (full-text extraction)
    # Navegação por st.radio persiste a aba ativa via session_state — evita que
    # widgets internos (multiselect, filtros) resetem para a primeira aba no rerun.
    ABAS = [
        "🏠 Pipeline",
        "🔎 Estratégia de Busca",
        "🧹 Deduplicação",
        "📚 Análise Bibliométrica",
        "✅ Triagem PRISMA-ScR",
        "📖 Revisão Bibliográfica",
        "🎯 Conclusões & Próximos Passos",
    ]
    aba_ativa = st.radio(
        "Navegação", ABAS, horizontal=True, key="aba_ativa", label_visibility="collapsed",
    )
    st.divider()

    if aba_ativa == ABAS[0]:
        aba_home(df_dedup, df_triagem, df_revisao)

    elif aba_ativa == ABAS[1]:
        # KPIs fixos da estrategia de busca: escopo das 35 strings e volumes brutos
        total_strings = len(STRINGS_BUSCA)
        total_bruto_busca = int(df_dedup["total_bruto"].iloc[0]) if df_dedup is not None and "total_bruto" in df_dedup.columns else 0
        total_unicos_busca = int(df_dedup["total_unico"].iloc[0]) if df_dedup is not None and "total_unico" in df_dedup.columns else len(df)
        taxa_sobrep = float(df_dedup["taxa_sobreposicao_pct"].iloc[0]) if df_dedup is not None and "taxa_sobreposicao_pct" in df_dedup.columns else 0.0
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Strings de Busca", f"{total_strings}",
                  help="Combinações booleanas aplicadas no Lens.org")
        k2.metric("Registros Brutos", f"{total_bruto_busca:,}")
        k3.metric("Artigos Únicos", f"{total_unicos_busca:,}")
        k4.metric("Taxa de Sobreposição", f"{taxa_sobrep:.1f}%",
                  help="% do corpus bruto redundante entre strings")
        st.divider()
        aba_strings(df_filtrado)

    elif aba_ativa == ABAS[2]:
        # KPIs da deduplicacao ja estao embutidos em aba_deduplicacao()
        aba_deduplicacao(df_dedup, df_filtrado)

    elif aba_ativa == ABAS[3]:
        # KPIs fixos do corpus bibliometrico (filtrado pela sidebar)
        exibir_kpis(df_filtrado, df_dedup=None)
        st.divider()
        aba_bibliometria(df_filtrado)

    elif aba_ativa == ABAS[4]:
        # KPIs fixos da triagem PRISMA-ScR
        exibir_kpis_triagem(df_triagem)
        st.divider()
        aba_triagem_prisma(df_triagem)

    elif aba_ativa == ABAS[5]:
        # KPIs fixos da revisao bibliografica (progresso de extracao)
        exibir_kpis_revisao(df_revisao)
        st.divider()
        aba_revisao_bibliografica(df_revisao)

    elif aba_ativa == ABAS[6]:
        aba_conclusoes(df_dedup, df_triagem, df_revisao)


# Ponto de entrada: so executa quando o script e rodado diretamente
# (nao quando importado como modulo). O Streamlit chama este arquivo diretamente.
if __name__ == "__main__":
    main()
