# ==========================================================
#  Fichier : app.py
#  Version : v8 – Stable (IA Maturity Agent)
#  Description : Agent IA de Transformation Stratégique
# ==========================================================

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
# Configuration de page
# =========================
st.set_page_config(
    page_title="Agent IA de Transformation Stratégique",
    page_icon="🚀",
    layout="wide"
)

# =========================
# Textes multilingues FR/EN
# =========================
LANGS = {
    "fr": {
        "app_title": "🚀 Agent IA de Transformation Stratégique",
        "app_sub": "Transformez n'importe quel référentiel de maturité en feuille de route IA.",
        "sidebar_title": "⚙️ Paramètres",
        "sidebar_lang": "Langue",
        "sidebar_excel": "Votre Référentiel (Excel)",
        "sidebar_ai_toggle": "Activer l'Agent IA (OpenAI)",
        "sidebar_model": "Modèle OpenAI",
        "sidebar_api": "OPENAI_API_KEY",
        "sidebar_hint": "L'IA est optionnelle. Sans clé, le rapport est généré par heuristique.",
        "questionnaire": "🧩 Auto-évaluation",
        "kpi_global": "Score global",
        "kpi_domains": "Domaines évalués",
        "kpi_questions": "Points de contrôle",
        "kpi_weak": "Domaines prioritaires",
        "radar_title": "📊 Radar de Maturité",
        "prio_title": "🧭 Priorisation Stratégique",
        "bar_title": "Domaines à traiter en premier",
        "ai_mode_manual": "🔒 Mode manuel — Activez l'IA pour une analyse consultant.",
        "summary_title": "📝 Rapport Exécutif & Feuille de Route",
        "download_report": "📥 Télécharger le Rapport (Markdown)",
        "post_title": "🔗 Post LinkedIn prêt à publier",
        "post_text": "J'arrête de voir des diagnostics de maturité Excel qui dorment dans un SharePoint.",
        "post_text_2": "J'ai donc buildé **MaturityAgent** (Streamlit) 🚀.",
        "post_text_3": "C'est un agent IA qui transforme n'importe quel framework (Data, IT, Cyber...) en un **atelier interactif**.",
        "post_text_4": "Le but ? Générer une **feuille de route IA** en < 1h, pas en 3 mois.",
        "post_bullets": [
            "• Mon benchmark : Score global **{score:.1f}/100**",
            "• Domaines prioritaires : **{top3}**"
        ],
        "post_footer": "Le code est open-source. #IA #DataGovernance #Consulting #Streamlit"
    },
    "en": {
        "app_title": "🚀 Strategic Transformation AI Agent",
        "app_sub": "Turn any maturity framework into an AI-driven roadmap.",
        "sidebar_title": "⚙️ Settings",
        "sidebar_lang": "Language",
        "sidebar_excel": "Your Framework (Excel)",
        "sidebar_ai_toggle": "Enable AI Agent (OpenAI)",
        "sidebar_model": "OpenAI Model",
        "sidebar_api": "OPENAI_API_KEY",
        "sidebar_hint": "AI is optional. Without key, a heuristic report is generated.",
        "questionnaire": "🧩 Self-Assessment",
        "kpi_global": "Global Score",
        "kpi_domains": "Domains Evaluated",
        "kpi_questions": "Control Points",
        "kpi_weak": "Priority Domains",
        "radar_title": "📊 Maturity Radar",
        "prio_title": "🧭 Strategic Prioritization",
        "bar_title": "Top Domains to Address",
        "ai_mode_manual": "🔒 Manual mode — Enable AI for consultant-grade insights.",
        "summary_title": "📝 Executive Report & Roadmap",
        "download_report": "📥 Download Report (Markdown)",
        "post_title": "🔗 LinkedIn Post (Ready to Share)",
        "post_text": "I'm tired of seeing Excel maturity diagnostics sleeping in SharePoint.",
        "post_text_2": "So I built **MaturityAgent** (Streamlit) 🚀.",
        "post_text_3": "It's an AI agent that turns any framework (Data, IT, Cyber...) into an **interactive workshop**.",
        "post_text_4": "Goal: Build an **AI roadmap** in <1h, not 3 months.",
        "post_bullets": [
            "• My benchmark: Global Score **{score:.1f}/100**",
            "• Priority Domains: **{top3}**"
        ],
        "post_footer": "Open-source code. #AI #Strategy #DataGovernance #Streamlit"
    }
}

# =========================
# Langue
# =========================
q_params = st.query_params
lang_list = q_params.get("lang", ["fr"])
cur_lang = lang_list[0] if lang_list else "fr"
if cur_lang not in LANGS:
    cur_lang = "fr"
T = LANGS[cur_lang]

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header(T["sidebar_title"])
    lang_choice = st.selectbox(T["sidebar_lang"], ["fr", "en"], index=(0 if cur_lang == "fr" else 1))
    excel = st.file_uploader(T["sidebar_excel"], type=["xlsx"])
    use_ai = st.toggle(T["sidebar_ai_toggle"], value=False)
    model_name = st.text_input(T["sidebar_model"], value="gpt-4o-mini")
    api_key = st.text_input(T["sidebar_api"], type="password", value=os.getenv("OPENAI_API_KEY", ""))
    st.caption(T["sidebar_hint"])

# =========================
# Données par défaut
# =========================
DEFAULT = pd.DataFrame({
    "domain": ["Stratégie", "Gouvernance", "Qualité", "Sécurité"],
    "question": ["La stratégie est-elle claire ?", "La gouvernance est-elle structurée ?", "La qualité est-elle suivie ?", "La sécurité est-elle assurée ?"],
    "weight": [1, 1, 1, 1],
    "level_1": ["Non défini", "Non structuré", "Non mesuré", "Non contrôlé"],
    "level_2": ["En cours", "Partiel", "Basique", "Réactif"],
    "level_3": ["Formalisé", "Structuré", "Suivi", "Préventif"],
    "level_4": ["Optimisé", "Automatisé", "Amélioré", "Proactif"],
    "level_5": ["Excellent", "Exemplaire", "Excellence", "Zero Trust"]
})

if excel:
    try:
        df = pd.read_excel(excel, sheet_name="questions")
    except Exception:
        st.error("Erreur lecture Excel. Feuille `questions` requise.")
        df = DEFAULT.copy()
else:
    df = DEFAULT.copy()

# =========================
# UI principale
# =========================
st.markdown(f"## {T['app_title']}")
st.caption(T["app_sub"])
st.divider()

answers = {}
for i, row in df.iterrows():
    with st.expander(f"{row['domain']} — {row['question']}"):
        level = st.radio("Niveau", ["1", "2", "3", "4", "5"], horizontal=True, key=f"q{i}")
        answers[i] = {"domain": row["domain"], "level": int(level), "weight": row["weight"]}

A = pd.DataFrame(answers).T
scores = A.groupby("domain").apply(lambda x: np.average((x["level"]-1)/4*100, weights=x["weight"])).to_dict()
global_score = np.mean(list(scores.values()))

# =========================
# Affichage des KPIs
# =========================
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric(T["kpi_global"], f"{global_score:.1f}")
with c2: st.metric(T["kpi_domains"], len(scores))
with c3: st.metric(T["kpi_questions"], len(A))
with c4: st.metric(T["kpi_weak"], len([s for s in scores.values() if s < 60]))

# =========================
# Graphiques
# =========================
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=list(scores.values())+[list(scores.values())[0]],
    theta=list(scores.keys())+[list(scores.keys())[0]],
    fill='toself',
    name='Maturité'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# =========================
# Rapport Markdown
# =========================
report = f"""# 🚀 Rapport de Maturité

**Score global :** {global_score:.1f}/100

## 📊 Détails par domaine
"""
for d, s in scores.items():
    report += f"- **{d}** : {s:.1f}/100\n"

report += "\n---\n"
report += T["post_text"] + "\n" + T["post_text_2"] + "\n" + T["post_text_3"] + "\n" + T["post_text_4"]
st.code(report, language="markdown")

st.download_button(
    label=T["download_report"],
    data=report.encode("utf-8"),
    file_name="rapport_maturite.md",
    mime="text/markdown"
)

# =========================
# Post LinkedIn final
# =========================
top3 = ", ".join(list(scores.keys())[:3])
post = "\n".join([
    T["post_text"],
    T["post_text_2"],
    T["post_text_3"],
    T["post_text_4"],
    "\n".join([b.format(score=global_score, top3=top3) for b in T["post_bullets"]]),
    T["post_footer"]
])
st.divider()
st.markdown(f"### {T['post_title']}")
st.code(post, language="text")

st.success("✅ Rapport et post générés avec succès.")
