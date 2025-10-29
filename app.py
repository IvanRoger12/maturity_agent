# app.py — MaturityAgent PRO (Ultimate v9.1 – Stable)
# ------------------------------------------------------------
# ✅ Correctifs :
# - Init langue sécurisée (plus de KeyError)
# - Widgets avec clés explicites
# - IA activable via clé OpenAI dans Secrets
# - Boutons download sans width="stretch" (TypeError corrigé)
# - Pandas groupby.apply + width Streamlit fixés
# ------------------------------------------------------------

import os
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ============== PDF Export Helper ==============
def try_export_pdf(html_str: str):
    """Try exporting HTML to PDF via WeasyPrint or pdfkit."""
    try:
        from weasyprint import HTML, CSS
        css = CSS(string="""
            @page { size: A4; margin: 18mm; }
            body { font-family: 'Segoe UI', Roboto, Arial; }
            h1,h2,h3 { color: #111827; }
            th, td { border: 1px solid #e5e7eb; padding: 6px 8px; font-size: 12px; }
        """)
        return HTML(string=html_str).write_pdf(stylesheets=[css])
    except Exception:
        pass
    try:
        import pdfkit
        return pdfkit.from_string(html_str, False)
    except Exception:
        pass
    return None

# ============== OpenAI Helper ==============
def get_openai_client():
    key = os.getenv("OPENAI_API_KEY", "")
    try:
        key = key or st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        pass
    if not key:
        return None, "No OPENAI_API_KEY found. Add it in Streamlit Secrets."
    try:
        from openai import OpenAI
        return OpenAI(api_key=key), None
    except Exception as e:
        return None, f"OpenAI SDK unavailable: {e}"

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="MaturityAgent PRO - AI Strategic Transformation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Lang init safe
# =========================
if "current_lang" not in st.session_state:
    try:
        qp = st.query_params
        lang = qp.get("lang", ["fr"])
        lang = lang[0] if isinstance(lang, list) else (lang or "fr")
    except Exception:
        lang = "fr"
    if lang not in ("fr", "en"):
        lang = "fr"
    st.session_state.current_lang = lang

LANGS = {
    "fr": {"hero_title": "🚀 MaturityAgent PRO",
           "hero_subtitle": "IA × Consulting × Data Engineering",
           "hero_tagline": "Transformez tout référentiel en feuille de route IA en moins d'1h",
           "hero_stats": "Utilisé par 500+ CDOs & Data Leaders",
           "sidebar_title": "⚙️ Configuration",
           "sidebar_lang": "🌍 Langue",
           "sidebar_excel": "📊 Uploadez votre Référentiel (Excel)",
           "sidebar_ai": "🤖 Agent IA (optionnel)",
           "sidebar_model": "Modèle IA",
           "sidebar_hint": "💡 Pas de clé ? Un rapport heuristique sera généré.",
           "sidebar_sql_toggle": "🗄️ Inclure le module SQL",
           "sidebar_sql_vendor": "Stack SQL",
           "kpi_score": "Score Global",
           "kpi_domains": "Domaines",
           "kpi_priorities": "Priorités",
           "kpi_savings": "Jours gagnés/an",
           "section_assessment": "🧩 Auto-Évaluation Interactive",
           "section_radar": "📊 Radar de Maturité",
           "section_prio": "🎯 Priorisation",
           "section_report": "📝 Rapport Exécutif",
           "section_roi": "💰 ROI Business",
           "section_linkedin": "🔗 Post LinkedIn Viral",
           "timeline_title": "🗓️ Feuille de Route IA",
           "timeline_90d": "🚀 90 Jours – Quick Wins",
           "timeline_6m": "📈 6 Mois – Structuration",
           "timeline_12m": "🎯 12 Mois – Transformation",
           "download_report": "📥 Télécharger le Rapport (Markdown)",
           "download_pdf": "🖨️ Exporter le Rapport PDF"},
    "en": {"hero_title": "🚀 MaturityAgent PRO",
           "hero_subtitle": "AI × Consulting × Data Engineering",
           "hero_tagline": "Turn any framework into an AI roadmap in under 1 hour",
           "hero_stats": "Trusted by 500+ CDOs & Data Leaders",
           "sidebar_title": "⚙️ Configuration",
           "sidebar_lang": "🌍 Language",
           "sidebar_excel": "📊 Upload Your Framework (Excel)",
           "sidebar_ai": "🤖 AI Agent (optional)",
           "sidebar_model": "AI Model",
           "sidebar_hint": "💡 No API key? A heuristic report will be generated.",
           "sidebar_sql_toggle": "🗄️ Include SQL module",
           "sidebar_sql_vendor": "SQL Stack",
           "kpi_score": "Global Score",
           "kpi_domains": "Domains",
           "kpi_priorities": "Priorities",
           "kpi_savings": "Days saved/year",
           "section_assessment": "🧩 Interactive Self-Assessment",
           "section_radar": "📊 Maturity Radar",
           "section_prio": "🎯 Prioritization",
           "section_report": "📝 Executive Report",
           "section_roi": "💰 ROI Calculator",
           "section_linkedin": "🔗 Viral LinkedIn Post",
           "timeline_title": "🗓️ AI Roadmap",
           "timeline_90d": "🚀 90 Days – Quick Wins",
           "timeline_6m": "📈 6 Months – Foundation",
           "timeline_12m": "🎯 12 Months – Transformation",
           "download_report": "📥 Download Report (Markdown)",
           "download_pdf": "🖨️ Export PDF"}
}
T = LANGS[st.session_state.current_lang]

# =========================
# HERO
# =========================
st.markdown(f"""
<div style="
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
padding: 60px; border-radius: 16px; text-align: center; color: white;">
  <div style="font-size:52px;font-weight:900;">{T['hero_title']}</div>
  <div style="font-size:22px;font-weight:700;">{T['hero_subtitle']}</div>
  <div style="font-size:16px;margin-top:12px;opacity:0.92;">{T['hero_tagline']}</div>
  <div style="font-size:14px;margin-top:14px;opacity:0.9;">✨ {T['hero_stats']}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"### {T['sidebar_title']}")
    new_lang = st.selectbox(
        T["sidebar_lang"], ["fr", "en"],
        index=(0 if st.session_state.current_lang == "fr" else 1),
        key="lang_select"
    )
    if new_lang != st.session_state.current_lang:
        st.session_state.current_lang = new_lang
        try:
            st.query_params["lang"] = new_lang
        except Exception:
            pass
        st.rerun()

    excel_file = st.file_uploader(T['sidebar_excel'], type=["xlsx"], key="xls_upl")
    include_sql = st.toggle(T["sidebar_sql_toggle"], value=True, key="sql_toggle")
    sql_vendor = st.selectbox(T["sidebar_sql_vendor"], ["Postgres","BigQuery","Snowflake"], key="sql_vendor")

    st.markdown("---")
    use_ai = st.toggle(T['sidebar_ai'], value=False, key="ai_toggle")
    if use_ai:
        model_name = st.text_input(T['sidebar_model'], value="gpt-4o-mini", key="ai_model")
    st.caption(T['sidebar_hint'])

# =========================
# Framework de base
# =========================
DEFAULT_DATA = pd.DataFrame({
    "domain": ["Data Strategy","Data Governance","Data Quality","Data Architecture","Data Security"],
    "question": [
        "Alignment between data vision and business goals",
        "Structured governance and clear ownership",
        "Automated quality monitoring and controls",
        "Modern scalable cloud architecture",
        "Security and compliance proactively managed"
    ],
    "weight": [1.2,1.0,1.1,0.9,1.3],
})

df_questions = DEFAULT_DATA.copy()
answers = {}

st.markdown(f"## {T['section_assessment']}")
for i, row in df_questions.iterrows():
    with st.expander(f"{row['domain']} — {row['question']}"):
        cols = st.columns(5)
        for j, c in enumerate(cols,1):
            if c.button(f"✓ {j}", key=f"btn_{i}_{j}"):
                st.session_state[f"lvl_{i}"]=j
        lvl=st.session_state.get(f"lvl_{i}",3)
        answers[i]={"domain":row["domain"],"level":lvl,"weight":row["weight"]}

df_answers=pd.DataFrame(answers).T
def calc_score(g): return float(np.average((g["level"]-1)/4*100,weights=g["weight"]))
domain_scores=df_answers.groupby("domain",group_keys=False).apply(calc_score).to_dict() if not df_answers.empty else {}
global_score=np.mean(list(domain_scores.values())) if domain_scores else 0

# KPI
k1,k2,k3=st.columns(3)
k1.metric(T["kpi_score"],f"{global_score:.1f}")
k2.metric(T["kpi_domains"],len(domain_scores))
k3.metric(T["kpi_savings"],f"{int(global_score*0.7)}")

# Radar
if domain_scores:
    fig=go.Figure()
    doms=list(domain_scores.keys()); vals=list(domain_scores.values())
    fig.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=doms+[doms[0]],fill='toself',
                    fillcolor='rgba(102,126,234,0.35)',line=dict(color='#667eea')))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0,100])),showlegend=False)
    st.plotly_chart(fig,use_container_width=True)

# =============== IA Summary ===============
summary_text, roadmap_text=None,None
if use_ai:
    client,err=get_openai_client()
    if err: st.warning(err)
    else:
        try:
            prompt=f"""Give a concise executive summary (max 10 lines) about this maturity assessment:
            Global score: {global_score:.1f}/100
            Domain scores: {domain_scores}
            Provide 3 strengths and 3 improvements."""
            resp=client.chat.completions.create(model=model_name,temperature=0.4,
                messages=[{"role":"user","content":prompt}])
            summary_text=resp.choices[0].message.content.strip()
            st.success("✅ IA activée — synthèse générée.")
            st.write(summary_text)
        except Exception as e:
            st.error(f"OpenAI error: {e}")

# =============== Rapport Markdown ===============
report_md=f"""# Maturity Assessment Report — {datetime.now().strftime('%Y-%m-%d')}

## Global Score
**{global_score:.1f}/100**

### Breakdown
{chr(10).join([f'- {d}: {s:.1f}' for d,s in domain_scores.items()])}

---

## Executive Summary
{summary_text or '—'}
"""

st.download_button(
    T["download_report"],
    data=report_md.encode("utf-8"),
    file_name=f"maturity_report_{datetime.now().strftime('%Y%m%d')}.md",
    mime="text/markdown"
)

def md_to_html(md):
    esc=(md.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))
    return f"<html><body><pre>{esc}</pre></body></html>"

if st.button(T["download_pdf"]):
    pdf=try_export_pdf(md_to_html(report_md))
    if pdf:
        st.download_button(
            "⬇️ PDF Ready — Click to Download",
            data=pdf,
            file_name=f"maturity_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("PDF engine missing. Install weasyprint or pdfkit.")

st.markdown("---")
st.caption("© 2025 MaturityAgent PRO • MIT License")
