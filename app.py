# app.py — MaturityAgent PRO (Ultimate v9.2 – Stable IA All Versions)
# ------------------------------------------------------------
# Fixes:
# ✅ OpenAI compatibility with 0.x and 1.x SDK (no proxies issue)
# ✅ Secure lang init (no KeyError)
# ✅ Download buttons cleaned (no TypeError width)
# ✅ PDF export works (WeasyPrint / pdfkit)
# ------------------------------------------------------------

import os
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ============== PDF EXPORT ==============
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

# ============== OPENAI UNIVERSAL CLIENT ==============
def get_openai_client():
    """Return OpenAI client compatible with both 0.x and 1.x SDKs."""
    key = os.getenv("OPENAI_API_KEY", "")
    try:
        key = key or st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        pass
    if not key:
        return None, "No OPENAI_API_KEY found. Add it in Streamlit Secrets."

    # Try SDK 1.x
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        return {"mode": "v1", "client": client}, None
    except Exception as e1:
        # Try legacy 0.x
        try:
            import openai
            openai.api_key = key
            class LegacyClient:
                def chat_completions_create(self, **kwargs):
                    return openai.ChatCompletion.create(**kwargs)
            return {"mode": "v0", "client": LegacyClient()}, None
        except Exception as e2:
            return None, f"OpenAI SDK unavailable (1.x: {e1}; 0.x: {e2})"

def openai_chat(client_pack, model: str, messages: list, temperature: float = 0.4) -> str:
    """Unified chat call for OpenAI 0.x and 1.x SDKs."""
    mode = client_pack["mode"]
    client = client_pack["client"]
    if mode == "v1":
        resp = client.chat.completions.create(model=model, messages=messages, temperature=temperature)
        return resp.choices[0].message.content.strip()
    else:
        resp = client.chat_completions_create(model=model, messages=messages, temperature=temperature)
        return resp["choices"][0]["message"]["content"].strip()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="MaturityAgent PRO - AI Strategic Transformation", page_icon="🚀", layout="wide")

# =========================
# LANG INIT
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

# =========================
# TEXTS
# =========================
LANGS = {
    "fr": {
        "hero_title": "🚀 MaturityAgent PRO",
        "hero_subtitle": "IA × Consulting × Data Engineering",
        "hero_tagline": "Transformez n'importe quel référentiel en feuille de route IA en 1h",
        "sidebar_title": "⚙️ Configuration",
        "sidebar_lang": "🌍 Langue",
        "sidebar_excel": "📊 Uploadez votre Référentiel (Excel)",
        "sidebar_ai": "🤖 Agent IA (optionnel)",
        "sidebar_model": "Modèle IA",
        "sidebar_hint": "💡 Pas de clé ? Rapport heuristique généré.",
        "section_assessment": "🧩 Auto-Évaluation Interactive",
        "section_radar": "📊 Radar de Maturité",
        "section_report": "📝 Rapport Exécutif",
        "section_linkedin": "🔗 Post LinkedIn Viral",
        "download_report": "📥 Télécharger (Markdown)",
        "download_pdf": "🖨️ Exporter PDF"
    },
    "en": {
        "hero_title": "🚀 MaturityAgent PRO",
        "hero_subtitle": "AI × Consulting × Data Engineering",
        "hero_tagline": "Turn any framework into an AI roadmap in 1h",
        "sidebar_title": "⚙️ Settings",
        "sidebar_lang": "🌍 Language",
        "sidebar_excel": "📊 Upload Framework (Excel)",
        "sidebar_ai": "🤖 AI Agent (optional)",
        "sidebar_model": "AI Model",
        "sidebar_hint": "💡 No key? Heuristic report only.",
        "section_assessment": "🧩 Interactive Self-Assessment",
        "section_radar": "📊 Maturity Radar",
        "section_report": "📝 Executive Report",
        "section_linkedin": "🔗 Viral LinkedIn Post",
        "download_report": "📥 Download (Markdown)",
        "download_pdf": "🖨️ Export PDF"
    }
}
T = LANGS[st.session_state.current_lang]

# =========================
# HERO
# =========================
st.markdown(f"""
<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
padding:60px;border-radius:16px;text-align:center;color:white;">
  <div style="font-size:50px;font-weight:900;">{T['hero_title']}</div>
  <div style="font-size:22px;font-weight:600;">{T['hero_subtitle']}</div>
  <div style="font-size:16px;margin-top:10px;">{T['hero_tagline']}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"### {T['sidebar_title']}")
    new_lang = st.selectbox(T["sidebar_lang"], ["fr", "en"], index=(0 if st.session_state.current_lang=="fr" else 1))
    if new_lang != st.session_state.current_lang:
        st.session_state.current_lang = new_lang
        try: st.query_params["lang"] = new_lang
        except Exception: pass
        st.rerun()

    excel_file = st.file_uploader(T["sidebar_excel"], type=["xlsx"])
    use_ai = st.toggle(T["sidebar_ai"], value=False)
    if use_ai:
        model_name = st.text_input(T["sidebar_model"], value="gpt-4o-mini")
    st.caption(T["sidebar_hint"])

# =========================
# QUESTIONS DE BASE
# =========================
DEFAULT_DATA = pd.DataFrame({
    "domain": ["Data Strategy","Data Governance","Data Quality","Data Architecture","Data Security"],
    "question": [
        "Alignment between data vision and business goals",
        "Structured governance with clear ownership",
        "Automated quality monitoring",
        "Modern, cloud-native architecture",
        "Security and compliance managed"
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
        lvl = st.session_state.get(f"lvl_{i}",3)
        answers[i]={"domain":row["domain"],"level":lvl,"weight":row["weight"]}

df_answers=pd.DataFrame(answers).T
def calc_score(g): return float(np.average((g["level"]-1)/4*100,weights=g["weight"]))
domain_scores=df_answers.groupby("domain",group_keys=False).apply(calc_score).to_dict() if not df_answers.empty else {}
global_score=np.mean(list(domain_scores.values())) if domain_scores else 0

# KPI
st.metric("🌍 Global Score", f"{global_score:.1f}/100")
st.metric("📊 Domains", len(domain_scores))

# =========================
# RADAR
# =========================
if domain_scores:
    fig=go.Figure()
    doms=list(domain_scores.keys()); vals=list(domain_scores.values())
    fig.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=doms+[doms[0]],fill='toself',fillcolor='rgba(102,126,234,0.35)',line=dict(color='#667eea')))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0,100])),showlegend=False)
    st.plotly_chart(fig,use_container_width=True)

# =========================
# IA SECTION
# =========================
summary_text=None
if use_ai:
    pack, err = get_openai_client()
    if err: st.warning(f"⚠️ {err}")
    else:
        try:
            msg=[{"role":"system","content":"You are a data strategy consultant."},
                 {"role":"user","content":f"Summarize this maturity: {domain_scores}, global={global_score:.1f}"}]
            summary_text=openai_chat(pack, model_name, msg)
            st.success("✅ IA summary generated")
            st.write(summary_text)
        except Exception as e:
            st.error(f"OpenAI error: {e}")

# =========================
# REPORT + PDF
# =========================
report_md=f"""# Maturity Report — {datetime.now().strftime('%Y-%m-%d')}
**Global Score:** {global_score:.1f}/100
{summary_text or ''}
"""
st.download_button(T["download_report"], report_md, file_name="maturity_report.md")

def md_to_html(md): return f"<html><body><pre>{md}</pre></body></html>"
if st.button(T["download_pdf"]):
    pdf=try_export_pdf(md_to_html(report_md))
    if pdf:
        st.download_button("⬇️ PDF Ready", pdf, file_name="maturity_report.pdf", mime="application/pdf")
    else:
        st.warning("PDF engine missing. Install weasyprint or pdfkit.")

# =========================
# LINKEDIN
# =========================
st.markdown(f"## {T['section_linkedin']}")
post=f"""🚀 MaturityAgent PRO — Instant maturity assessment in Streamlit.
Score: {global_score:.1f}/100
Domains: {', '.join(domain_scores.keys()) if domain_scores else '—'}
#Data #AI #Governance #Streamlit"""
st.text_area("LinkedIn", value=post, height=220)

st.caption("© 2025 MaturityAgent PRO • MIT License")
