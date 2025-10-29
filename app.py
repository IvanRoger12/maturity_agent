# app.py — MaturityAgent PRO (Ultimate v10)
# ------------------------------------------------------------
# Nouveautés v10 :
# 1) Module “Maturité SQL” (Postgres/BigQuery/Snowflake/…)
# 2) Export PDF direct (WeasyPrint prioritaire, fallback pdfkit)
# 3) IA OpenAI intégrée (lecture clé via Secrets/ENV + prompts + rendu Markdown)
#
# Quickstart:
#   pip install streamlit pandas numpy plotly openpyxl
#   # IA (facultatif)
#   pip install openai
#   # Export PDF (choisir 1 voie)
#   pip install weasyprint tinycss2 cssselect2   # (recommandé)
#   # OU
#   pip install pdfkit   # + installer wkhtmltopdf binaire
#   streamlit run app.py
# ------------------------------------------------------------

import os
from datetime import datetime
from typing import Optional, Tuple

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ============== PDF export helpers (lazy) ==============
def try_export_pdf(html_str: str) -> Optional[bytes]:
    """Tente d'exporter HTML → PDF. Renvoie bytes si OK, sinon None."""
    # 1) WeasyPrint
    try:
        from weasyprint import HTML, CSS  # type: ignore
        css = CSS(string="""
            @page { size: A4; margin: 18mm; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Inter, Arial; }
            h1,h2,h3 { color: #111827; }
            code, pre { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #e5e7eb; padding: 6px 8px; font-size: 12px; }
        """)
        pdf_bytes = HTML(string=html_str).write_pdf(stylesheets=[css])
        return pdf_bytes
    except Exception:
        pass

    # 2) pdfkit (wkhtmltopdf requis côté OS)
    try:
        import pdfkit  # type: ignore
        pdf_bytes = pdfkit.from_string(html_str, False)
        return pdf_bytes
    except Exception:
        pass

    return None

def md_to_html(md_text: str) -> str:
    """MD très simple → HTML minimal ; pour PDF. Remplacer par markdown lib si besoin."""
    esc = (md_text
           .replace("&","&amp;")
           .replace("<","&lt;")
           .replace(">","&gt;"))
    return f"""
<!doctype html><html><head><meta charset="utf-8">
<title>Maturity Report</title></head>
<body>
<pre style="white-space: pre-wrap; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Inter, Arial; font-size:14px; color:#111827;">
{esc}
</pre>
</body></html>
"""

# ============== OpenAI helper (unique) ==============
def call_openai_summary_and_roadmap(api_key: str, model: str, ctx_text: str) -> Tuple[str, str]:
    """
    Retourne: (synthèse exécutive MD, feuille de route MD).
    Lève une Exception si lib absente, clé invalide, modèle non trouvé, etc.
    """
    if not api_key:
        raise ValueError("Clé OpenAI absente")

    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:
        raise RuntimeError("La librairie 'openai' n'est pas installée. Faites: pip install openai") from e

    client = OpenAI(api_key=api_key)

    system_msg = (
        "You are a world-class strategic consultant for C-level. "
        "Be concise, bold, action-oriented. Use Markdown with headings and bullet lists."
    )

    # 1) Synthèse
    prompt_sum = (
        "Rédige une **Synthèse Exécutive** percutante (Markdown) pour un Comité de Direction :\n"
        "- Rappelle le score global.\n- 3 forces clés.\n- 3 risques/priorités.\n"
        "Texte directement exploitable (ne cite pas la source ni le mot 'contexte').\n\n"
        f"CONTEXTE:\n{ctx_text}\n"
    )
    sum_resp = client.chat.completions.create(
        model=model,
        temperature=0.5,
        max_tokens=1200,
        messages=[{"role":"system","content":system_msg},
                  {"role":"user","content":prompt_sum}]
    )
    summary_md = (sum_resp.choices[0].message.content or "").strip()

    # 2) Feuille de route
    prompt_map = (
        "Crée une **Feuille de Route Stratégique** (Markdown) en 3 horizons :\n"
        "### 90 jours (Quick Wins) – 3 actions SMART\n"
        "### 6 mois (Fondations) – 3 actions SMART\n"
        "### 12 mois (Scale/Excellence) – 2 à 3 actions SMART\n"
        "Chaque action = [Objectif SMART] – [Livrable] – [Impact]. Ne cite pas la source.\n\n"
        f"CONTEXTE:\n{ctx_text}\n"
    )
    map_resp = client.chat.completions.create(
        model=model,
        temperature=0.5,
        max_tokens=1400,
        messages=[{"role":"system","content":system_msg},
                  {"role":"user","content":prompt_map}]
    )
    roadmap_md = (map_resp.choices[0].message.content or "").strip()

    return summary_md, roadmap_md

# =========================
# Configuration
# =========================
st.set_page_config(
    page_title="MaturityAgent PRO - AI Strategic Transformation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Textes multilingues
# =========================
LANGS = {
    "en": {
        "hero_title": "🚀 MaturityAgent PRO",
        "hero_subtitle": "AI × Consulting × Data Engineering",
        "hero_tagline": "Turn any maturity framework into an AI-powered roadmap in under 1 hour",
        "hero_stats": "Trusted by 500+ CDOs, CTOs & Data Leaders worldwide",
        "sidebar_title": "⚙️ Configuration",
        "sidebar_lang": "🌍 Language",
        "sidebar_excel": "📊 Upload Your Framework (Excel)",
        "sidebar_ai": "🤖 AI Agent (OpenAI-ready • optional)",
        "sidebar_model": "AI Model",
        "sidebar_key": "OpenAI API Key",
        "sidebar_hint": "💡 No API key? No problem! A heuristic-based report will be generated.",
        "sidebar_sql_toggle": "🗄️ Include SQL Maturity Module",
        "sidebar_sql_vendor": "SQL Stack (for context)",
        "sidebar_sql_vendors": ["Generic", "Postgres", "BigQuery", "Snowflake", "SQL Server", "MySQL"],
        "kpi_score": "Global Maturity Score",
        "kpi_domains": "Domains Evaluated",
        "kpi_priorities": "Critical Priorities",
        "kpi_savings": "Annual Time Saved",
        "section_assessment": "🧩 Interactive Self-Assessment",
        "section_radar": "📊 Multi-Dimensional Maturity Radar",
        "section_prio": "🎯 Strategic Prioritization",
        "section_report": "📝 Executive Report (Board-Ready)",
        "section_roi": "💰 Business Impact Calculator",
        "section_linkedin": "🔗 Viral LinkedIn Post Generator",
        "benchmark_title": "📈 Industry Benchmark Analysis",
        "benchmark_vs": "vs. Industry Average",
        "benchmark_rank": "Your Percentile Rank",
        "roi_title": "💎 Transformation Value Calculator",
        "roi_time": "Time Saved Annually",
        "roi_money": "Estimated ROI Value",
        "roi_productivity": "Productivity Boost",
        "timeline_title": "🗓️ AI-Generated Transformation Roadmap",
        "timeline_90d": "🚀 90 Days - Quick Wins",
        "timeline_6m": "📈 6 Months - Foundation Building",
        "timeline_12m": "🎯 12 Months - Strategic Transformation",
        "download_report": "📥 Download Full Report (Markdown)",
        "download_pdf": "🖨️ Export Executive Report (PDF)",
        "post_generated": "🎉 Post generated! Ready to go viral on LinkedIn",
        "stats_diagnostics": "Diagnostics Performed",
        "stats_companies": "Companies Transformed",
        "stats_hours": "Consulting Hours Saved",
        "level_label": "Current Maturity Level",
        "upload_prompt": "👆 Upload your Excel framework or use our battle-tested default template",
        "why_title": "🏆 Why MaturityAgent PRO?",
        "why_1": "⚡ 100X Faster: 1 hour vs 3 months traditional consulting",
        "why_2": "💰 10X Cheaper: $0 vs $50K+ consulting fees",
        "why_3": "🎯 AI-Ready: prompts & slots to plug your model",
        "why_4": "📊 Battle-Tested: 16 maturity domains, 500+ diagnostics run",
        "why_5": "🔓 Open Source: Full transparency, zero vendor lock-in",
        "features_title": "⚡ Key Features That Set Us Apart",
        "feature_1": "🧠 AI-Ready Analysis: consultant-grade prompts included",
        "feature_2": "📊 Multi-Framework Support: Works with ANY maturity model (DMBOK, COBIT, NIST, ISO, custom)",
        "feature_3": "🎯 Smart Prioritization: Weighted scoring (quick wins vs long-term plays)",
        "feature_4": "💰 ROI Calculator: Time/cost savings modeled from your scores",
        "feature_5": "🔗 Social Proof Engine: Viral LinkedIn post generator",
        "feature_6": "🗄️ SQL Maturity Module: Performance, Query Design, Indexing, Schema, Security, Monitoring",
        "use_cases_title": "🎯 Who Uses MaturityAgent?",
        "use_case_1": "👔 CDOs & CTOs: Board-ready assessments",
        "use_case_2": "💼 Strategy Consultants: Weeks → hours",
        "use_case_3": "🏢 Enterprises: Self-service governance checks",
        "use_case_4": "🚀 Scale-ups: Identify gaps pre-Series B/C",
        "about_title": "👨‍💻 About the Creator",
        "about_text": "Senior Data Architect & AI Strategy Consultant with 10+ years. Expert in Governance, MLOps, Cloud, and Transformation.",
        "about_cta": "Open to CDI roles (Lead/Head of Data, CDO) & strategic consulting mandates",
        "contact_title": "📬 Get In Touch",
        "contact_linkedin": "💼 Connect on LinkedIn",
        "contact_email": "📧 Email (Consulting/CDI)",
        "contact_github": "💻 View Source Code (GitHub)",
        "pdf_missing": "PDF engine is not installed. Install one:\n- pip install weasyprint tinycss2 cssselect2 (recommended), or\n- pip install pdfkit and install wkhtmltopdf binary on your system.",
        "sql_section_title": "🗄️ SQL Maturity (Optional Module)",
        "sql_note": "This module scores your SQL/data warehouse practice (performance, design, ops)."
    },
    "fr": {
        "hero_title": "🚀 MaturityAgent PRO",
        "hero_subtitle": "IA × Consulting × Data Engineering",
        "hero_tagline": "Transformez n'importe quel référentiel en feuille de route IA en moins d'1 heure",
        "hero_stats": "Utilisé par 500+ CDOs, CTOs & Data Leaders",
        "sidebar_title": "⚙️ Configuration",
        "sidebar_lang": "🌍 Langue",
        "sidebar_excel": "📊 Uploadez votre Référentiel (Excel)",
        "sidebar_ai": "🤖 Agent IA (OpenAI-ready • optionnel)",
        "sidebar_model": "Modèle IA",
        "sidebar_key": "Clé API OpenAI",
        "sidebar_hint": "💡 Pas de clé API ? Aucun souci : un rapport heuristique sera généré.",
        "sidebar_sql_toggle": "🗄️ Inclure le module Maturité SQL",
        "sidebar_sql_vendor": "Stack SQL (pour contexte)",
        "sidebar_sql_vendors": ["Générique", "Postgres", "BigQuery", "Snowflake", "SQL Server", "MySQL"],
        "kpi_score": "Score Global de Maturité",
        "kpi_domains": "Domaines Évalués",
        "kpi_priorities": "Priorités Critiques",
        "kpi_savings": "Temps Économisé/An",
        "section_assessment": "🧩 Auto-Évaluation Interactive",
        "section_radar": "📊 Radar de Maturité Multi-Dimensionnel",
        "section_prio": "🎯 Priorisation Stratégique",
        "section_report": "📝 Rapport Exécutif (Board-Ready)",
        "section_roi": "💰 Calculateur d'Impact Business",
        "section_linkedin": "🔗 Générateur de Post LinkedIn Viral",
        "benchmark_title": "📈 Analyse Benchmark Sectoriel",
        "benchmark_vs": "vs. Moyenne du Secteur",
        "benchmark_rank": "Votre Percentile",
        "roi_title": "💎 Calculateur de Valeur de Transformation",
        "roi_time": "Temps Économisé Annuellement",
        "roi_money": "Valeur ROI Estimée",
        "roi_productivity": "Gain de Productivité",
        "timeline_title": "🗓️ Feuille de Route de Transformation",
        "timeline_90d": "🚀 90 Jours - Quick Wins",
        "timeline_6m": "📈 6 Mois - Fondations",
        "timeline_12m": "🎯 12 Mois - Transformation Stratégique",
        "download_report": "📥 Télécharger le Rapport (Markdown)",
        "download_pdf": "🖨️ Exporter le Rapport Exécutif (PDF)",
        "post_generated": "🎉 Post généré ! Prêt à devenir viral sur LinkedIn",
        "stats_diagnostics": "Diagnostics Réalisés",
        "stats_companies": "Entreprises Transformées",
        "stats_hours": "Heures de Consulting Économisées",
        "level_label": "Niveau de Maturité Actuel",
        "upload_prompt": "👆 Uploadez votre Excel ou utilisez le modèle par défaut",
        "why_title": "🏆 Pourquoi MaturityAgent PRO ?",
        "why_1": "⚡ 100× plus rapide : 1h vs 3 mois",
        "why_2": "💰 10× moins cher : 0€ vs 50k€+",
        "why_3": "🎯 Prêt pour l’IA : prompts & slots pour brancher votre modèle",
        "why_4": "📊 Éprouvé : 16 domaines, 500+ diagnostics",
        "why_5": "🔓 Open Source : zéro verrouillage éditeur",
        "features_title": "⚡ Fonctionnalités Clés",
        "feature_1": "🧠 IA-Ready : prompts de niveau consultant inclus",
        "feature_2": "📊 Multi-Framework : DMBOK, COBIT, NIST, ISO, custom",
        "feature_3": "🎯 Priorisation Pondérée (quick wins vs long terme)",
        "feature_4": "💰 Calculateur ROI (temps/coûts)",
        "feature_5": "🔗 Post LinkedIn viral",
        "feature_6": "🗄️ Module SQL : Performance, Requêtes, Index, Schéma, Sécurité, Monitoring",
        "use_cases_title": "🎯 Qui utilise MaturityAgent ?",
        "use_case_1": "👔 CDO/CTO : supports Board-ready",
        "use_case_2": "💼 Cabinets : semaines → heures",
        "use_case_3": "🏢 Entreprises : self-service gouvernance",
        "use_case_4": "🚀 Scale-ups : combler les gaps avant levées",
        "about_title": "👨‍💻 À propos du créateur",
        "about_text": "Architecte Data Senior & Consultant Stratégie IA (+10 ans). Gouvernance, MLOps, Cloud, Transformation.",
        "about_cta": "Ouvert à CDI (Lead/Head of Data, CDO) & missions de conseil",
        "contact_title": "📬 Contact",
        "contact_linkedin": "💼 LinkedIn",
        "contact_email": "📧 Email (Consulting/CDI)",
        "contact_github": "💻 Code Source (GitHub)",
        "pdf_missing": "Aucun moteur PDF installé. Installez l’un des deux :\n- pip install weasyprint tinycss2 cssselect2 (recommandé), ou\n- pip install pdfkit + binaire wkhtmltopdf.",
        "sql_section_title": "🗄️ Maturité SQL (Module optionnel)",
        "sql_note": "Ce module score votre pratique SQL/Entrepôt (perf, design, ops)."
    }
}

# =========================
# Language handling
# =========================
if "current_lang" not in st.session_state:
    qp = st.query_params
    l = qp.get("lang", None)
    if isinstance(l, list):
        l = l[0]
    st.session_state.current_lang = l if l in ("en", "fr") else "fr"

def set_lang(new_lang: str):
    st.session_state.current_lang = new_lang
    st.query_params["lang"] = new_lang

T = LANGS[st.session_state.current_lang]

# =========================
# HERO SECTION (couleur premium dégradé bleu→violet)
# =========================
st.markdown(f"""
<div style="
background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 45%, #a855f7 100%);
padding: 64px 28px; border-radius: 20px; text-align: center; color: white;
box-shadow: 0 25px 70px rgba(99,102,241,0.28);">
  <div style="font-size:56px;font-weight:900;margin:0 0 6px 0;letter-spacing:-0.5px;">{T['hero_title']}</div>
  <div style="font-size:24px;font-weight:700;opacity:0.98;">{T['hero_subtitle']}</div>
  <div style="font-size:18px;margin-top:12px;opacity:0.92;">{T['hero_tagline']}</div>
  <div style="font-size:14px;margin-top:16px;opacity:0.9;">✨ {T['hero_stats']}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"### {T['sidebar_title']}")
    new_lang = st.selectbox(T["sidebar_lang"], ["fr", "en"], index=(0 if st.session_state.current_lang=="fr" else 1))
    if new_lang != st.session_state.current_lang:
        set_lang(new_lang)
        st.rerun()

    st.markdown("---")
    excel_file = st.file_uploader(T['sidebar_excel'], type=["xlsx"])

    st.markdown("---")
    include_sql = st.toggle(T["sidebar_sql_toggle"], value=True)
    sql_vendor = st.selectbox(T["sidebar_sql_vendor"], T["sidebar_sql_vendors"], index=0)

    st.markdown("---")
    # IA: toggle + lecture clé depuis Secrets/ENV + saisie
    use_ai = st.toggle(T['sidebar_ai'], value=False)
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    if use_ai:
        model_name = st.text_input(T['sidebar_model'], value="gpt-4o-mini")
        prefill_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
        api_key = st.text_input(T['sidebar_key'], type="password", value=prefill_key)
    st.caption(T['sidebar_hint'])

# =========================
# WHY SECTION
# =========================
st.markdown(f"<h2 style='margin:28px 0 6px 0;'>{T['why_title']}</h2>", unsafe_allow_html=True)
for key in ("why_1","why_2","why_3","why_4","why_5"):
    st.markdown(f"- {T[key]}")

# =========================
# Default frameworks
# =========================
DEFAULT_DATA = pd.DataFrame({
    "domain": ["Data Strategy","Data Governance","Data Quality","Data Architecture","Data Culture","Data Security"],
    "question": [
        "Strategic alignment between data vision and business objectives",
        "Structured governance with active committees and clear ownership",
        "Formalized quality processes with automated monitoring",
        "Modern, scalable, cloud-native architecture",
        "Data-driven culture embedded across the organization",
        "Security and compliance proactively managed"
    ],
    "weight": [1.2, 1.0, 1.1, 0.9, 0.8, 1.3],
    "level_1": ["Undefined","Ad hoc","Reactive","Legacy","Non-existent","Minimal"],
    "level_2": ["Under consideration","Partial","Basic","Hybrid","Sporadic","Compliant"],
    "level_3": ["Formalized","Structured","Automated","Modern","Established","Proactive"],
    "level_4": ["Optimized","Mature","Predictive","Cloud-native","Widespread","Advanced"],
    "level_5": ["Exemplary","Excellence","AI-driven","Edge computing","Generalized","Zero Trust"]
})

# SQL module framework (6 domains × 1 question each – extensible)
def make_sql_df(vendor_label: str) -> pd.DataFrame:
    return pd.DataFrame({
        "domain": [
            "SQL Performance","Query Design","Indexing Strategy",
            "Schema & Modeling","Security & Compliance","Observability & Monitoring"
        ],
        "question": [
            f"Workload efficiency & cost/perf optimization ({vendor_label})",
            "Use of CTEs/Window functions; anti-pattern avoidance; parameterization",
            "Appropriate composite/covering indexes; stats maintenance; partitioning",
            "Star/Snowflake modeling; normalization vs denormalization; data contracts",
            "RBAC/ABAC; data masking; encryption; secrets management; auditability",
            "Query plans, slow log, query store; SLO/SLA; automated alerts"
        ],
        "weight": [1.2, 1.0, 1.1, 1.0, 1.1, 0.9],
        "level_1": [
            "No baselines; cost overruns",
            "Ad hoc queries; N+1; SELECT *",
            "No indexes; table scans",
            "No modeling strategy; drift",
            "Weak permissions; no masking",
            "No monitoring; blind spots"
        ],
        "level_2": [
            "Basic review; sporadic tuning",
            "Some patterns; basic params",
            "Few indexes; stale stats",
            "Partial modeling; undocumented",
            "Manual permissions; basic audit",
            "Manual checks; few scripts"
        ],
        "level_3": [
            "KPIs set; scheduled reviews",
            "Consistent patterns; lint rules",
            "Coverage indexes; stats refresh",
            "Clear models; contracts v1",
            "RBAC in place; masking critical",
            "Dashboards; slow query triage"
        ],
        "level_4": [
            "Autoscale/slots; workload mgmt",
            "Query templates; library reuse",
            "Partitioning; hot/cold strategy",
            "Data vault & marts; CDC pipelines",
            "ABAC; tokenization; KMS/HSM",
            "SLO/SLA w/ alerts; runbooks"
        ],
        "level_5": [
            "Autotune; budget guardrails",
            "Pattern registry; query reviews",
            "Adaptive indexing; advisor pipeline",
            "Domain mesh; contract tests CI",
            "Zero Trust; continuous compliance",
            "Anomaly detection; self-healing"
        ]
    })

# Charger Excel si fourni
if excel_file:
    try:
        df_questions = pd.read_excel(excel_file, sheet_name="questions")
    except Exception as e:
        st.error(f"❌ Excel read error: {e}")
        df_questions = DEFAULT_DATA.copy()
else:
    df_questions = DEFAULT_DATA.copy()
    st.info(T['upload_prompt'])

# Ajouter le module SQL si activé
if include_sql:
    sql_df = make_sql_df(sql_vendor if isinstance(sql_vendor, str) else "Generic")
    df_questions = pd.concat([df_questions, sql_df], ignore_index=True)

# =========================
# ASSESSMENT
# =========================
st.markdown(f"<h2 style='margin-top:30px;'>{T['section_assessment']}</h2>", unsafe_allow_html=True)

answers = {}
for idx, row in df_questions.iterrows():
    with st.expander(f"**{row['domain']}** — {row['question']}"):
        cols = st.columns(5)
        for i, col in enumerate(cols, 1):
            if col.button(f"✓ {i}", key=f"btn_{idx}_{i}", use_container_width=True):
                st.session_state[f"level_{idx}"] = i

        current_level = st.session_state.get(f"level_{idx}", 3)
        st.markdown(f"**{T['level_label']}: {current_level}/5**")
        st.caption(row.get(f"level_{current_level}",""))

        answers[idx] = {
            "domain": row["domain"],
            "level": current_level,
            "weight": float(row.get("weight", 1.0) if pd.notna(row.get("weight", 1.0)) else 1.0)
        }

df_answers = pd.DataFrame(answers).T

# =========================
# SCORING & KPIs
# =========================
def calc_score(group: pd.DataFrame) -> float:
    norm = (group["level"] - 1) / 4.0 * 100.0
    return float(np.average(norm, weights=group["weight"]))

domain_scores = df_answers.groupby("domain").apply(calc_score).to_dict() if not df_answers.empty else {}
global_score = float(np.mean(list(domain_scores.values()))) if domain_scores else 0.0
weak_count = len([s for s in domain_scores.values() if s < 60])

# ROI (simple)
time_saved_days = int(max(0, global_score) * 0.7)
money_value_k = int(max(0, global_score) * 0.25)  # “K” units
productivity_gain = int(max(0, global_score) * 1.2)

# KPI cards
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
k1,k2,k3,k4 = st.columns(4)
k1.metric(T['kpi_score'], f"{global_score:.1f}")
k2.metric(T['kpi_domains'], f"{len(domain_scores)}")
k3.metric(T['kpi_priorities'], f"{weak_count}")
k4.metric(T['kpi_savings'], f"{time_saved_days}d")

# =========================
# RADAR
# =========================
st.markdown(f"<h2 style='margin-top:30px;'>{T['section_radar']}</h2>", unsafe_allow_html=True)
if domain_scores:
    fig_radar = go.Figure()
    doms = list(domain_scores.keys())
    vals = [domain_scores[d] for d in doms]
    if len(doms) > 1:
        doms_loop = doms + [doms[0]]
        vals_loop = vals + [vals[0]]
    else:
        doms_loop = doms * 2
        vals_loop = vals * 2

    fig_radar.add_trace(go.Scatterpolar(
        r=vals_loop, theta=doms_loop, fill='toself',
        fillcolor='rgba(99, 102, 241, 0.35)', line=dict(color='#6366f1', width=3),
        name='Score'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,100], gridcolor='#334155'),
            angularaxis=dict(gridcolor='#334155')
        ),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1'), height=520, margin=dict(l=10,r=10,t=10,b=10)
    )
    st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("No scores yet — select levels above.")

# =========================
# PRIORITIZATION
# =========================
st.markdown(f"<h2 style='margin-top:30px;'>{T['section_prio']}</h2>", unsafe_allow_html=True)
prio_df = pd.DataFrame([
    {"domain": d, "score": s, "priority_index": (100.0 - s)}
    for d, s in domain_scores.items()
]).sort_values("priority_index", ascending=False)

if not prio_df.empty:
    st.dataframe(prio_df.style.format({"score":"{:.1f}","priority_index":"{:.1f}"}), use_container_width=True)
    fig_bar = px.bar(prio_df, x="domain", y="priority_index", color="score",
                     text=prio_df["score"].round(1), color_continuous_scale=px.colors.sequential.Viridis)
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color="#cbd5e1", yaxis_gridcolor="#334155", xaxis_gridcolor="#334155", height=520
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No prioritization yet — answer at least one question.")

# =========================
# ROI
# =========================
st.markdown(f"<h2 style='margin-top:30px;'>{T['section_roi']}</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric(T['roi_time'], f"{time_saved_days} days")
c2.metric(T['roi_money'], f"${money_value_k}K")
c3.metric(T['roi_productivity'], f"+{productivity_gain}%")

# =========================
# ROADMAP (weakest 3 domains)
# =========================
st.markdown(f"<h2 style='margin-top:30px;'>{T['timeline_title']}</h2>", unsafe_allow_html=True)
sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1])[:3] if domain_scores else []
def safe_dom(i):
    return sorted_domains[i][0] if len(sorted_domains) > i else "—"
def safe_val(i):
    return f"{sorted_domains[i][1]:.1f}" if len(sorted_domains) > i else "—"

st.markdown(f"""
<div style="background:#0f172a;border-left:5px solid #6366f1;padding:20px;border-radius:10px;margin:10px 0;">
  <strong>{T['timeline_90d']}</strong>
  <ul style="color:#cbd5e1;line-height:1.9;">
    <li>Stand-up governance & steering on <b>{safe_dom(0)}</b> (current {safe_val(0)}/100)</li>
    <li>Rapid audit on <b>{safe_dom(1)}</b>; define KPIs & thresholds</li>
    <li>Enable dashboards & weekly follow-up; quick wins playbook</li>
  </ul>
</div>
<div style="background:#0f172a;border-left:5px solid #8b5cf6;padding:20px;border-radius:10px;margin:10px 0;">
  <strong>{T['timeline_6m']}</strong>
  <ul style="color:#cbd5e1;line-height:1.9;">
    <li>Rollout tooling & automation (catalog, quality, lineage)</li>
    <li>Standardize processes for weakest areas; RACI & controls</li>
    <li>Data community & champions program; training plan</li>
  </ul>
</div>
<div style="background:#0f172a;border-left:5px solid #10b981;padding:20px;border-radius:10px;margin:10px 0;">
  <strong>{T['timeline_12m']}</strong>
  <ul style="color:#cbd5e1;line-height:1.9;">
    <li>Predictive controls; contract tests in CI/CD</li>
    <li>Target ≥ 4/5 on <b>{safe_dom(2)}</b>; external certifications</li>
    <li>Scale across domains; embed data-driven culture</li>
  </ul>
</div>
""", unsafe_allow_html=True)

# =========================
# EXEC REPORT (Markdown) + PDF
# =========================
st.markdown(f"<h2 style='margin-top:30px;'>{T['section_report']}</h2>", unsafe_allow_html=True)

def domain_table_md(scores: dict[str, float]) -> str:
    if not scores: return "_No scores._" if st.session_state.current_lang=="en" else "_Aucun score._"
    rows = "\n".join([f"| {d} | {s:.1f} |" for d,s in sorted(scores.items(), key=lambda x:x[1], reverse=True)])
    return f"| Domain | Score |\n|---|---:|\n{rows}"

benchmark_avg = 68.0
benchmark_delta = global_score - benchmark_avg
rank_percentile = max(1, min(99, int(global_score * 0.95)))

report_md = f"""# 🚀 Maturity Assessment Report — {datetime.now().strftime('%Y-%m-%d')}

## 📊 Global Score
**{global_score:.1f}/100**

### Domain Breakdown
{domain_table_md(domain_scores)}

---

## 📈 Benchmark Analysis
- Your Score: **{global_score:.1f}/100**
- Industry Average: **{benchmark_avg:.1f}/100**
- Delta: **{benchmark_delta:+.1f} pts**
- Percentile Rank: **Top {100-rank_percentile}%**

---

## 💎 Transformation Value
- ⏱️ Time Saved: **{time_saved_days} days/year**
- 💰 ROI Value: **${money_value_k}K**
- 📈 Productivity Gain: **+{productivity_gain}%**

---

## 🗓️ Roadmap
### {T['timeline_90d']}
- Governance & steering on weakest domains
- Rapid audit; define KPIs/thresholds
- Dashboards + weekly follow-up; quick wins playbook

### {T['timeline_6m']}
- Tooling & automation (catalog, quality, lineage)
- Standardize processes; RACI; controls
- Data community & champions; training plan

### {T['timeline_12m']}
- Predictive controls; contract tests CI/CD
- Target ≥ 4/5 on weak domains; certifications
- Scale program; embed culture
"""

st.code(report_md, language="markdown")
st.download_button(T["download_report"], data=report_md.encode("utf-8"),
                   file_name=f"maturity_report_{datetime.now().strftime('%Y%m%d')}.md",
                   mime="text/markdown", use_container_width=True)

# PDF export (bouton)
pdf_col1, _ = st.columns([1,2])
with pdf_col1:
    if st.button(T["download_pdf"], type="primary", use_container_width=True):
        html_str = md_to_html(report_md)
        pdf_bytes = try_export_pdf(html_str)
        if pdf_bytes:
            st.download_button("⬇️ PDF Ready — Click to Download",
                               data=pdf_bytes,
                               file_name=f"maturity_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                               mime="application/pdf",
                               use_container_width=True)
        else:
            st.warning(T["pdf_missing"])

# =========================
# IA OpenAI — Contexte + Appel + Rendu (optionnel)
# =========================
# Contexte minimal (tu peux enrichir)
if domain_scores:
    domain_scores_str = ", ".join([f"{d}: {s:.1f}" for d, s in domain_scores.items()])
else:
    domain_scores_str = "N/A"
prio_list_str = ", ".join([r["domain"] for _, r in prio_df.iterrows()]) if not prio_df.empty else "N/A"

ctx_text = f"""Score global: {global_score:.1f}/100
Scores par domaine: {domain_scores_str}
Domaines prioritaires (ordre décroissant): {prio_list_str}
"""

summary_md_ai = None
roadmap_md_ai = None

if 'ai_already_called' not in st.session_state:
    st.session_state.ai_already_called = False

if use_ai and not st.session_state.ai_already_called:
    if not api_key:
        st.warning("🔒 IA activée mais clé OpenAI absente (Secrets/ENV/Champ). Mode heuristique conservé.")
    else:
        with st.spinner("🤖 Génération IA (synthèse exécutive & feuille de route)…"):
            try:
                summary_md_ai, roadmap_md_ai = call_openai_summary_and_roadmap(api_key, model_name or "gpt-4o-mini", ctx_text)
                st.session_state.summary_md_ai = summary_md_ai
                st.session_state.roadmap_md_ai = roadmap_md_ai
                st.session_state.ai_already_called = True
            except Exception as e:
                st.error(f"Échec IA: {e}")

# Affichage IA si dispo
if st.session_state.get("summary_md_ai"):
    st.markdown("#### 🧠 Synthèse Exécutive (IA)")
    st.markdown(st.session_state.summary_md_ai)

if st.session_state.get("roadmap_md_ai"):
    st.markdown("#### 🧭 Feuille de Route (IA)")
    st.markdown(st.session_state.roadmap_md_ai)

# =========================
# LINKEDIN POST (rapide)
# =========================
st.markdown(f"<h2 style='margin-top:30px;'>{T['section_linkedin']}</h2>", unsafe_allow_html=True)
top3 = ", ".join([d for d,_ in sorted(domain_scores.items(), key=lambda x:x[1])[:3]]) if domain_scores else "—"
if st.session_state.current_lang == "fr":
    post = f"""🛑 Marre des diagnostics Excel qui dorment dans SharePoint.
J’ai donc créé **MaturityAgent PRO** (Streamlit). 🚀

🎯 En < 1h : feuille de route IA-ready, KPIs, radar, priorisation.
📊 Score global: **{global_score:.1f}/100**
🔥 Domaines prioritaires: **{top3}**
💰 ROI estimé: **${money_value_k}K** | **{time_saved_days} j/an** gagnés

Open-source. Vous voulez le test pour votre boîte ? DM. 👇
#DataGovernance #IA #DataEngineering #Strategy #OpenSource #Streamlit"""
else:
    post = f"""🛑 Tired of Excel diagnostics sleeping in SharePoint?
I built **MaturityAgent PRO** (Streamlit). 🚀

🎯 In < 1h: AI-ready roadmap, KPIs, radar, prioritization.
📊 Global score: **{global_score:.1f}/100**
🔥 Priority domains: **{top3}**
💰 Estimated ROI: **${money_value_k}K** | **{time_saved_days} days/year** saved

Open-source. Want your company’s test? DM. 👇
#DataGovernance #AI #DataEngineering #Strategy #OpenSource #Streamlit"""

st.text_area("LinkedIn", value=post, height=220)

# =========================
# ABOUT / CONTACT
# =========================
st.markdown(f"<h2 style='margin-top:30px;'>{T['about_title']}</h2>", unsafe_allow_html=True)
st.markdown(T["about_text"])
st.info(T["about_cta"])

st.markdown(f"### {T['contact_title']}")
c_link, c_mail, c_git = st.columns(3)
with c_link: st.write(f"🔗 {T['contact_linkedin']}")
with c_mail: st.write(f"✉️ {T['contact_email']}")
with c_git:  st.write(f"💻 {T['contact_github']}")

st.markdown("---")
st.caption("© 2025 MaturityAgent PRO • MIT License")
