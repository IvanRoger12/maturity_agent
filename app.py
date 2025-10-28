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
    page_title="MaturityAgent — Enterprise Maturity AI",
    page_icon="🧭",
    layout="wide"
)

# =========================
# I18N — Multilingue FR/EN
# =========================
LANGS = {
    "fr": {
        "app_title": "🧭 MaturityAgent — Agent IA d’évaluation de maturité",
        "app_sub": "Charge un référentiel Excel ou utilise le modèle par défaut. Obtiens un score par domaine, une synthèse IA et une feuille de route priorisée.",
        "sidebar_title": "⚙️ Paramètres",
        "sidebar_lang": "Langue",
        "sidebar_excel": "Référentiel Excel (facultatif)",
        "sidebar_ai_toggle": "Activer l'agent IA (OpenAI)",
        "sidebar_model": "Modèle OpenAI",
        "sidebar_api": "OPENAI_API_KEY",
        "sidebar_hint": "L’IA est optionnelle : sans clé, le diagnostic texte est généré sans LLM.",
        "questionnaire": "🧩 Questionnaire",
        "level_label": "Niveau atteint",
        "level": ["level_1","level_2","level_3","level_4","level_5"],
        "chosen_level": "Niveau choisi",
        "kpi_global": "Score global",
        "kpi_domains": "Domaines évalués",
        "kpi_questions": "Questions",
        "kpi_weak": "Domaines prioritaires (<60)",
        "radar_title": "📊 Radar par domaine",
        "prio_title": "🧭 Priorisation (faible maturité × poids)",
        "bar_title": "Domaines à traiter en premier",
        "ai_mode_manual": "🔒 Mode manuel — active l’IA (OpenAI) dans la barre latérale pour une synthèse exécutive et une feuille de route détaillées.",
        "summary_title": "📝 Rapport (Markdown)",
        "download_report": "📥 Télécharger le rapport Markdown",
        "post_title": "🔗 Post LinkedIn (copier-coller)",
        "post_text": "Aujourd’hui, j’ai publié **MaturityAgent** (Streamlit) — un agent IA qui évalue la **maturité d’entreprise** (Data, IT, Sécurité, Gouvernance, Produit).",
        "post_bullets": [
            "• Score global: **{score:.1f}/100**",
            "• Domaines prioritaires: {top3}",
            "• Feuille de route: 90j / 6m / 12m (actions SMART)"
        ],
        "post_footer": "Je l’ai conçu pour des ateliers flash: import Excel, questionnaire dynamique, radar, rapport Markdown & synthèse IA.\nQui veut tester sur son référentiel ? 👇\n#DataGovernance #Risk #Cyber #IT #Product #Streamlit #AI #Consulting",
        "xls_template": "📦 Télécharger le modèle Excel",
        "xls_template_tip": "Modèle: feuille `questions` avec colonnes domain, question, weight, level_1..level_5",
        "default_strengths": "Forces",
        "default_risks": "Risques/Priorités",
        "fallback_summary": "Synthèse — Score global **{score:.1f}/100**. {strengths}: {s_list}. {risks}: {r_list}.",
        "fallback_roadmap_title": "Feuille de route (heuristique sans IA)",
        "fallback_roadmap_90": "**90 jours:**",
        "fallback_roadmap_6m": "**6 mois:**",
        "fallback_roadmap_12m": "**12 mois:**",
        "quick_win_line": "- [{domain}] **Quick win** sur “{question}” (poids {weight:.2f}) — viser niveau 3 dans 90 jours."
    },
    "en": {
        "app_title": "🧭 MaturityAgent — Enterprise Maturity AI",
        "app_sub": "Upload an Excel framework or use the default one. Get per-domain scores, an AI executive summary, and a prioritized roadmap.",
        "sidebar_title": "⚙️ Settings",
        "sidebar_lang": "Language",
        "sidebar_excel": "Excel framework (optional)",
        "sidebar_ai_toggle": "Enable AI agent (OpenAI)",
        "sidebar_model": "OpenAI model",
        "sidebar_api": "OPENAI_API_KEY",
        "sidebar_hint": "AI is optional: without a key, a heuristic (non-LLM) summary is generated.",
        "questionnaire": "🧩 Questionnaire",
        "level_label": "Selected level",
        "level": ["level_1","level_2","level_3","level_4","level_5"],
        "chosen_level": "Selected level",
        "kpi_global": "Global score",
        "kpi_domains": "Domains evaluated",
        "kpi_questions": "Questions",
        "kpi_weak": "Priority domains (<60)",
        "radar_title": "📊 Domain radar",
        "prio_title": "🧭 Prioritization (low maturity × weight)",
        "bar_title": "Top domains to address",
        "ai_mode_manual": "🔒 Manual mode — enable AI (OpenAI) in the sidebar for an executive summary and detailed roadmap.",
        "summary_title": "📝 Report (Markdown)",
        "download_report": "📥 Download Markdown report",
        "post_title": "🔗 LinkedIn Post (copy/paste)",
        "post_text": "Today I released **MaturityAgent** (Streamlit) — an AI agent to assess **enterprise maturity** (Data, IT, Security, Governance, Product).",
        "post_bullets": [
            "• Global score: **{score:.1f}/100**",
            "• Priority domains: {top3}",
            "• Roadmap: 90d / 6mo / 12mo (SMART actions)"
        ],
        "post_footer": "Built for flash workshops: Excel import, dynamic questionnaire, radar, Markdown report & AI summary.\nWho wants to try it on their framework? 👇\n#DataGovernance #Risk #Cyber #IT #Product #Streamlit #AI #Consulting",
        "xls_template": "📦 Download Excel template",
        "xls_template_tip": "Template: sheet `questions` with columns domain, question, weight, level_1..level_5",
        "default_strengths": "Strengths",
        "default_risks": "Risks/Priorities",
        "fallback_summary": "Summary — Global score **{score:.1f}/100**. {strengths}: {s_list}. {risks}: {r_list}.",
        "fallback_roadmap_title": "Roadmap (heuristic, no AI)",
        "fallback_roadmap_90": "**90 days:**",
        "fallback_roadmap_6m": "**6 months:**",
        "fallback_roadmap_12m": "**12 months:**",
        "quick_win_line": "- [{domain}] **Quick win** on “{question}” (weight {weight:.2f}) — target level 3 within 90 days."
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
# CSS (léger)
# =========================
st.markdown("""
<style>
.title { font-size: 34px; font-weight: 800; margin-bottom: 4px; }
.sub { color:#667085; margin-bottom: 18px; }
.card { background: rgba(255,255,255,0.75); border:1px solid rgba(0,0,0,0.06); border-radius:16px; padding:18px; }
.kpi { font-size: 36px; font-weight: 800; line-height:1; }
.kpi-sub { color:#667085; font-size: 13px; }
.gradient { background: linear-gradient(90deg,#0ea5e9,#7c3aed); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
button[kind="secondary"] { border-radius: 10px !important; }
div.stButton > button:hover { transform: translateY(-1px); }
</style>
""", unsafe_allow_html=True)

st.markdown(f"<div class='title gradient'>{T['app_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub'>{T['app_sub']}</div>", unsafe_allow_html=True)

# =========================
# Référentiel par défaut
# =========================
DEFAULT_QUESTIONS = pd.DataFrame([
    ["Data", "Catalogue de données formalisé ?", 0.25, "Non", "Épars", "Début de catalogue", "Catalogue utilisé", "Catalogue gouverné & audité"],
    ["Data", "Qualité des données mesurée (KPI) ?", 0.25, "Non", "Ad hoc", "Pilotes", "Suivi mensuel", "Score DQ automatisé & SLA"],
    ["Data", "Lignage / traçabilité ?", 0.20, "Non", "Partiel", "Périmètre clé", "Généralisé", "Automatisé & outillé"],
    ["Data", "Self-service BI ?", 0.15, "Non", "Limité", "Expérimenté", "Déployé", "Gouverné & sécurisé"],
    ["Data", "Rôle CDO / comité data ?", 0.15, "Non", "Informel", "Défini", "Actif", "Mature & sponsor ExCom"],

    ["IT", "Gestion des changements (ITIL/DevOps) ?", 0.20, "Non", "Basique", "Processus défini", "CI/CD partiel", "CI/CD & SRE matures"],
    ["IT", "Observabilité (logs, métriques, traces) ?", 0.20, "Non", "Partiel", "Stack observabilité", "SLO/SLI suivis", "SRE & alerting prédictif"],
    ["IT", "Disponibilité & reprise (DRP) ?", 0.20, "Aucun", "RTO/RPO non testés", "Plan testé", "Multi-AZ/région", "Chaos testing & résilience"],
    ["IT", "Sécurité des environnements ?", 0.20, "Non", "Durcissement basique", "IAM + secrets gérés", "Zero-Trust partiel", "Zero-Trust mature"],
    ["IT", "Gestion des coûts cloud ?", 0.20, "Non", "Suivi mensuel", "Budgets / alertes", "FinOps tags", "FinOps optimisation continue"],

    ["Sécurité", "Gouvernance ISO 27001/27002 ?", 0.20, "Non", "Feuille de route", "SMSI lancé", "SMSI audité", "Certifié & amélioration continue"],
    ["Sécurité", "Gestion des accès (IAM, SoD) ?", 0.25, "Non", "Revue ad hoc", "Revue périodique", "RBAC/ABAC", "IGA + recertif automatisée"],
    ["Sécurité", "Sensibilisation & phishing test ?", 0.15, "Non", "Ponctuel", "Trimestriel", "Mensuel", "Culture sécurité forte"],
    ["Sécurité", "Protection des données (chiffrement, DLP) ?", 0.20, "Non", "Partiel", "Chiffrement at-rest", "At-rest + in-transit + DLP", "CLoP + tokenisation"],
    ["Sécurité", "Gestion vulnérabilités (patching) ?", 0.20, "Non", "Mensuel", "Bimensuel", "Hebdo", "Continu + risk-based"],

    ["Gouvernance", "Rôles et responsabilités (RACI) ?", 0.25, "Non", "Partiel", "RACI défini", "RACI appliqué", "RACI outillé & suivi"],
    ["Gouvernance", "Processus documentés ?", 0.20, "Non", "Clés", "Standardisés", "Amélioration continue", "KPI de process & audités"],
    ["Gouvernance", "Gestion des risques (registre) ?", 0.20, "Non", "Initial", "Tenue à jour", "Scoring & plans", "ERM intégré comex"],
    ["Gouvernance", "Conformité (RGPD, sectoriel) ?", 0.20, "Non", "Plan d’actions", "Procédures en place", "Audits réguliers", "Contrôles automatisés"],
    ["Gouvernance", "Comité transformation (cadence) ?", 0.15, "Non", "Irrégulier", "Mensuel", "Bimensuel", "Hebdo orienté valeur"],

    ["Produit", "Backlog priorisé (valeur) ?", 0.25, "Non", "Basique", "Value scoring", "WSJF/ICE", "Portfolio management"],
    ["Produit", "Découverte utilisateur (UX research) ?", 0.15, "Non", "Ponctuel", "Cadencé", "OKR orientés user", "Dual-track discovery/delivery"],
    ["Produit", "Mesure d’impact (KPI/OKR) ?", 0.20, "Non", "Défini", "Tracké", "Lié aux décisions", "Comité performance"],
    ["Produit", "Agile à l’échelle (Scrum/Kanban) ?", 0.20, "Non", "Pilotes", "Multi-équipes", "PI Planning", "Lean Portfolio"],
    ["Produit", "Design System / qualité UI ?", 0.20, "Non", "Guidelines", "Design system v1", "DS versionné", "DesignOps mature"],
], columns=["domain","question","weight","level_1","level_2","level_3","level_4","level_5"])

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
    df = DEFAULT_QUESTIONS.copy()
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
        for c in ["level_1","level_2","level_3","level_4","level_5"]:
            if c not in df.columns:
                df[c] = ""
        return df
    except Exception:
        return DEFAULT_QUESTIONS.copy()

Q = load_questions(excel) if excel else DEFAULT_QUESTIONS.copy()

# =========================
# Questionnaire (boutons 1..5)
# =========================
st.markdown(f"### {T['questionnaire']}")
domains = sorted(Q["domain"].unique())
answers = []

for d in domains:
    st.markdown(f"#### **{d}**")
    block = Q[Q["domain"]==d].reset_index(drop=True)
    for i, row in block.iterrows():
        with st.expander(f"{row['question']}"):
            labels = T["level"]
            state_key = f"choice_{d}_{i}"
            if state_key not in st.session_state:
                st.session_state[state_key] = "level_1"

            cols_btn = st.columns(5)
            for idx, level_key in enumerate(labels):
                with cols_btn[idx]:
                    clicked = st.button(
                        f"{level_key.split('_')[1]}/5",
                        key=f"{d}_{i}_{idx}",
                        use_container_width=True
                    )
                    if clicked:
                        st.session_state[state_key] = level_key

            chosen = st.session_state[state_key]
            desc = row.get(chosen, "")
            st.caption(f"{T['chosen_level']}: **{chosen.split('_')[1]}/5** — {desc}")

            answers.append({
                "domain": d,
                "question": row["question"],
                "weight": float(row["weight"]),
                "level": LEVEL_MAP[chosen]
            })

if not answers:
    st.stop()

A = pd.DataFrame(answers)

# =========================
# Scoring
# =========================
def score_domain(df):
    x = df.assign(norm=(df["level"]-1)/4.0)
    w = x["weight"].clip(lower=0)
    if w.sum() == 0:
        return 0.0
    return float(100 * (x["norm"] * w).sum() / w.sum())

domain_scores = A.groupby("domain").apply(score_domain).to_dict()
global_score = float(np.mean(list(domain_scores.values()))) if domain_scores else 0.0

c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f"<div class='card'><div class='kpi'>{global_score:.1f}</div><div class='kpi-sub'>{T['kpi_global']}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='card'><div class='kpi'>{len(domains)}</div><div class='kpi-sub'>{T['kpi_domains']}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='card'><div class='kpi'>{len(A)}</div><div class='kpi-sub'>{T['kpi_questions']}</div></div>", unsafe_allow_html=True)
with c4:
    weak = [d for d,s in domain_scores.items() if s < 60]
    st.markdown(f"<div class='card'><div class='kpi'>{len(weak)}</div><div class='kpi-sub'>{T['kpi_weak']}</div></div>", unsafe_allow_html=True)

# =========================
# Viz — Radar & Priorisation
# =========================
st.markdown(f"### {T['radar_title']}")
fig = go.Figure()
r_vals = [domain_scores[d] for d in domains] + [domain_scores[domains[0]]]
theta_vals = domains + [domains[0]]
fig.add_trace(go.Scatterpolar(
    r=r_vals,
    theta=theta_vals,
    fill='toself',
    fillcolor='rgba(14,165,233,0.20)',
    line=dict(width=2)
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0,100])),
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10)
)
st.plotly_chart(fig, use_container_width=True)

# Priorisation (faible score × poids total du domaine)
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
st.dataframe(prio_df, use_container_width=True)

bar = px.bar(
    prio_df, x="domain", y="priority_index", color="score",
    title=T["bar_title"], text=prio_df["score"].round(1)
)
bar.update_traces(textposition="outside")
st.plotly_chart(bar, use_container_width=True)

# =========================
# Heuristique d’actions (sans IA)
# =========================
def heuristic_actions(df_q: pd.DataFrame, df_a: pd.DataFrame, lang: str) -> str:
    out = []
    merged = df_a.merge(df_q[["domain","question","weight"]], on=["domain","question"], how="left")
    for d in df_q["domain"].unique():
        sub = merged[(merged["domain"]==d)].sort_values(["level","weight"], ascending=[True, False])
        wins = sub.head(3)
        for _, r in wins.iterrows():
            out.append(T["quick_win_line"].format(domain=d, question=r["question"], weight=r["weight"]))
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
                {"role":"system","content":"You are a senior transformation consultant (IT/Data/Security/Product). Be concise, executive tone."},
                {"role":"user","content": prompt}
            ],
            temperature=0.4,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"(AI disabled/unavailable) {e}"

if not use_ai or not api_key:
    st.info(T["ai_mode_manual"])

base_context = f"Domain scores: {domain_scores}\nPriority order: {', '.join(prio_df['domain'].tolist())}\nQuick wins:\n{quick_wins}"

summary_text = None
roadmap_text = None

if use_ai and api_key:
    # Prompts FR/EN minimalistes
    if cur_lang == "fr":
        sum_prompt = f"""Écris une synthèse exécutive (≤10 lignes) d'un diagnostic de maturité (Data/IT/Sécurité/Gouvernance/Produit).
Mets en avant 3 forces et 3 risques, ton factuel COMEX.
Contexte:\n{base_context}"""
        map_prompt = f"""Feuille de route priorisée (actions SMART) :
- 90 jours: 5 actions pragmatiques
- 6 mois: 5 actions structurantes
- 12 mois: 5 actions de scale
Pour chaque action: objectif mesurable, owner (rôle), effort (S/M/L), impact, dépendances.
Contexte:\n{base_context}"""
    else:
        sum_prompt = f"""Write an executive summary (≤10 lines) of a maturity assessment (Data/IT/Security/Governance/Product).
Highlight 3 strengths and 3 risks, factual C-suite tone.
Context:\n{base_context}"""
        map_prompt = f"""Prioritized roadmap (SMART actions):
- 90 days: 5 pragmatic actions
- 6 months: 5 structural actions
- 12 months: 5 scale actions
For each: measurable objective, owner (role), effort (S/M/L), impact, dependencies.
Context:\n{base_context}"""

    summary_text = ai_summary_openai(api_key, model_name, sum_prompt)
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
    if cur_lang == "fr":
        roadmap_text = f"""**{T['fallback_roadmap_title']}**  
{T['fallback_roadmap_90']}  
{quick_wins}

{T['fallback_roadmap_6m']}  
- Standardiser les processus dans les 2 domaines les plus faibles  
- Mettre en place des KPI mensuels et des revues trimestrielles  
- Outiller (catalogue, observabilité, IAM) sur périmètre prioritaire  

{T['fallback_roadmap_12m']}  
- Passage à l’échelle (automatisation, gouvernance outillée)  
- Audits externes / certifications (ISO, RGPD, FinOps)  
- Lean Portfolio pour arbitrer la valeur sur l’ensemble des domaines
"""
    else:
        roadmap_text = f"""**{T['fallback_roadmap_title']}**  
{T['fallback_roadmap_90']}  
{quick_wins}

{T['fallback_roadmap_6m']}  
- Standardize processes in the 2 weakest domains  
- Set monthly KPIs & quarterly reviews  
- Tooling (catalog, observability, IAM) on priority scope  

{T['fallback_roadmap_12m']}  
- Scale automation & governance tooling  
- External audits / certifications (ISO, GDPR, FinOps)  
- Lean Portfolio to arbitrate value across domains
"""

series_scores = pd.Series(domain_scores).round(1).to_string()
prio_table = prio_df[['domain','priority_index','score','weight_total']].to_string(index=False)

report_md = f"""# MaturityAgent — Report

**{T['kpi_global']}:** {global_score:.1f}/100

## Scores
{series_scores}

## Prioritization
{prio_table}

## Executive Summary
{summary_text}

## Roadmap
{roadmap_text}
"""

st.code(report_md, language="markdown")
st.download_button(T["download_report"], data=report_md.encode("utf-8"), file_name="maturity_report.md")

# =========================
# Post LinkedIn
# =========================
st.markdown(f"### {T['post_title']}")
top3 = ", ".join(prio_df.head(3)["domain"].tolist())
post_lines = [
    T["post_text"],
    *[b.format(score=global_score, top3=top3) for b in T["post_bullets"]],
    T["post_footer"]
]
post_txt = "\n".join(post_lines)
st.code(post_txt, language="markdown")
