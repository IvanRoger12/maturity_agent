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
        # ... (Gardez les traductions EN si vous le souhaitez, je me concentre sur le FR pour l'impact)
        # ... (Vous pouvez traduire la nouvelle version FR si besoin)
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
q_lang = st.query_params.get("lang", ["fr"])[0]
cur_lang = "en" if q_lang.lower().startswith("en") else "fr"

with st.sidebar:
    st.header(LANGS[cur_lang]["sidebar_title"])
    cur_lang = st.selectbox(LANGS[cur_lang]["sidebar_lang"], ["fr","en"], index=(0 if cur_lang=="fr" else 1))
st.query_params["lang"] = cur_lang  # keep in URL

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
}
div[role="radiogroup"] > label {
    background-color: #334155; /* Slate 700 */
    border: 1px solid #475569; /* Slate 600 */
    padding: 8px 16px;
    border-radius: 8px;
    margin-right: 10px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}
div[role="radiogroup"] > label:hover {
    background-color: #475569; /* Slate 600 */
}
/* Style pour l'option radio sélectionnée */
div[role="radiogroup"] label[data-baseweb="radio"] [aria-checked="true"] + div {
    background-color: #A78BFA !important; /* Violet 400 */
    border-color: #A78BFA !important;
    color: #0F172A !important; /* Texte foncé pour contraste */
    font-weight: 700;
}
div[role="radiogroup"] label[data-baseweb="radio"] [aria-checked="true"] + div:hover {
    background-color: #C4B5FD !important; /* Violet 300 */
}

/* Cacher le point radio moche */
div[role="radiogroup"] input[type="radio"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)


st.markdown(f"<div class='title gradient'>{T['app_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub'>{T['app_sub']}</div>", unsafe_allow_html=True)

# =========================
# Référentiel par défaut (VOTRE EXPERTISE)
# =========================
# (Ceci est votre référentiel, déjà intégré. Parfait.)
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

DEFAULT_QUESTIONS = VOTRE_REFERENTIEL.copy()

LEVEL_MAP = { "level_1": 1, "level_2": 2, "level_3": 3, "level_4": 4, "level_5": 5 }

# =========================
# Sidebar (fichiers & IA)
# =========================
with st.sidebar:
    excel = st.file_uploader(T["sidebar_excel"], type=["xlsx"])
    use_ai = st.toggle(T["sidebar_ai_toggle"], value=False)
    model_name = st.text_input(T["sidebar_model"], value="gpt-4o-mini")
    api_key = st.text_input(T["sidebar_api"], type="password", value=os.getenv("OPENAI_API_KEY",""))
    st.caption(T["sidebar_hint"])

# Bouton pour télécharger un modèle Excel
def xls_template_bytes() -> bytes:
    buf = io.BytesIO()
    df = VOTRE_REFERENTIEL.copy()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="questions", index=False)
    return buf.getvalue()

with st.sidebar:
    st.markdown(T["xls_template_tip"])
    st.download_button(T["xls_template"], data=xls_template_bytes(), file_name="maturity_questions_template.xlsx")

# =========================
# Chargement du référentiel
# =========================
def load_questions(uploaded):
    try:
        df = pd.read_excel(uploaded, sheet_name="questions")
        req = {"domain","question","weight"}
        if not req.issubset(df.columns):
            return DEFAULT_QUESTIONS.copy()
        for c in T["level_keys"]:
            if c not in df.columns:
                df[c] = ""
        return df
    except Exception:
        return DEFAULT_QUESTIONS.copy()

Q = load_questions(excel) if excel else DEFAULT_QUESTIONS.copy()

# =========================
# Questionnaire (UX AMÉLIORÉE AVEC st.radio)
# =========================
st.markdown(f"### {T['questionnaire']}")
domains = sorted(Q["domain"].unique())
answers = []

for d in domains:
    st.markdown(f"#### **{d}**")
    block = Q[Q["domain"]==d].reset_index(drop=True)
    for i, row in block.iterrows():
        with st.expander(f"{row['question']}"):
            
            # Utilisation de st.radio pour une meilleure UX
            state_key = f"choice_{d}_{i}"
            if state_key not in st.session_state:
                st.session_state[state_key] = T["level_options"][0] # Default to "1"
            
            # st.radio est plus propre que 5 boutons
            chosen_label = st.radio(
                label=T["level_label"],
                options=T["level_options"],
                key=state_key,
                horizontal=True,
                label_visibility="collapsed" # Le CSS le rend beau
            )
            
            # Mapping du label "1" -> "level_1" et 1
            chosen_key = f"level_{chosen_label}"
            level_num = int(chosen_label)
            desc = row.get(chosen_key, "")
            
            st.caption(f"{T['chosen_level']}: **{chosen_label}/5** — {desc}")

            answers.append({
                "domain": d,
                "question": row["question"],
                "weight": float(row["weight"]),
                "level": level_num
            })

if not answers:
    st.stop()

A = pd.DataFrame(answers)

# =========================
# Scoring (Inchangé)
# =========================
def score_domain(df):
    x = df.assign(norm=(df["level"]-1)/4.0)
    w = x["weight"].clip(lower=0)
    if w.sum() == 0:
        return 0.0
    return float(100 * (x["norm"] * w).sum() / w.sum())

domain_scores = A.groupby("domain").apply(score_domain).to_dict()
global_score = float(np.mean(list(domain_scores.values()))) if domain_scores else 0.0

st.divider()
c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f"<div class='card'><div class='kpi'>{global_score:.1f}</div><div class='kpi-sub'>{T['kpi_global']}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='card'><div class='kpi'>{len(domains)}</div><div class='kpi-sub'>{T['kpi_domains']}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='card'><div class='kpi'>{len(A)}</div><div class='kpi-sub'>{T['kpi_questions']}</div></div>", unsafe_allow_html=True)
with c4:
    weak = [d for d,s in domain_scores.items() if s < 60]
    st.markdown(f"<div class='card'><div class='kpi'>{len(weak)}</div><div class='kpi-sub'>{T['kpi_weak']}</div></div>", unsafe_allow_html=True)

# =========================
# Viz — Radar & Priorisation (Adapté au Dark Mode)
# =========================
st.markdown(f"### {T['radar_title']}")
fig = go.Figure()
r_vals = [domain_scores[d] for d in domains] + [domain_scores[domains[0]]]
theta_vals = domains + [domains[0]]
fig.add_trace(go.Scatterpolar(
    r=r_vals,
    theta=theta_vals,
    fill='toself',
    fillcolor='rgba(167, 139, 250, 0.2)', # Violet 400
    line=dict(color='#A78BFA', width=3) # Violet 400
))
fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0,100], color="#94A3B8", gridcolor="#334155"),
        angularaxis=dict(color="#F8FAFC", gridcolor="#334155")
    ),
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)', # Transparent
    plot_bgcolor='rgba(0,0,0,0)', # Transparent
    margin=dict(l=10, r=10, t=10, b=10)
)
st.plotly_chart(fig, use_container_width=True)

# Priorisation
weights_by_domain = Q.groupby("domain")["weight"].sum().to_dict()
prio = []
for d in domains:
    prio.append({
        "domain": d,
        "score": domain_scores[d],
        "weight_total": float(weights_by_domain.get(d,1.0)),
        "priority_index": float((100-domain_scores[d]) * weights_by_domain.get(d,1.0))
    })
prio_df = pd.DataFrame(prio).sort_values("priority_index", ascending=False)

st.markdown(f"### {T['prio_title']}")
st.dataframe(prio_df, use_container_width=True) # Dataframe s'adapte bien au dark mode

bar = px.bar(
    prio_df, x="domain", y="priority_index", color="score",
    title=T["bar_title"], text=prio_df["score"].round(1),
    color_continuous_scale=px.colors.sequential.Viridis # Une échelle de couleur qui marche sur le noir
)
bar.update_traces(textposition="outside")
bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color="#F8FAFC",
    yaxis_gridcolor="#334155",
    xaxis_gridcolor="#334155"
)
st.plotly_chart(bar, use_container_width=True)

# =========================
# Heuristique d’actions (sans IA)
# =========================
def heuristic_actions(df_q: pd.DataFrame, df_a: pd.DataFrame, lang: str) -> str:
    out = []
    merged = df_a.merge(df_q[["domain","question","weight"]], on=["domain","question"], how="left")
    
    # Priorise les domaines avec le score le plus bas
    prio_domains = prio_df["domain"].tolist()
    
    merged_sorted = merged.set_index('domain').loc[prio_domains].reset_index()
    
    # Prend les 5 actions les plus faibles (level 1) parmi les domaines prioritaires
    wins = merged_sorted[merged_sorted["level"] <= 2].sort_values("level", ascending=True).head(5)
    
    for _, r in wins.iterrows():
        out.append(T["quick_win_line"].format(domain=r["domain"], question=r["question"], level=r["level"]))
    return "\n".join(out) if out else "- —"

quick_wins = heuristic_actions(Q, A, cur_lang)

# =========================
# IA (optionnelle)
# =========================
def ai_summary_openai(api_key: str, model: str, prompt: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role":"system","content":"You are a world-class strategic consultant. Your clients are C-level executives. Be concise, bold, and action-oriented. Use Markdown."},
                {"role":"user","content": prompt}
            ],
            temperature=0.5,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"(AI agent unavailable: {e})"

if not use_ai or not api_key:
    st.info(T["ai_mode_manual"])

base_context = f"""
CONTEXT:
- Overall Score: {global_score:.1f}/100
- Domain Scores: {domain_scores}
- Priority Order (Domains to fix first): {', '.join(prio_df['domain'].tolist())}
- Top Quick Wins (based on low score):
{quick_wins}
"""

summary_text = None
roadmap_text = None

if use_ai and api_key:
    # Prompts améliorés pour un ton "Consultant Senior"
    if cur_lang == "fr":
        sum_prompt = f"""Rédige une synthèse exécutive (3 bullets "Forces", 3 bullets "Risques") pour un COMEX. Ton factuel, direct, sans jargon.
{base_context}"""
        map_prompt = f"""Rédige une feuille de route stratégique (format Markdown) basée sur le diagnostic.
- **Plan 90 Jours (Quick Wins):** 3 actions concrètes (SMART) pour stopper "l'hémorragie" sur les domaines prioritaires.
- **Plan 6 Mois (Structuration):** 3 actions pour bâtir les fondations (gouvernance, outils) sur les domaines faibles.
- **Plan 12 Mois (Scale):** 2 actions pour industrialiser et atteindre le niveau 'Leader'.
Pour chaque action : [Objectif] - [Livrable clé] - [Impact (Faible/Moyen/Élevé)].
{base_context}"""
    else:
        sum_prompt = f"""Write an executive summary (3 'Strengths' bullets, 3 'Risks' bullets) for a C-level meeting. Factual, direct, no jargon.
{base_context}"""
        map_prompt = f"""Write a strategic roadmap (Markdown format) based on the diagnosis.
- **90-Day Plan (Quick Wins):** 3 concrete SMART actions to stop the "bleeding" in priority domains.
- **6-Month Plan (Foundation):** 3 actions to build the foundation (governance, tooling) in weak areas.
- **12-Month Plan (Scale):** 2 actions to industrialize and reach the 'Leader' level.
For each action: [Objective] - [Key Deliverable] - [Impact (Low/Med/High)].
{base_context}"""

    with st.spinner("🚀 L'Agent IA rédige la synthèse..."):
        summary_text = ai_summary_openai(api_key, model_name, sum_prompt)
    with st.spinner("🧭 L'Agent IA construit la feuille de route..."):
        roadmap_text = ai_summary_openai(api_key, model_name, map_prompt)

# =========================
# Rapport Markdown + DL
# =========================
st.markdown(f"### {T['summary_title']}")

if not summary_text:
    strengths = ", ".join([d for d,s in domain_scores.items() if s>=70]) or "—"
    risks = ", ".join([d for d,s in domain_scores.items() if s<60]) or "—"
    summary_text = T["fallback_summary"].format(
        score=global_score, strengths=T["default_strengths"], risks=T["default_risks"],
        s_list=strengths, r_list=risks
    )

if not roadmap_text:
    roadmap_text = f"""**{T['fallback_roadmap_title']}**

{T['fallback_roadmap_90']}
{quick_wins}

{T['fallback_roadmap_6m']}
- Standardiser les processus sur les 2 domaines les plus faibles.
- Mettre en place des KPI de suivi mensuels.
- Outiller (catalogue, qualité) sur le périmètre prioritaire.

{T['fallback_roadmap_12m']}
- Automatiser la gouvernance.
- Passer des audits de certification.
"""

# Formatage du rapport final
report_md = f"""# 🚀 Rapport de Transformation Stratégique

**Score Global de Maturité:** {global_score:.1f}/100

---

## 📊 Scores par Domaine
