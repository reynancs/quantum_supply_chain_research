"""
Script de Triagem de Artigos — Fase 2 (Protocolo de Selecao)

Este script faz o seguinte:
1. Le o arquivo de artigos unicos (data/artigos_unicos.csv)
2. Aplica criterios de exclusao em 2 fases:
   - Fase 1: triagem por titulo + tipo de publicacao
   - Fase 2: triagem por titulo + abstract
3. Classifica cada artigo (incluir/excluir) sem remover nenhum
4. Exporta o resultado com as novas colunas de decisao

Como usar:
    python src/triagem_artigos.py

Entrada: data/artigos_unicos.csv (2.471 artigos deduplicados)
Saida:   data/artigos_unicos_triagem.csv (mesmos 2.471 artigos + colunas de triagem)

Protocolo completo: docs/protocolo_triagem.md
"""

import os
import re
import pandas as pd
from datetime import datetime


# ============================================================
# CONFIGURACAO — Caminhos dos arquivos
# ============================================================

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_ENTRADA = os.path.join(PASTA_PROJETO, "data", "artigos_unicos.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_PROJETO, "data", "artigos_unicos_triagem.csv")


# ============================================================
# CONFIGURACAO — Criterios de Exclusao (palavras-chave)
# ============================================================

# CE-1: Otimizacao quantica pura SEM componente de Machine Learning
# Logica: excluir se tem_otimizacao E NAO tem_ml
CONFIG_CE1 = {
    "palavras_otimizacao": [
        "qaoa", "quantum approximate optimization",
        "quantum annealing", "adiabatic quantum",
        "variational quantum eigensolver", "vqe",
        "ising model", "ising formulation",
        "maxcut", "max-cut", "max cut",
        "combinatorial optimization",
        "quadratic unconstrained binary optimization", "qubo",
        "d-wave",
        "quantum walk", "grover search", "grover's algorithm",
        "quantum counting",
        "quantum integer programming",
    ],
    "palavras_ml": [
        # Arquiteturas QML
        "quantum machine learning", "quantum neural network", "qnn",
        "variational quantum circuit", "vqc",
        "parameterized quantum circuit", "pqc",
        "quantum kernel", "quantum support vector", "qsvm",
        "quantum reservoir", "quantum convolutional",
        "quantum transfer learning", "quantum classifier",
        "quantum reinforcement learning",
        "hybrid quantum-classical", "hybrid quantum classical",
        "quantum generative", "quantum autoencoder",
        "quantum boltzmann",
        "quantum feature map",
        "quantum embedding",
        # Termos gerais de ML
        "machine learning", "deep learning", "neural network",
        "classification", "regression", "training",
        "supervised", "unsupervised",
        "forecasting", "prediction", "predictive",
        "backorder", "demand forecast",
    ],
}

# CE-2: QML mencionado apenas como trabalho futuro (Fase 2 apenas)
# Logica: excluir se tem_futuro E NAO tem_experimento
CONFIG_CE2 = {
    "palavras_futuro": [
        "future work", "future research", "future direction",
        "could be applied", "could be explored",
        "potential application", "potential of quantum",
        "promising direction", "promising avenue",
        "remains to be explored", "left for future",
        "as a next step",
        "we plan to", "we intend to",
    ],
    "palavras_experimento": [
        "experiment", "experimental result",
        "we implement", "we implemented",
        "we propose and evaluate", "we propose and test",
        "we train", "we trained",
        "accuracy", "precision", "recall", "f1",
        "mean squared error", "mse", "rmse", "mae",
        "benchmark", "benchmarked",
        "dataset", "data set",
        "simulation result", "simulated",
        "our result", "results show", "results demonstrate",
        "outperform", "outperforms",
        "tested on", "evaluated on",
        "quantum circuit", "qiskit", "pennylane", "cirq",
    ],
}

# CE-3: Dominio de aplicacao fora de supply chain/logistica
# Logica: excluir se tem_dominio_excluir E NAO tem_dominio_manter
CONFIG_CE3 = {
    "palavras_dominio_excluir": [
        # Biomedico / Saude
        "healthcare", "drug discovery", "drug design", "drug development",
        "protein folding", "protein structure", "protein-ligand",
        "molecular docking", "molecular simulation",
        "genomic", "genome", "gene expression", "dna sequencing",
        "clinical trial", "clinical diagnosis", "clinical study",
        "cancer detection", "cancer diagnosis", "tumor",
        "medical imaging", "medical diagnosis",
        "disease detection", "disease diagnosis", "disease prediction",
        "pathology", "radiology", "Biotechnology",
        "electroencephalog", "Biochemistry", "Pharmaceutical",
        "ecg", "electrocardiog", "Nanoparticle", "nanoscience",
        "brain-computer interface", "Biochemical", "Health services",
        "Pain Treatment", "DNA", "RNA", "protein", "biological",
        "neuroscience",
        "rheumatoid", "arthritis", "diabetes", "mental health",
        "mental disorder", "cardiovascular", "cardiology",
        "ophthalmology", "thyroid", "stroke prediction",
        "vaccine", "vaccination", "drug response",
        "health prediction", "health forecasting",
        "animal nutrition", "dairy", "veterinary",
        # Financas / Portfolio
        "portfolio optimization", "portfolio management",
        "stock market", "stock price", "stock trading",
        "financial trading", "option pricing", "credit scoring",
        "cryptocurrency price", "economic", "Financial Risk",
        "Cryptocurrency", "finance", "Financial forecasting",
        "fraud detection", "financial market", "loan risk",
        "loan eligibility", "credit card", "inflation",
        "capital market", "financial performance",
        "stock prediction", "stock forecasting",
        # Telecomunicacoes / Wireless / 6G
        "6g", "5g network", "5g communication",
        "antenna design", "beamforming",
        "wireless network", "wireless communication",
        "spectrum allocation", "spectrum management",
        "channel estimation", "Electrical engineering",
        "telecommunication", "Computer network",
        "radar signal", "Geography", "IIoT",
        "Geospatial Simulation",
        "satellite communication", "OFDM",
        # Fisica pura / Ciencia de Materiais
        "graphene", "photonic", "photonics",
        "topological insulator", "Astronomy",
        "superconducting qubit design",
        "lattice gauge", "quantum chromodynamics",
        "high energy physics", "particle physics",
        "condensed matter", "chemistry",
        "thermodynamics", "cyber-physical system",
        "Power system simulation", "Hurricanes",
        "Rydberg", "Jaynes-Cummings", "anyon", "anyonic",
        "entanglement detection", "quantum phase transition",
        "Kerr nonlinear", "echo state property",
        "quantum propagator", "Feynman path",
        "orbital angular momentum", "spin-network",
        "dissipation", "quantum reservoir probing",
        "gravitational wave", "gravitational-wave",
        "quantum chromodynamic", "lattice surgery",
        "Fibonacci", "quantum game",
        # Energia
        "solar cell", "solar energy", "solar panel",
        "solar irradiance", "solar irradiation", "photovoltaic",
        "wind energy", "wind farm", "wind power",
        "battery degradation", "battery management", "battery health",
        "power grid", "smart grid", "energy grid",
        "electric vehicle charging", "Lithium-ion",
        "load forecasting", "load prediction", "electric load",
        "electricity price", "electricity forecast",
        "microgrid", "microgrids", "power plant", "hydropower",
        # Clima / Meteorologia / Geofisica
        "weather forecast", "weather prediction", "weather forecasting",
        "rainfall", "typhoon", "cyclone",
        "air quality", "drought", "meteorological",
        "earthquake", "seismic", "volcano",
        "climate forecasting", "climate prediction",
        "corrosion prediction", "corrosion inhibitor",
        "carbonation depth",
        # Agricultura
        "crop yield", "crop prediction", "Climate change",
        "soil moisture", "agricultural", "agriculture",
        "Ecology", "Biology", "Water demand prediction",
        # Imagem / Visao / NLP (nao-logistica)
        "face recognition", "face detection",
        "speech recognition", "voice recognition",
        "music generation", "music composition",
        "autonomous driving", "self-driving",
        "satellite image", "Linguistics",
        "image classification", "image recognition",
        "object detection", "video surveillance",
        "remote sensing", "hyperspectral",
        "sentiment analysis", "sentiment classification",
        "speech emotion", "natural language processing",
        # Ciberseguranca (nao-supply-chain)
        "intrusion detection", "malware detection",
        "Malware", "Cryptography", "shor algorithm",
        "quantum key distribution", "qkd",
        "quantum cryptography", "Security",
        "post-quantum cryptography", "Encryption",
        "military", "defense", "cybersecurity",
        "Hardware Security", "Blockchain",
        # Transportes / Mobilidade (nao-logistica)
        "mobility", "Public transport",
        "Smart City", "traffic prediction", "traffic flow",
        # Social / Humanidades
        "social", "Sociology", "psychology",
        "education", "linguistics",
        "sociotechnical", "Social Networks",
        # Junk / Editorial
        "Table of content", "Table of Contents",
        "Notes from the Editor", "Editorial message",
        "Subject Index", "Conference Main Schedule",
        "National Science Foundation",
        "Contents", "Issue Introduction",
        # Outros dominios
        "Ethnography", "Work Systems Theory",
        "Policy Violation", "Decision Optimization",
        "hearing protector", "football club",
        "quantum chemistry", "molecular property",
        "alloy", "high-entropy alloy",
        "polymer", "soy sauce",
        # Patentes / Revisoes genericas de QML (fora de SC)
        "patent", "patent review", "patent analysis", "patent landscape",
        # Nanotecnologia / Nanociencia (consolidar)
        "nanotechnology", "nanotech", "nanomaterial", "nanostructure",
        "nanotube", "nanofluid",
        # Saude digital / Biomedico (complementos)
        "digital health", "e-health", "ehealth", "telemedicine",
        "biomedical",
        # Espaco / Satelite (complementos — "satellite communication" ja existe acima)
        "space mission", "space exploration", "aerospace",
        # Energia nuclear / Fusao
        "nuclear fusion", "plasma physics", "tokamak",
        # Gas natural / LNG / Infraestrutura energetica
        "lng", "liquefied natural gas", "natural gas distribution",
        "mobile power plant", "low-carbon energy",
        "energy infrastructure",
        # Farmacia / Dispensacao / Saude (complementos)
        "pharmacy", "pharmaceutical dispensing", "medication dispensing",
        "central fill", "robotic dispensing",
        "functional near-infrared", "fnirs", "fear detection",
        # Quimica / Fisica quantica (complementos)
        "hamiltonian framework", "effective model hamiltonian",
        "nonadiabatic dynamics", "non-adiabatic dynamics",
        "condensed phase", "wave-particle duality",
        # Comunicacao quantica (nao-logistica)
        "quantum communication", "quantum communications",
        # COVID / Pandemia (objeto de estudo nao-QML)
        "covid-19", "covid", "pandemic impact",
        # Manutencao preditiva veicular (nao-logistica)
        "vehicle break down", "vehicle breakdown", "breakdown prediction",
        # Politica economica / Comercio internacional
        "export control", "export controls", "trade sanction",
        "economic resilience", "corporate resilience",
        # Clima / Meteorologia (complementos — "weather forecast/prediction" ja existem)
        "weather", "forecasting the weather",
        # Baterias (complementos — "Lithium-ion" ja existe)
        "lifepo4", "battery lifetime", "lithium iron phosphate",
        # QML generico sem ancora de SC
        "non-trivial classification", "quantum kernel framework",
        "shallow entangled circuits", "ibm devices",
        # Semicondutores
        "semiconductor manufacturing", "semiconductor industry",
        # Gestao / Negocios / Economia
        "innovation ecosystem", "human-centric economy",
        "ESG goals", "ESG reporting", "augmented reality",
        # Geracao procedural de conteudo / Jogos
        "level generation", "procedural content",
        # Engenharia de software
        "microservice", "microservices",
        # Editorial / Social
        "women in quantum",
    ],
    "palavras_dominio_excluir_forte": [
        # Exclusoes "hard" — aplicadas ao titulo na Fase 1 e NAO sao revogadas
        # pela presenca de palavras de "dominio_manter" (supply chain, logistics, etc).
        # Motivo: artigos cujo TITULO evidencia claramente outra area de pesquisa
        # nao devem ser salvos apenas porque mencionam SC de passagem.
        "blockchain", "patent review", "patent analysis",
        "nanotechnology", "nanotech",
        "digital health", "biomedical",
        "quantum cryptography", "post-quantum cryptography",
        "satellite communication",
        "quantum communication", "quantum communications",
        "covid-19", "covid", "pandemic",
        "lng", "liquefied natural gas",
        "pharmacy", "central fill", "robotic dispensing",
        "semiconductor manufacturing",
        "ESG goals", "augmented reality",
        "women in quantum", "editorial",
        "export control",
        "vehicle break down", "vehicle breakdown",
        "level generation",
        "microservice", "microservices",
        "innovation ecosystem", "human-centric economy",
        "functional near-infrared", "fnirs",
        "wave-particle duality",
        "hamiltonian framework", "nonadiabatic dynamics",
        "weather", "forecasting the weather",
        "lifepo4", "lithium iron phosphate",
        "vaccine supply chain", "vaccine",
        "export controls",
        "non-trivial classification", "quantum kernel framework",
        "finance and supply chain",
        "shallow entangled circuits", "ibm devices",
    ],
    "palavras_dominio_manter": [
        "supply chain", "logistics", "inventory",
        "warehouse", "demand forecast", "backorder",
        "procurement", "freight", "distribution network",
        "supplier", "replenishment", "order fulfillment",
        "last mile", "transportation planning",
        "production planning", "manufacturing",
    ],
}

# CE-5: Tipos de publicacao nao-substantivos
CONFIG_CE5 = {
    "tipos_excluir": [
        "book chapter",
        "report",
        "book",
        "dissertation",
        "other",
        "NaN (sem tipo)",
        "dataset",
        "component",
        "journal issue",
        "editorial",
        "news",
        "conference proceedings",
    ],
}


# ============================================================
# FUNCOES UTILITARIAS — Matching por regex
# ============================================================

def _compilar_padroes(lista_palavras):
    """Compila lista de palavras-chave em padroes regex com word boundary."""
    padroes = []
    for palavra in lista_palavras:
        escaped = re.escape(palavra)
        padrao = re.compile(r"\b" + escaped + r"\b", re.IGNORECASE)
        padroes.append((palavra, padrao))
    return padroes


def _tem_match(texto, padroes):
    """Retorna True se qualquer padrao encontrar match no texto."""
    if not texto or pd.isna(texto):
        return False
    for _, padrao in padroes:
        if padrao.search(texto):
            return True
    return False


def _primeiro_match(texto, padroes):
    """Retorna a primeira palavra-chave que deu match, ou None."""
    if not texto or pd.isna(texto):
        return None
    for palavra, padrao in padroes:
        if padrao.search(texto):
            return palavra
    return None


# ============================================================
# PRE-COMPILACAO dos padroes (executado uma vez ao carregar)
# ============================================================

# CE-1
PADROES_OTIMIZACAO = _compilar_padroes(CONFIG_CE1["palavras_otimizacao"])
PADROES_ML = _compilar_padroes(CONFIG_CE1["palavras_ml"])

# CE-2
PADROES_FUTURO = _compilar_padroes(CONFIG_CE2["palavras_futuro"])
PADROES_EXPERIMENTO = _compilar_padroes(CONFIG_CE2["palavras_experimento"])

# CE-3
PADROES_DOMINIO_EXCLUIR = _compilar_padroes(CONFIG_CE3["palavras_dominio_excluir"])
PADROES_DOMINIO_EXCLUIR_FORTE = _compilar_padroes(CONFIG_CE3["palavras_dominio_excluir_forte"])
PADROES_DOMINIO_MANTER = _compilar_padroes(CONFIG_CE3["palavras_dominio_manter"])


# ============================================================
# FASE 1 — Triagem por metadados (titulo + tipo de publicacao + fields of study)
# ============================================================

def aplicar_fase1(df):
    """
    Aplica criterios de exclusao da Fase 1 (titulo + tipo de publicacao + fields of study).

    Criterios aplicados (em ordem de prioridade):
        CE-5: tipo de publicacao nao-substantivo
        CE-1: otimizacao quantica pura (sem ML) no titulo + fields of study
        CE-3: dominio fora de escopo no titulo + fields of study

    Adiciona colunas: fase1_decisao, motivo_exclusao
    """
    print("\n" + "=" * 60)
    print("  FASE 1 — Triagem por Metadados")
    print("  (titulo + tipo de publicacao + fields of study)")
    print("=" * 60)

    df["fase1_decisao"] = ""
    df["motivo_exclusao"] = ""

    tipos_excluir = [t.lower().strip() for t in CONFIG_CE5["tipos_excluir"]]

    for idx in df.index:
        titulo = str(df.at[idx, "Title"]).strip() if pd.notna(df.at[idx, "Title"]) else ""
        pub_type = str(df.at[idx, "Publication Type"]).strip().lower() if pd.notna(df.at[idx, "Publication Type"]) else ""
        fields = str(df.at[idx, "Fields of Study"]).strip() if pd.notna(df.at[idx, "Fields of Study"]) else ""

        # CE-5: tipo de publicacao
        if pub_type in tipos_excluir:
            df.at[idx, "fase1_decisao"] = "excluir"
            df.at[idx, "motivo_exclusao"] = "CE-5"
            continue

        # Texto combinado: titulo + fields of study
        texto = titulo + " " + fields

        # CE-1: otimizacao pura sem ML (no titulo + fields of study)
        if _tem_match(texto, PADROES_OTIMIZACAO) and not _tem_match(texto, PADROES_ML):
            df.at[idx, "fase1_decisao"] = "excluir"
            df.at[idx, "motivo_exclusao"] = "CE-1"
            continue

        # CE-3 FORTE: dominio claramente fora de escopo no TITULO.
        # Nao ha revogacao via palavras_dominio_manter — artigos cujo titulo
        # evidencia outro dominio de pesquisa (ex: blockchain, patent review,
        # nanotechnology) sao excluidos mesmo que mencionem "supply chain".
        if _tem_match(titulo, PADROES_DOMINIO_EXCLUIR_FORTE):
            df.at[idx, "fase1_decisao"] = "excluir"
            df.at[idx, "motivo_exclusao"] = "CE-3 (forte)"
            continue

        # CE-3: dominio fora de escopo (no titulo + fields of study)
        if _tem_match(texto, PADROES_DOMINIO_EXCLUIR) and not _tem_match(texto, PADROES_DOMINIO_MANTER):
            df.at[idx, "fase1_decisao"] = "excluir"
            df.at[idx, "motivo_exclusao"] = "CE-3"
            continue

        # Passou todos os filtros
        df.at[idx, "fase1_decisao"] = "incluir"

    return df


# ============================================================
# FASE 2 — Triagem por abstract (apenas abstract)
# ============================================================

def aplicar_fase2(df):
    """
    Aplica criterios de exclusao da Fase 2 (apenas abstract).

    Apenas para artigos com fase1_decisao == 'incluir'.
    Artigos excluidos na Fase 1 recebem fase2_decisao = 'nao_avaliado'.
    Artigos sem abstract passam automaticamente (abordagem conservadora).

    Criterios aplicados (em ordem de prioridade):
        CE-1: otimizacao quantica pura (sem ML) no abstract
        CE-2: QML apenas como trabalho futuro
        CE-3: dominio fora de escopo no abstract
    """
    print("\n" + "=" * 60)
    print("  FASE 2 — Triagem por Abstract")
    print("  (apenas abstract)")
    print("=" * 60)

    df["fase2_decisao"] = ""

    sem_abstract = 0
    sem_abstract_excluidos = 0

    for idx in df.index:
        # Artigos ja excluidos na Fase 1
        if df.at[idx, "fase1_decisao"] == "excluir":
            df.at[idx, "fase2_decisao"] = "nao_avaliado"
            continue

        abstract = str(df.at[idx, "Abstract"]).strip() if pd.notna(df.at[idx, "Abstract"]) else ""

        # Abstract vazio: incluir apenas se titulo tem keyword de supply chain
        if not abstract or abstract.lower() == "nan":
            titulo = str(df.at[idx, "Title"]).strip() if pd.notna(df.at[idx, "Title"]) else ""
            if _tem_match(titulo, PADROES_DOMINIO_MANTER):
                df.at[idx, "fase2_decisao"] = "incluir"
                sem_abstract += 1
            else:
                df.at[idx, "fase2_decisao"] = "excluir"
                df.at[idx, "motivo_exclusao"] = "CE-3"
                sem_abstract_excluidos += 1
            continue

        # CE-1: otimizacao pura sem ML (no abstract)
        if _tem_match(abstract, PADROES_OTIMIZACAO) and not _tem_match(abstract, PADROES_ML):
            df.at[idx, "fase2_decisao"] = "excluir"
            df.at[idx, "motivo_exclusao"] = "CE-1"
            continue

        # CE-2: QML apenas como trabalho futuro (no abstract)
        if _tem_match(abstract, PADROES_FUTURO) and not _tem_match(abstract, PADROES_EXPERIMENTO):
            df.at[idx, "fase2_decisao"] = "excluir"
            df.at[idx, "motivo_exclusao"] = "CE-2"
            continue

        # CE-3: dominio fora de escopo (no abstract)
        if _tem_match(abstract, PADROES_DOMINIO_EXCLUIR) and not _tem_match(abstract, PADROES_DOMINIO_MANTER):
            df.at[idx, "fase2_decisao"] = "excluir"
            df.at[idx, "motivo_exclusao"] = "CE-3"
            continue

        # Passou todos os filtros
        df.at[idx, "fase2_decisao"] = "incluir"

    if sem_abstract > 0 or sem_abstract_excluidos > 0:
        print(f"\n  [!] Artigos sem abstract:")
        print(f"      Incluidos (tem keyword SC no titulo): {sem_abstract}")
        print(f"      Excluidos (sem keyword SC no titulo): {sem_abstract_excluidos}")

    return df


# ============================================================
# ESTATISTICAS
# ============================================================

def imprimir_estatisticas_fase1(df):
    """Imprime estatisticas detalhadas da Fase 1."""
    total = len(df)
    incluidos = (df["fase1_decisao"] == "incluir").sum()
    excluidos = (df["fase1_decisao"] == "excluir").sum()

    print(f"\n  Resultado Fase 1:")
    print(f"  {'-' * 40}")
    print(f"  Total de artigos:     {total:>6,}")
    print(f"  Incluidos:            {incluidos:>6,} ({100*incluidos/total:.1f}%)")
    print(f"  Excluidos:            {excluidos:>6,} ({100*excluidos/total:.1f}%)")

    if excluidos > 0:
        print(f"\n  Detalhamento por criterio:")
        df_excl = df[df["fase1_decisao"] == "excluir"]
        for ce in ["CE-5", "CE-1", "CE-3"]:
            qtd = (df_excl["motivo_exclusao"] == ce).sum()
            if qtd > 0:
                print(f"    {ce}: {qtd:>4} artigos")
                # Top 5 exemplos
                exemplos = df_excl[df_excl["motivo_exclusao"] == ce]["Title"].head(5)
                for i, titulo in enumerate(exemplos, 1):
                    titulo_curto = str(titulo)[:80] + "..." if len(str(titulo)) > 80 else str(titulo)
                    print(f"         {i}. {titulo_curto}")


def imprimir_estatisticas_fase2(df):
    """Imprime estatisticas detalhadas da Fase 2."""
    df_fase2 = df[df["fase1_decisao"] == "incluir"]
    total_fase2 = len(df_fase2)
    incluidos = (df_fase2["fase2_decisao"] == "incluir").sum()
    excluidos = (df_fase2["fase2_decisao"] == "excluir").sum()

    print(f"\n  Resultado Fase 2:")
    print(f"  {'-' * 40}")
    print(f"  Entraram na Fase 2:   {total_fase2:>6,}")
    print(f"  Incluidos:            {incluidos:>6,} ({100*incluidos/total_fase2:.1f}%)")
    print(f"  Excluidos:            {excluidos:>6,} ({100*excluidos/total_fase2:.1f}%)")

    if excluidos > 0:
        print(f"\n  Detalhamento por criterio:")
        df_excl = df_fase2[df_fase2["fase2_decisao"] == "excluir"]
        for ce in ["CE-1", "CE-2", "CE-3"]:
            qtd = (df_excl["motivo_exclusao"] == ce).sum()
            if qtd > 0:
                print(f"    {ce}: {qtd:>4} artigos")
                exemplos = df_excl[df_excl["motivo_exclusao"] == ce]["Title"].head(5)
                for i, titulo in enumerate(exemplos, 1):
                    titulo_curto = str(titulo)[:80] + "..." if len(str(titulo)) > 80 else str(titulo)
                    print(f"         {i}. {titulo_curto}")


def imprimir_resumo_final(df):
    """Imprime resumo final no formato PRISMA."""
    total = len(df)
    excl_f1 = (df["fase1_decisao"] == "excluir").sum()
    incl_f1 = (df["fase1_decisao"] == "incluir").sum()

    df_fase2 = df[df["fase1_decisao"] == "incluir"]
    excl_f2 = (df_fase2["fase2_decisao"] == "excluir").sum()
    incl_f2 = (df_fase2["fase2_decisao"] == "incluir").sum()

    # Breakdown por criterio
    ce5 = (df["motivo_exclusao"] == "CE-5").sum()
    ce1_f1 = ((df["fase1_decisao"] == "excluir") & (df["motivo_exclusao"] == "CE-1")).sum()
    ce3_f1 = ((df["fase1_decisao"] == "excluir") & (df["motivo_exclusao"] == "CE-3")).sum()
    ce1_f2 = ((df["fase2_decisao"] == "excluir") & (df["motivo_exclusao"] == "CE-1")).sum()
    ce2_f2 = ((df["fase2_decisao"] == "excluir") & (df["motivo_exclusao"] == "CE-2")).sum()
    ce3_f2 = ((df["fase2_decisao"] == "excluir") & (df["motivo_exclusao"] == "CE-3")).sum()

    print("\n" + "=" * 60)
    print("  RESUMO FINAL — Fluxo PRISMA-ScR")
    print("=" * 60)
    print(f"\n  Identificacao:             {total:>6,} artigos")
    print(f"  {'-' * 50}")
    print(f"  Fase 1 — Excluidos:        {excl_f1:>6,}  (CE-5: {ce5}, CE-1: {ce1_f1}, CE-3: {ce3_f1})")
    print(f"  Fase 1 — Incluidos:        {incl_f1:>6,}")
    print(f"  {'-' * 50}")
    print(f"  Fase 2 — Excluidos:        {excl_f2:>6,}  (CE-1: {ce1_f2}, CE-2: {ce2_f2}, CE-3: {ce3_f2})")
    print(f"  Fase 2 — Incluidos:        {incl_f2:>6,}")
    print(f"  {'-' * 50}")
    print(f"  Elegiveis para revisao:    {incl_f2:>6,}  ({100*incl_f2/total:.1f}% do corpus)")


# ============================================================
# LIMPEZA DE DADOS
# ============================================================

def limpar_quebras_de_linha(df):
    """
    Remove quebras de linha (\n, \r) dentro dos campos de texto.

    Alguns registros exportados do Lens.org contem newlines internos em
    campos como Title, Source Title e Keywords. Isso causa linhas extras
    ao abrir o CSV em planilhas (Excel, LibreOffice).
    """
    colunas_corrigidas = {}
    for col in df.columns:
        mask = df[col].fillna("").str.contains(r"[\n\r]", regex=True)
        n = mask.sum()
        if n > 0:
            df[col] = df[col].fillna("").str.replace(r"\s*[\n\r]+\s*", " ", regex=True).str.strip()
            colunas_corrigidas[col] = n

    if colunas_corrigidas:
        total = sum(colunas_corrigidas.values())
        print(f"\n  [Limpeza] Quebras de linha removidas em {total} campos:")
        for col, n in colunas_corrigidas.items():
            print(f"    {col}: {n} registros corrigidos")
    else:
        print("\n  [Limpeza] Nenhuma quebra de linha encontrada.")

    return df


# ============================================================
# FUNCAO PRINCIPAL
# ============================================================

def main():
    """Funcao principal — orquestra as fases de triagem."""
    print("=" * 60)
    print("  TRIAGEM DE ARTIGOS — QML + Supply Chain/Inventory")
    print(f"  Executado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # --- Carregar dados ---
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"\n  [ERRO] Arquivo nao encontrado: {ARQUIVO_ENTRADA}")
        print("  Execute primeiro: python src/deduplicar_artigos.py")
        return

    print(f"\n  Carregando: {os.path.basename(ARQUIVO_ENTRADA)}")
    df = pd.read_csv(ARQUIVO_ENTRADA, dtype=str, encoding="utf-8-sig")
    print(f"  Artigos carregados: {len(df):,}")

    # --- Limpeza: remover quebras de linha internas nos campos ---
    df = limpar_quebras_de_linha(df)

    # Salvar CSV original corrigido (sem quebras de linha internas)
    df_original_cols = [c for c in df.columns if c not in ["fase1_decisao", "fase2_decisao", "motivo_exclusao"]]
    df[df_original_cols].to_csv(ARQUIVO_ENTRADA, index=False, encoding="utf-8-sig")
    print(f"  Arquivo original atualizado (quebras de linha corrigidas)")

    # --- Fase 1 ---
    df = aplicar_fase1(df)
    imprimir_estatisticas_fase1(df)

    # --- Fase 2 ---
    df = aplicar_fase2(df)
    imprimir_estatisticas_fase2(df)

    # --- Resumo final ---
    imprimir_resumo_final(df)

    # --- Exportar ---
    print(f"\n  Exportando: {os.path.basename(ARQUIVO_SAIDA)}")
    df.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")
    print(f"  Arquivo salvo com {len(df):,} artigos e {len(df.columns)} colunas")
    print(f"  Colunas adicionadas: fase1_decisao, fase2_decisao, motivo_exclusao")

    print("\n" + "=" * 60)
    print("  Triagem concluida com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
