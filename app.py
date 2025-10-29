# Fichier: app.py (Version Finale - PROPRE - GARANTIE v8 - Complète)
import os
import io
import base64
from typing import Dict, List
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# =========================
# Config de page
# =========================
st.set_page_config(
    # TITRE MIS À JOUR POUR LES RECRUTEURS
    page_title="Agent IA de Transformation Stratégique",
    page_icon="🚀",
    layout="wide"
)

# =========================
# I18N — Multilingue FR/EN
# =========================
# TEXTES MIS À JOUR POUR ÊTRE PLUS PERCUTANTS
LANGS = {
    "fr": {
        "app_title": "🚀 Agent IA de Transformation Stratégique",
        "app_sub": "Transformez n'importe quel référentiel de maturité en une feuille de route IA. Ciblez les priorités, générez le rapport et pilotez le changement.",
        "sidebar_title": "⚙️ Paramètres",
        "sidebar_lang": "Langue",
        "sidebar_excel": "Votre Référentiel (Excel)",
        "sidebar_ai_toggle": "Activer l'Agent IA (OpenAI)",
        "sidebar_model": "Modèle OpenAI",
        "sidebar_api": "OPENAI_API_KEY",
        "sidebar_hint": "L'IA est optionnelle. Sans clé, le rapport est généré par heuristique.",
        "questionnaire": "🧩 1. Auto-évaluation (16 domaines)",
        "level_label": "Niveau",
        "level_options": ["1", "2", "3", "4", "5"], # Pour st.radio
        "level_keys": ["level_1","level_2","level_3","level_4","level_5"],
        "chosen_level": "Niveau choisi",
        "kpi_global": "Score global",
        "kpi_domains": "Domaines évalués",
        "kpi_questions": "Points de contrôle",
        "kpi_weak": "Domaines prioritaires",
        "radar_title": "📊 2. Radar de Maturité",
        "prio_title": "🧭 3. Priorisation Stratégique (Score vs. Poids)",
        "bar_title": "Domaines à traiter en premier",
        "ai_mode_manual": "🔒 Mode manuel — activez l'IA (OpenAI) dans la barre latérale pour une analyse et une feuille de route de niveau consultant.",
        "summary_title": "📝 4. Rapport Exécutif & Feuille de Route",
        "download_report": "📥 Télécharger le Rapport (Markdown)",
        "post_title": "🔗 5. Post LinkedIn (Prêt à frapper)",
        # POST LINKEDIN REFAIT POUR ATTRIRER LES CDI
        "post_text": "J'arrête de voir des diagnostics de maturité Excel qui dorment dans un SharePoint.",
        "post_text_2": "J'ai donc buildé **MaturityAgent** (Streamlit) 🚀.",
        "post_text_3": "C'est un agent IA qui transforme n'importe quel framework (Data, IT, Cyber, ESG...) en un **atelier interactif**.",
        "post_text_4": "Le but ? Générer une **feuille de route IA** en < 1 heure, pas en 3 mois.",
        "post_bullets": [
            "• Mon benchmark (sur 16 domaines): Score global **{score:.1f}/100**",
            "• Domaines prioritaires (Quick Wins): **{top3}**"
        ],
        "post_footer": "Le code est open-source. Qui est prêt à challenger son référentiel ?\n#TransformationDigitale #IA #Consulting #Strategy #DataGovernance #Cybersecurity #Streamlit #CDI",
        "xls_template": "📦 Télécharger le modèle Excel",
        "xls_template_tip": "Feuille `questions` requise: domain, question, weight, level_1..level_5",
        "default_strengths": "Forces",
        "default_risks": "Risques/Priorités",
        "fallback_summary": "Synthèse — Score global **{score:.1f}/100**. {strengths}: {s_list}. {risks}: {r_list}.",
        "fallback_roadmap_title": "Feuille de route (heuristique sans IA)",
        "fallback_roadmap_90": "**90 jours (Quick Wins):**",
        "fallback_roadmap_6m": "**6 mois (Structuration):**",
        "fallback_roadmap_12m": "**12 mois (Scale):**",
        "quick_win_line": "- [{domain}] **Action prioritaire** sur “{question}” (Score actuel: {level}/5) — Viser le niveau 3."
    },
    "en": {
         "app_title": "🚀 Strategic Transformation AI Agent",
        "app_sub": "Turn any maturity framework into an AI-driven roadmap. Target priorities, generate reports, and drive change.",
        "sidebar_title": "⚙️ Settings",
        "sidebar_lang": "Language",
        "sidebar_excel": "Your Framework (Excel)",
        "sidebar_ai_toggle": "Enable AI Agent (OpenAI)",
        "sidebar_model": "OpenAI model",
        "sidebar_api": "OPENAI_API_KEY",
        "sidebar_hint": "AI is optional. Without a key, a heuristic report is generated.",
        "questionnaire": "🧩 1. Self-Assessment (16 Domains)",
        "level_label": "Level",
        "level_options": ["1", "2", "3", "4", "5"],
        "level_keys": ["level_1","level_2","level_3","level_4","level_5"],
        "chosen_level": "Selected level",
        "kpi_global": "Global Score",
        "kpi_domains": "Domains Assessed",
        "kpi_questions": "Control Points",
        "kpi_weak": "Priority Domains",
        "radar_title": "📊 2. Maturity Radar",
        "prio_title": "🧭 3. Strategic Prioritization (Score vs. Weight)",
        "bar_title": "Top Domains to Address",
        "ai_mode_manual": "🔒 Manual Mode — Enable AI (OpenAI) in the sidebar for a consultant-grade analysis and roadmap.",
        "summary_title": "📝 4. Executive Report & Roadmap",
        "download_report": "📥 Download Report (Markdown)",
        "post_title": "🔗 5. LinkedIn Post (Ready to Hit)",
        "post_text": "I'm tired of seeing Excel maturity diagnostics sleeping in a SharePoint.",
        "post_text_2": "So I built **MaturityAgent** (Streamlit) 🚀.",
        "post_text_3": "It's an AI agent that turns any framework (Data, IT, Cyber, ESG...) into an **interactive workshop**.",
        "post_text_4": "The goal? Generate an **AI-driven roadmap** in < 1 hour, not 3 months.",
        "post_bullets": [
            "• My benchmark (16 domains): Global Score **{score:.1f}/100**",
            "• Priority Domains (Quick Wins): **{top3}**"
        ],
        "post_footer": "The code is open-source. Who's ready to challenge their framework?\n#DigitalTransformation #AI #Consulting #Strategy #DataGovernance #Cybersecurity #Streamlit #Hiring",
        "xls_template": "📦 Download Excel Template",
        "xls_template_tip": "Sheet `questions` required: domain, question, weight, level_1..level_5",
        "default_strengths": "Strengths",
        "default_risks": "Risks/Priorities",
        "fallback_summary": "Summary — Global score **{score:.1f}/100**. {strengths}: {s_list}. {risks}: {r_list}.",
        "fallback_roadmap_title": "Roadmap (heuristic, no AI)",
        "fallback_roadmap_90": "**90 Days (Quick Wins):**",
        "fallback_roadmap_6m": "**6 Months (Foundation):**",
        "fallback_roadmap_12m": "**12 Months (Scale):**",
        "quick_win_line": "- [{domain}] **Priority action** on “{question}” (Current Score: {level}/5) — Target Level 3."
    }
}

# Lang selection (query param or sidebar)
# Utilisation de st.query_params qui est la méthode recommandée maintenant
q_params = st.query_params
# Utiliser .get pour récupérer la valeur, default à ["fr"] si non présent
lang_list = q_params.get("lang", ["fr"])
# S'assurer qu'il y a bien une valeur dans la liste
q_lang = lang_list[0] if lang_list else "fr"
cur_lang = "en" if q_lang.lower().startswith("en") else "fr"

with st.sidebar:
    st.header(LANGS[cur_lang]["sidebar_title"])
    # Utiliser on_change pour mettre à jour la langue immédiatement
    def update_lang():
        # Utiliser .set() qui est la méthode moderne pour les query params
        # Gérer le cas où query_params n'est pas directement modifiable (anciennes versions Streamlit?)
        try:
             st.query_params["lang"] = st.session_state.lang_select
        except AttributeError: # AttributError si query_params n'est pas modifiable
             st.experimental_set_query_params(lang=st.session_state.lang_select)


    selected_lang = st.selectbox(
        LANGS[cur_lang]["sidebar_lang"],
        ["fr","en"],
        index=(0 if cur_lang=="fr" else 1),
        key="lang_select",
        on_change=update_lang
    )
    # Assurer la cohérence si selectbox change la langue via interaction
    if 'lang_select' in st.session_state:
        cur_lang = st.session_state.lang_select


T = LANGS[cur_lang]

# =========================
# CSS "MAGNIFIQUE" (Dark Mode SaaS)
# =========================
st.markdown("""
<style>
/* Base */
body {
    color: #F8FAFC; /* Texte clair */
}
/* Titres */
.title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}
.sub {
    color: #CBD5E1; /* Gris clair */
    margin-bottom: 24px;
    font-size: 18px;
}
/* Cartes KPI - Look "Dashboard" */
.card {
    background-color: #1E293B; /* Slate 800 */
    border: 1px solid #334155; /* Slate 700 */
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    height: 100%; /* Pour aligner les cartes */
}
.kpi {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.1;
    color: #F8FAFC;
}
.kpi-sub {
    color: #94A3B8; /* Slate 400 */
    font-size: 14px;
    font-weight: 500;
}
/* Gradient pour le titre */
.gradient {
    background: linear-gradient(90deg, #A78BFA, #A78BFA); /* Violet 400 */
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
/* Amélioration des expanders */
.stExpander {
    background-color: #1E293B; /* Slate 800 */
    border: 1px solid #334155; /* Slate 700 */
    border-radius: 10px !important;
    margin-bottom: 12px; /* Espacement entre expanders */
}
.stExpander header {
    font-size: 16px;
    font-weight: 600;
    color: #F1F5F9; /* Slate 100 */
}
/* Style pour st.radio horizontal */
div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 10px; /* Espace entre les boutons radio */
}
/* Style des boutons radio */
div[role="radiogroup"] label {
    background-color: #334155; /* Slate 700 */
    border: 1px solid #475569; /* Slate 600 */
    padding: 8px 16px;
    border-radius: 8px;
    transition: all 0.2s ease;
    cursor: pointer; /* Indiquer que c'est cliquable */
    display: flex; /* Aligner le texte */
    align-items: center;
    margin-bottom: 0 !important; /* Override Streamlit margin */
}
div[role="radiogroup"] label:hover {
    background-color: #475569; /* Slate 600 */
}

/* Style pour l'option radio SÉLECTIONNÉE - PLUS VISIBLE */
/* Cibler le label parent quand le radio input est checké */
div[role="radiogroup"] label:has(input[type="radio"]:checked) {
     background-color: #6D28D9 !important; /* Violet plus foncé */
     border-color: #A78BFA !important; /* Bordure violet clair */
     color: #F8FAFC !important; /* Texte clair */
}

/* Style du texte à l'intérieur du label sélectionné */
div[role="radiogroup"] label:has(input[type="radio"]:checked) span {
     color: #F8FAFC !important;
     font-weight: bold;
}


/* Cacher le point radio par défaut */
div[role="radiogroup"] input[type="radio"] {
    opacity: 0;
    position: absolute;
    width: 0;
    height: 0;
}

/* Enlever la marge par défaut du widget radio global */
div[data-testid="stRadio"] > label {
    margin-bottom: 0px !important;
}
/* Ajuster l'espacement global du widget radio si nécessaire */
div[data-testid="stRadio"] {
    padding-bottom: 10px; /* Ajouter un peu d'espace en dessous */
}

</style>
""", unsafe_allow_html=True)


st.markdown(f"<div class='title gradient'>{T['app_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub'>{T['app_sub']}</div>", unsafe_allow_html=True)

# =========================
# Référentiel par défaut (VOTRE EXPERTISE)
# =========================
# Utilisation directe du DataFrame pour éviter des copies inutiles si possible
VOTRE_REFERENTIEL = pd.DataFrame([
    # === AXE 1 : Stratégie, Gouvernance, Organisation ===
    ["AXE 1 - Stratégie", "Politique & Stratégie", 1.0,
     "Cadre stratégique et politique data à définir",
     "Cadre stratégique data défini",
     "Politique de gouvernance & qualité définie",
     "Politique de gouvernance & qualité formalisée, divulguée et mise à jour",
     "Politique data auditée et alignée dynamiquement sur la stratégie groupe"],

    ["AXE 1 - Stratégie", "Gouvernance", 1.0,
     "Comités autour de la donnée à définir",
     "Comité ad hoc non structuré",
     "Comité mis en place au sein de chaque métier & fonction",
     "Comités transverses (Métier & IT) mis en place avec participation du top management",
     "Gouvernance data intégrée aux décisions stratégiques (ExCom)"],

    ["AXE 1 - Stratégie", "Organisation", 1.0,
     "Rôles et responsabilités à définir",
     "Data Owner & Data Steward identifiés",
     "Identification d'un CDO / DPO",
     "Mise en Place d'un Data Office structuré",
     "Data Office reconnu comme centre d'excellence transverse"],

    # === AXE 2 : Connaissance Data ===
    ["AXE 2 - Connaissance", "Identification des données", 1.0,
     "Catégorisation des données à effectuer, Golden sources à identifier",
     "Quelques données clés identifiées pour le suivi de l'activité",
     "Démarche d'identification des données prioritaires formalisée, catégorisation en cours",
     "Catégorisation établie, Golden sources identifiées, démarche revue périodiquement",
     "Inventaire des données 'data assets' 100% automatisé et outillé"],

    ["AXE 2 - Connaissance", "Catalogue & Lineage", 1.0,
     "Standards et référentiels data à définir",
     "Cadre standard de métadonnée mis en place",
     "Catalogue & dictionnaire formalisés, Lineage fonctionnel en place",
     "Catalogue partagé, gouverné et mis à jour, Lineages fonctionnel & technique en place",
     "Catalogue prédictif et 'data marketplace' active"],

    ["AXE 2 - Connaissance", "Données de références (MDM)", 1.0,
     "Réflexion en cours sur l'organisation de la gestion des données de références",
     "Existence de mapping (souvent Excel)",
     "Identification de golden sources, début d'automatisation",
     "Golden source et golden copy identifiées, gestion outillée, automatisée et gouvernée",
     "MDM global et 'multi-domaine' unifié"],

    # === AXE 3 : Qualité des données ===
    ["AXE 3 - Qualité", "Approche et démarches qualité", 1.0,
     "Approche et démarche qualité en cours de réflexion",
     "Critères de qualité définis, processus d'identification des anomalies défini",
     "Processus de gestion des anomalies (stockage, plans d'action, suivi remédiation) mis en place",
     "Organisation spécifique (Data Quality Manager, comités qualité) mise en place",
     "Qualité 'by design' intégrée dans tous les nouveaux projets"],

    ["AXE 3 - Qualité", "Contrôle qualité", 1.0,
     "Plan de contrôle qualité en cours d'élaboration",
     "Cadre de contrôle défini, plan de contrôle pour données prioritaires",
     "Contrôles de 1er niveau (collecte, traitement, restitution) documentés, semi-automatisés",
     "Contrôles qualité entièrement automatisés et outillés, plan de contrôle 2e niveau défini",
     "Contrôles prédictifs (IA) pour anticiper les non-qualités"],

    ["AXE 3 - Qualité", "Metrics (Mesure Gouv & Qualité)", 1.0,
     "Indicateurs spécifiques à définir",
     "Indicateurs de mesure de la qualité des données mis en place",
     "Indicateurs de suivi de la gouvernance de la qualité (reporting) définis et mis en place",
     "Plan d'amélioration continue (revue des seuils, outils temps réel) défini et mis en place",
     "Scoring de qualité exposé en temps réel via API à toute l'entreprise"],

    # === AXE 4 : Socle & Archi SI ===
    ["AXE 4 - Socle SI", "Sécurité", 1.0,
     "Réflexion en cours sur la gestion de la sécurité et des droits d'accès",
     "Niveau de protection et droits d'accès défini à minima pour les données prioritaires",
     "Politique de gestion des accès (IAM) définie, contraintes de localisation prises en compte",
     "Conformité alignée gouvernance globale, audits réguliers, plan de contrôle 2e niveau",
     "Sécurité 'Zero Trust' et contrôles de conformité 100% automatisés"],

    ["AXE 4 - Socle SI", "Architecture", 1.0,
     "Modélisation des données à initier",
     "Flux des données clés/références cartographiés, localisation effectuée",
     "Modélisation des données clés/références effectuée",
     "Gestion outillée et automatisée des données, cartographie globale effectuée",
     "Architecture 'data mesh' ou 'data fabric' active et scalable"],

    ["AXE 4 - Socle SI", "Outils & Solution", 1.0,
     "Identification des outils et solutions à prévoir",
     "Connecteurs, APIs mis en place pour faciliter l'accès aux données",
     "Ingestion temps réel possible, Data Lake mise en place",
     "Data Lab mis en place, contrôle automatisé du monitoring des models",
     "Plateforme MLOps/DataOps unifiée et 100% 'self-service'"],

    # === AXE 5 : Culture Data ===
    ["AXE 5 - Culture", "Culture Data", 1.0,
     "Peu d'initiative pour la promotion de la donnée",
     "Organisation d'activités ponctuelles d'initiation aux problématiques data",
     "Plan de formation formalisé et déployé, identification de référents métiers/IT",
     "Communautés data (Métiers & IT) mises en place, ateliers réguliers",
     "Culture 'data-driven' généralisée, la donnée est l'affaire de tous"],

    # === AXE 6 : Initiative & Valorisation ===
    ["AXE 6 - Valorisation", "Business Model", 1.0,
     "Réflexion à initier sur l'impact de la data sur le business model",
     "Mise en place d'une veille concurrentielle par les données",
     "Plateformisation des services mise en place",
     "Data as an Asset: composante stratégique dans la construction du business model",
     "Nouveaux 'business models' 100% basés sur la valorisation de la donnée (ex: Data as a Service)"],

    ["AXE 6 - Valorisation", "Usages des données", 1.0,
     "Identification de certains cas d'usage de valorisation data à initier",
     "Centralisation des différentes sources des données",
     "Modèle prédictif mis en place pour les métiers clés",
     "Data Driven: solutions et décisions appuyées par les données",
     "Optimisation et simulation (jumeau numérique) basées sur l'IA"],

    ["AXE 6 - Valorisation", "Initiatives", 1.0,
     "Plan d'action à initier pour la promotion de la donnée",
     "Désilotage des données à travers les métiers et fonctions",
     "Communauté data mis en place",
     "Data Insight: organisation centrée sur la donnée avec des assets partagés",
     "Innovation data 'bottom-up' encouragée et financée (ex: hackathons)"]
], columns=["domain", "question", "weight", "level_1", "level_2", "level_3", "level_4", "level_5"])

DEFAULT_QUESTIONS = VOTRE_REFERENTIEL # Pas besoin de .copy() ici si on ne le modifie pas

LEVEL_MAP = { "level_1": 1, "level_2": 2, "level_3": 3, "level_4": 4, "level_5": 5 }

# =========================
# Sidebar (fichiers & IA)
# =========================
with st.sidebar:
    excel = st.file_uploader(T["sidebar_excel"], type=["xlsx"])
    use_ai = st.toggle(T["sidebar_ai_toggle"], value=False, help="Nécessite une clé API OpenAI valide")
    model_name = st.text_input(T["sidebar_model"], value="gpt-4o-mini", help="Modèle à utiliser pour l'analyse IA")
    api_key = st.text_input(T["sidebar_api"], type="password", value=os.getenv("OPENAI_API_KEY",""), help="Votre clé API OpenAI (gardée secrète)")
    st.caption(T["sidebar_hint"])

# Bouton pour télécharger un modèle Excel
@st.cache_data # Mise en cache pour éviter recalcul inutile
def get_template_bytes() -> bytes:
    buf = io.BytesIO()
    # Utiliser VOTRE_REFERENTIEL directement
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        VOTRE_REFERENTIEL.to_excel(writer, sheet_name="questions", index=False)
    buf.seek(0) # Revenir au début du buffer
    return buf.getvalue()

with st.sidebar:
    st.markdown("---") # Séparateur visuel
    st.markdown(T["xls_template_tip"])
    st.download_button(
        label=T["xls_template"],
        data=get_template_bytes(),
        file_name="maturity_questions_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" # Mime type correct pour xlsx
    )

# =========================
# Chargement du référentiel
# =========================
# @st.cache_data # Mise en cache potentielle si le fichier uploadé ne change pas souvent
def load_questions(uploaded_file):
    if uploaded_file is None:
        return DEFAULT_QUESTIONS
    try:
        # Lire directement depuis l'objet uploadé
        df = pd.read_excel(uploaded_file, sheet_name="questions")
        # Vérification plus robuste des colonnes requises
        required_cols = {"domain", "question", "weight"}
        level_cols = set(T["level_keys"])
        if not required_cols.issubset(df.columns):
            st.error(f"Fichier Excel invalide. Colonnes requises manquantes: {required_cols - set(df.columns)}")
            return DEFAULT_QUESTIONS.copy() # Retourner une copie pour éviter modif accidentelle
        # Ajouter les colonnes de niveau manquantes avec des chaînes vides
        for col in level_cols:
            if col not in df.columns:
                df[col] = ""
        # Nettoyer les types si nécessaire (optionnel mais recommandé)
        # Assurer que weight est numérique, fallback à 1.0 si erreur/manquant
        df['weight'] = pd.to_numeric(df['weight'], errors='coerce').fillna(1.0)
        df['domain'] = df['domain'].astype(str).fillna("Domaine Manquant").str.strip() # Remplacer NaN et strip
        df['question'] = df['question'].astype(str).fillna("Question Manquante").str.strip() # Remplacer NaN et strip
        # Supprimer les lignes où domain ou question sont réellement vides après nettoyage
        df = df[df['domain'] != ""]
        df = df[df['question'] != ""]
        df = df[df['domain'] != "Domaine Manquant"]
        df = df[df['question'] != "Question Manquante"]
        # Assurer que les poids sont valides (non-NaN après conversion)
        df['weight_numeric'] = pd.to_numeric(df['weight'], errors='coerce')
        df = df[df['weight_numeric'].notna()]
        df = df.drop(columns=['weight_numeric']) # Supprimer colonne temporaire

        if df.empty:
            st.warning("Le fichier Excel ne contient aucune question valide après nettoyage.")
            return DEFAULT_QUESTIONS.copy()

        return df
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier Excel: {e}")
        return DEFAULT_QUESTIONS.copy() # Retourner une copie

# Chargement conditionnel basé sur l'upload
Q = load_questions(excel)

# =========================
# Questionnaire (UX AMÉLIORÉE AVEC st.radio)
# =========================
st.markdown(f"### {T['questionnaire']}")
# Utiliser les domaines du DataFrame chargé (Q), pas DEFAULT_QUESTIONS
# Filtrer les domaines vides ou NaN potentiels
valid_domains = [d for d in Q["domain"].unique() if pd.notna(d) and str(d).strip()]
domains = sorted(valid_domains)
answers = {} # Utiliser un dictionnaire pour stocker les réponses par clé unique

# Initialiser les réponses dans session_state si elles n'existent pas
for d in domains:
    block = Q[Q["domain"]==d]
    for i, row in block.iterrows():
         # Utiliser l'index pandas original comme partie de la clé
        row_idx = i # Utiliser directement l'index pandas
        state_key = f"choice_{d}_{row_idx}"
        if state_key not in st.session_state:
            st.session_state[state_key] = T["level_options"][0] # Default to "1"


# Afficher le questionnaire
if not domains:
     st.warning("Aucun domaine valide trouvé dans le référentiel chargé.")
else:
    for d in domains:
        st.markdown(f"#### **{d}**")
        block = Q[Q["domain"]==d] # Pas besoin de reset_index si on utilise l'index original

        for i, row in block.iterrows():
            # Vérification si la question est valide
            question_text = row.get("question")
            if pd.isna(question_text) or not str(question_text).strip():
                continue # Ignorer silencieusement

            row_idx = i
            state_key = f"choice_{d}_{row_idx}"

            with st.expander(f"{question_text}"):
                # Récupérer la valeur actuelle de session_state pour le radio
                current_value = st.session_state.get(state_key, T["level_options"][0])
                if current_value not in T["level_options"]:
                    current_value = T["level_options"][0] # Reset si invalide
                    st.session_state[state_key] = current_value
                # Trouver l'index correspondant à la valeur actuelle
                try:
                    current_value_index = T["level_options"].index(current_value)
                except ValueError:
                    current_value_index = 0 # Fallback au premier élément si non trouvé
                    st.session_state[state_key] = T["level_options"][0]


                chosen_label = st.radio(
                    label=f"Niveau pour: {question_text}", # Label unique pour accessibilité
                    options=T["level_options"],
                    key=state_key, # Utilisation de la clé unique
                    index=current_value_index, # Assurer que l'index correspond à la valeur
                    horizontal=True,
                    label_visibility="collapsed"
                )

                # Mapping et affichage description
                chosen_key = f"level_{chosen_label}"
                level_num = int(chosen_label)
                desc = row.get(chosen_key, "Description non disponible") # Fallback pour description manquante

                st.caption(f"{T['chosen_level']}: **{chosen_label}/5** — {desc}")

                # Stocker la réponse dans le dictionnaire 'answers'
                weight_val = 1.0 # Default weight
                try:
                    weight_input = pd.to_numeric(row["weight"], errors='coerce')
                    if pd.notna(weight_input) and np.isfinite(weight_input):
                        weight_val = float(weight_input)
                except Exception:
                     weight_val = 1.0

                answers[state_key] = {
                    "domain": d,
                    "question": question_text,
                    "weight": weight_val,
                    "level": level_num
                }

# Vérifier s'il y a des réponses avant de continuer
if not answers:
    # Afficher le message seulement si des domaines existent
    if domains:
        st.info("Veuillez répondre à au moins une question pour générer le rapport.")
    # Si aucun domaine n'existe (fichier vide/invalide), l'avertissement précédent suffit
    st.stop()

# Créer le DataFrame de réponses à partir du dictionnaire
A = pd.DataFrame(list(answers.values()))

# =========================
# Scoring
# =========================
def score_domain(df_group):
    df_group = df_group.copy()
    df_group['level'] = pd.to_numeric(df_group['level'], errors='coerce')
    df_group['weight'] = pd.to_numeric(df_group['weight'], errors='coerce').fillna(1.0).clip(lower=0)
    df_group = df_group.dropna(subset=['level'])

    if df_group.empty:
        return np.nan

    x = df_group.assign(norm=(df_group["level"] - 1) / 4.0)
    w = x["weight"]
    w_sum = w.sum()

    if w_sum <= 0:
        if not x["norm"].empty:
             return float(100 * x["norm"].mean())
        else:
             return np.nan

    try:
        weighted_score = np.average(x["norm"], weights=w)
        return float(100 * weighted_score)
    except ZeroDivisionError:
         return 0.0


# Calcul des scores
domain_scores = {}
global_score = np.nan
calculated_scores = []

try:
    if not A.empty:
        # Appliquer score_domain seulement si A n'est pas vide
        grouped = A.groupby("domain")
        for name, group in grouped:
            if not group.empty:
                score = score_domain(group)
                domain_scores[name] = score
                if pd.notna(score):
                    calculated_scores.append(score)

        if calculated_scores:
            global_score = float(np.mean(calculated_scores))
        else:
            if not A.empty:
                 st.warning("Aucun score de domaine calculable. Vérifiez les poids/niveaux.")

except Exception as e:
    st.error(f"Erreur majeure lors du calcul des scores: {e}.")
    import traceback
    st.error(traceback.format_exc())
    domain_scores = {d: np.nan for d in domains}
    global_score = np.nan


st.divider()
# Affichage des KPIs
kpi_global_display = f"{global_score:.1f}" if pd.notna(global_score) else "N/A"
kpi_domains_count = len(domains) # Nombre total de domaines du référentiel
kpi_questions_count = len(A) # Nombre de réponses valides
weak_domains = [d for d, s in domain_scores.items() if pd.notna(s) and s < 60]
kpi_weak_count = len(weak_domains)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='card'><div class='kpi'>{kpi_global_display}</div><div class='kpi-sub'>{T['kpi_global']}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='card'><div class='kpi'>{kpi_domains_count}</div><div class='kpi-sub'>{T['kpi_domains']}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='card'><div class='kpi'>{kpi_questions_count}</div><div class='kpi-sub'>{T['kpi_questions']}</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='card'><div class='kpi'>{kpi_weak_count}</div><div class='kpi-sub'>{T['kpi_weak']}</div></div>", unsafe_allow_html=True)

# =========================
# Viz — Radar & Priorisation (Adapté au Dark Mode)
# =========================
st.markdown(f"### {T['radar_title']}")
fig_radar = go.Figure()

# Domaines valides pour le radar (scores non-NaN, ordre alphabétique de `domains`)
valid_radar_data = {d: domain_scores.get(d) for d in domains if pd.notna(domain_scores.get(d))}

if valid_radar_data:
    radar_domains = list(valid_radar_data.keys())
    r_vals = list(valid_radar_data.values())

    if r_vals:
        theta_vals = radar_domains
        # Boucler seulement si > 1 point
        if len(r_vals) > 1:
            r_vals.append(r_vals[0])
            theta_vals.append(theta_vals[0])
        elif len(r_vals) == 1: # Si 1 seul point, dupliquer pour ligne visible
             r_vals = [0, r_vals[0]]
             theta_vals = [theta_vals[0], theta_vals[0]]


        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals,
            theta=theta_vals,
            fill='toself' if len(theta_vals) > 2 else 'none', # Remplir si polygone (>2 pts)
            fillcolor='rgba(167, 139, 250, 0.3)',
            line=dict(color='#A78BFA', width=3)
        ))
    else:
         st.warning("Aucun score numérique valide trouvé pour construire le radar.")

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#94A3B8", gridcolor="#334155"),
            angularaxis=dict(color="#F8FAFC", gridcolor="#334155", tickfont=dict(size=12))
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    if r_vals: # Afficher seulement si trace ajoutée
        st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.warning("Aucun score de domaine valide à afficher dans le radar.")


# --- Priorisation ---
# Nettoyer Q avant groupby
Q['weight'] = pd.to_numeric(Q['weight'], errors='coerce').fillna(1.0).clip(lower=0)
weights_by_domain = Q.groupby("domain")["weight"].sum().to_dict()

prio_list = []
# Itérer sur les domaines avec score valide
for d in valid_radar_data.keys(): # Utiliser clés de valid_radar_data
    score = valid_radar_data[d]
    weight = float(weights_by_domain.get(d, 1.0))
    if pd.isna(weight) or weight <= 0: weight = 1.0

    prio_list.append({
        "domain": d,
        "score": score,
        "weight_total": weight,
        "priority_index": float((100 - score) * weight)
    })

if prio_list:
    prio_df = pd.DataFrame(prio_list).sort_values("priority_index", ascending=False).reset_index(drop=True)
else:
    prio_df = pd.DataFrame(columns=["domain", "score", "weight_total", "priority_index"])

st.markdown(f"### {T['prio_title']}")
st.dataframe(prio_df.style.format({"score": "{:.1f}", "weight_total": "{:.2f}", "priority_index": "{:.1f}"}), use_container_width=True)

# --- Bar Chart de Priorisation ---
if not prio_df.empty:
    try:
        # S'assurer que les données sont valides
        df_chart = prio_df.dropna(subset=['domain', 'priority_index', 'score'])
        if not df_chart.empty:
            fig_bar = px.bar(
                df_chart,
                x="domain",
                y="priority_index",
                color="score",
                title=T["bar_title"],
                text=df_chart["score"].round(1),
                color_continuous_scale=px.colors.sequential.Viridis_r,
                labels={"priority_index": "Indice de Priorité", "domain": "Domaine", "score": "Score"}
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="#F8FAFC",
                yaxis=dict(gridcolor="#334155", title="Indice de Priorité"),
                xaxis=dict(gridcolor="#334155", title="Domaine"),
                coloraxis_colorbar=dict(title="Score")
            )
            fig_bar.update_xaxes(categoryorder='array', categoryarray=df_chart['domain'])
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Données invalides pour graphique priorisation après nettoyage.")

    except Exception as e:
        st.error(f"Erreur création graphique barres: {e}")

else:
     st.warning("Impossible de générer le graphique de priorisation (pas de données valides).")


# =========================
# Heuristique d’actions (sans IA) - Robuste
# =========================
@st.cache_data # Mise en cache possible
def generate_heuristic_actions(_df_q: pd.DataFrame, _df_a: pd.DataFrame, _df_prio: pd.DataFrame, lang_code: str) -> str:
    if _df_a.empty or _df_q.empty or _df_prio.empty:
        return "- Aucun quick win identifiable (données manquantes) -"
    out = []
    try:
        required_q_cols = {"domain", "question", "weight"}
        required_a_cols = {"domain", "question", "level"}
        if not required_q_cols.issubset(_df_q.columns) or not required_a_cols.issubset(_df_a.columns):
            missing_q = required_q_cols - set(_df_q.columns); missing_a = required_a_cols - set(_df_a.columns)
            return f"- Colonnes manquantes (Q: {missing_q}, A: {missing_a}) -"

        df_q_clean = _df_q.copy(); df_q_clean['weight'] = pd.to_numeric(df_q_clean['weight'], errors='coerce').fillna(1.0).clip(lower=0)
        q_subset = df_q_clean[["domain", "question", "weight"]].drop_duplicates(subset=["domain", "question"])
        df_a_clean = _df_a.copy(); df_a_clean['level'] = pd.to_numeric(df_a_clean['level'], errors='coerce')
        df_a_clean = df_a_clean.dropna(subset=['level']); df_a_clean['level'] = df_a_clean['level'].astype(int)

        merged = df_a_clean.merge(q_subset, on=["domain", "question"], how="left"); merged['weight'] = merged['weight'].fillna(1.0)
        prio_domains_order = _df_prio["domain"].tolist(); domain_order_map = {domain: i for i, domain in enumerate(prio_domains_order)}
        merged = merged[merged['domain'].isin(domain_order_map)]
        if merged.empty: return "- Aucun domaine prioritaire trouvé dans les réponses -"
        merged['prio_sort_order'] = merged['domain'].map(domain_order_map)

        low_level_actions = merged[merged["level"] <= 2]
        if low_level_actions.empty: return "- Aucun point critique (niveau 1 ou 2) identifié -"

        wins = low_level_actions.sort_values(by=['prio_sort_order', 'level', 'weight'], ascending=[True, True, False]).head(5)
        line_template = LANGS[lang_code]["quick_win_line"]
        for _, r in wins.iterrows():
            try:
                out.append(line_template.format(domain=r.get("domain", "N/A"), question=r.get("question", "N/A"), level=int(r.get("level", 0))))
            except Exception as fmt_e: st.warning(f"Erreur formatage quick win: {fmt_e} - Ligne: {r.to_dict()}")
        return "\n".join(out) if out else "- Aucun quick win applicable trouvé -"
    except Exception as e:
        st.error(f"Erreur technique (generate_heuristic_actions): {e}"); import traceback; st.error(traceback.format_exc())
        return "- Erreur technique identification quick wins -"

# Appel
quick_wins = generate_heuristic_actions(Q, A, prio_df, cur_lang)


# =========================
# IA (optionnelle) - Gestion Erreurs Améliorée
# =========================
# @st.cache_data # Cache délicat
def ai_summary_openai(api_key_param: str, model_param: str, prompt_param: str) -> str:
    if not api_key_param: return "(CLÉ API MANQUANTE)"
    try:
        from openai import OpenAI, AuthenticationError, RateLimitError, NotFoundError, APIError, BadRequestError
        client = OpenAI(api_key=api_key_param)
        resp = client.chat.completions.create(model=model_param, messages=[{"role": "system", "content": "You are a world-class strategic consultant... Use Markdown heavily."}, {"role": "user", "content": prompt_param}], temperature=0.6, max_tokens=1500)
        choice = resp.choices[0]
        if choice.message and choice.message.content: return choice.message.content.strip()
        else: st.warning("Agent IA: Réponse vide."); return "(RÉPONSE IA VIDE)"
    except ImportError: st.error("pip install openai"); return "(ERREUR TECHNIQUE: OpenAI non installé)"
    except AuthenticationError: st.error("Erreur Auth OpenAI: Vérifiez clé API."); return "(ERREUR AUTHENTIFICATION)"
    except RateLimitError: st.warning("Erreur OpenAI: Quota atteint."); return "(ERREUR QUOTA)"
    except NotFoundError: st.error(f"Erreur OpenAI: Modèle '{model_param}' introuvable."); return f"(ERREUR MODÈLE '{model_param}' INTROUVABLE)"
    except BadRequestError as e: st.error(f"Erreur OpenAI (Bad Request): {e}"); return "(ERREUR REQUÊTE IA)"
    except APIError as e: st.error(f"Erreur API OpenAI: {e}"); return f"(ERREUR API OPENAI: {e})"
    except Exception as e: st.error(f"Erreur inattendue (Agent IA): {e}"); import traceback; st.error(traceback.format_exc()); return f"(ERREUR INATTENDUE AGENT IA)"

# Affichage conditionnel
if not use_ai: st.info(T["ai_mode_manual"])
elif not api_key and use_ai: st.warning("Agent IA activé, mais clé API manquante.")

# --- Préparation Contexte ---
valid_scores_dict = {k: f"{v:.1f}" for k, v in domain_scores.items() if pd.notna(v)}
domain_scores_str = str(valid_scores_dict) if valid_scores_dict else "N/A"
prio_order_str = ', '.join(prio_df['domain'].tolist()) if not prio_df.empty else "N/A"
global_score_str = f"{global_score:.1f}/100" if pd.notna(global_score) else "N/A"
quick_wins_context = quick_wins if not quick_wins.startswith("-") else "Aucun quick win critique identifié."

base_context = f"""
INFORMATIONS CLÉS DU DIAGNOSTIC:
- Score Global Actuel: {global_score_str}
- Scores par Domaine: {domain_scores_str}
- Domaines Prioritaires (ordre décroissant d'urgence): {prio_order_str}
- Actions Quick Wins suggérées (basées sur score <= 2):
{quick_wins_context}"""

summary_text_ai = None
roadmap_text_ai = None

# --- Appel IA ---
if use_ai and api_key:
    # Définition dynamique des prompts
    sum_prompt_template = LANGS[cur_lang].get("prompt_sum_template", """Rédige une **Synthèse Exécutive** (Markdown): 3 Forces Clés, 3 Risques Majeurs. Langue={lang}. {base_context}""") # Fallback simple
    map_prompt_template = LANGS[cur_lang].get("prompt_map_template", """Rédige une **Feuille de Route** (Markdown): Plan 90j (3 actions), 6m (3 actions), 12m (2 actions). Actions SMART. Langue={lang}. {base_context}""") # Fallback simple

    # Vérifier si les templates existent réellement dans LANGS (pour éviter KeyError)
    if "prompt_sum_template" not in LANGS[cur_lang]:
         # Utiliser le prompt générique si le template spécifique manque
         if cur_lang == "fr":
             sum_prompt_template = """Rédige une **Synthèse Exécutive** percutante (format Markdown) pour un Comité de Direction:\n- Rappelle brièvement le score global.\n- Liste **3 Forces Clés** (domaines avec les meilleurs scores, si disponibles).\n- Liste **3 Risques Majeurs / Points Faibles** (domaines prioritaires avec les scores les plus bas, si disponibles).\nUtilise des listes à puces. Sois direct et orienté décision. Ne mentionne pas "selon le contexte fourni".\n{base_context}"""
         else:
             sum_prompt_template = """Write a concise **Executive Summary** (Markdown format) for a Board meeting:\n- Briefly mention the overall score.\n- List **3 Key Strengths** (domains with the highest scores, if available).\n- List **3 Major Risks / Weaknesses** (priority domains with the lowest scores, if available).\nUse bullet points. Be direct and decision-oriented. Do not mention "based on the provided context".\n{base_context}"""

    if "prompt_map_template" not in LANGS[cur_lang]:
         if cur_lang == "fr":
            map_prompt_template = """Rédige une **Feuille de Route Stratégique** détaillée (format Markdown) pour adresser ce diagnostic:\n### Plan d'Action - 90 Jours (Quick Wins)\n* Action 1: [Objectif SMART] - [Livrable concret] - [Impact: Faible/Moyen/Élevé]\n* Action 2: ... (total 3 actions ciblant les domaines **les plus prioritaires** listés)\n* Action 3: ...\n### Plan d'Action - 6 Mois (Structuration)\n* Action 1: [Objectif SMART] - [Livrable concret] - [Impact: Faible/Moyen/Élevé]\n* Action 2: ... (total 3 actions pour bâtir les fondations)\n* Action 3: ...\n### Plan d'Action - 12 Mois (Transformation & Scale)\n* Action 1: [Objectif SMART] - [Livrable concret] - [Impact: Faible/Moyen/Élevé]\n* Action 2: ... (total 2 actions visant l'excellence)\n**Instructions:** Inspire-toi des Quick Wins mais propose des actions SMART complètes. Rends chaque plan actionnable.\n{base_context}"""
         else:
            map_prompt_template = """Write a detailed **Strategic Roadmap** (Markdown format):\n### 90-Day Action Plan (Quick Wins)\n* Action 1: [SMART Objective] - [Concrete Deliverable] - [Impact: Low/Med/High]\n* Action 2: ... (total 3 actions targeting top priority domains)\n* Action 3: ...\n### 6-Month Action Plan (Foundation)\n* Action 1: [SMART Objective] - [Concrete Deliverable] - [Impact: Low/Med/High]\n* Action 2: ... (total 3 actions for foundations)\n* Action 3: ...\n### 12-Month Action Plan (Transformation & Scale)\n* Action 1: [SMART Objective] - [Concrete Deliverable] - [Impact: Low/Med/High]\n* Action 2: ... (total 2 actions for excellence)\n**Instructions:** Use Quick Wins for inspiration but propose full SMART actions. Make it actionable.\n{base_context}"""


    sum_prompt = sum_prompt_template.format(base_context=base_context, lang=cur_lang)
    map_prompt = map_prompt_template.format(base_context=base_context, lang=cur_lang)

    # Exécution appels IA
    with st.spinner(f"🚀 Agent IA ({model_name}) analyse..."):
        summary_text_ai = ai_summary_openai(api_key, model_name, sum_prompt)

    if summary_text_ai and not summary_text_ai.startswith("("):
        with st.spinner(f"🧭 Agent IA ({model_name}) élabore la roadmap..."):
            roadmap_text_ai = ai_summary_openai(api_key, model_name, map_prompt)
        if roadmap_text_ai and roadmap_text_ai.startswith("("):
             st.warning(f"Génération IA échouée (roadmap): {roadmap_text_ai}")
    elif summary_text_ai: # Erreur synthèse
         st.warning(f"Génération IA échouée (synthèse): {summary_text_ai}. Roadmap non générée.")


# =========================
# Rapport Markdown + DL
# =========================
st.markdown(f"### {T['summary_title']}")

# --- Sélection texte final ---
fallback_score_str = f"{global_score:.1f}" if pd.notna(global_score) else "N/A"
valid_scores_dict_report = {d: s for d, s in domain_scores.items() if pd.notna(s)}
strengths_list = ", ".join([d for d, s in valid_scores_dict_report.items() if s >= 70]) or "N/A"
risks_list = ", ".join([d for d, s in valid_scores_dict_report.items() if s < 60]) or "N/A"

# Utiliser texte IA si valide, sinon fallback
final_summary = summary_text_ai if summary_text_ai and not summary_text_ai.startswith("(") else T["fallback_summary"].format(
    score=fallback_score_str, strengths=T["default_strengths"], risks=T["default_risks"], s_list=strengths_list, r_list=risks_list
)
final_roadmap = roadmap_text_ai if roadmap_text_ai and not roadmap_text_ai.startswith("(") else f"""**{T['fallback_roadmap_title']}**

{T['fallback_roadmap_90']}
{quick_wins}

{T['fallback_roadmap_6m']}
- Standardiser processus (2 domaines faibles).
- KPIs mensuels.
- Outillage (catalogue, qualité) sur périmètre prioritaire.

{T['fallback_roadmap_12m']}
- Automatiser gouvernance.
- Audits / certifications.
"""

# --- Formatage Rapport ---
scores_str_md = pd.Series(valid_scores_dict_report).round(1).to_string() if valid_scores_dict_report else 'N/A'
prio_str_md = prio_df[['domain','priority_index','score']].round(1).to_string(index=False) if not prio_df.empty else 'N/A'

report_md = f"""# 🚀 Rapport de Transformation Stratégique

**Score Global de Maturité:** {fallback_score_str}/100

---

## 📊 Scores par Domaine

```
{scores_str_md}
```

## 🧭 Analyse de Priorisation (Indice = (100-Score) * Poids Total)

```
{prio_str_md}

