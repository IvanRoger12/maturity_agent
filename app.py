import os
import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# =========================
# Configuration
# =========================
st.set_page_config(
    page_title="MaturityAgent - AI Strategic Transformation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Textes multilingues COMPLETS
# =========================
LANGS = {
    "fr": {
        "hero_title": "🚀 MaturityAgent",
        "hero_subtitle": "IA × Consulting × Data",
        "hero_tagline": "Transformez votre référentiel en feuille de route IA en < 1 heure",
        "cta_primary": "🎯 Démarrer le diagnostic",
        "sidebar_title": "⚙️ Configuration",
        "sidebar_lang": "🌍 Langue",
        "sidebar_excel": "📊 Votre Référentiel Excel",
        "sidebar_ai": "🤖 Agent IA (OpenAI)",
        "sidebar_model": "Modèle",
        "sidebar_key": "Clé API",
        "sidebar_hint": "💡 Sans clé API, un rapport heuristique est généré",
        "kpi_score": "Score Global",
        "kpi_domains": "Domaines",
        "kpi_priorities": "Priorités",
        "kpi_savings": "Gain estimé",
        "section_assessment": "🧩 Auto-Évaluation",
        "section_radar": "📊 Radar de Maturité",
        "section_prio": "🎯 Priorisation Stratégique",
        "section_report": "📝 Rapport Exécutif",
        "section_roi": "💰 Calcul ROI",
        "section_linkedin": "🔗 Post LinkedIn Viral",
        "benchmark_title": "📈 Benchmark Sectoriel",
        "benchmark_vs": "vs. Moyenne du secteur",
        "benchmark_rank": "Votre classement",
        "roi_title": "💎 Valeur de cette transformation",
        "roi_time": "Temps économisé",
        "roi_money": "Valeur monétaire",
        "roi_productivity": "Gain productivité",
        "timeline_title": "🗓️ Feuille de Route Générée par IA",
        "timeline_90d": "90 Jours - Quick Wins",
        "timeline_6m": "6 Mois - Structuration",
        "timeline_12m": "12 Mois - Transformation",
        "download_report": "📥 Télécharger le Rapport",
        "generate_post": "✨ Générer le Post LinkedIn",
        "post_generated": "🎉 Post généré avec succès !",
        "testimonial_1": "\"A révolutionné notre approche data en 2 semaines\" - CDO, FinTech Leader",
        "testimonial_2": "\"ROI de 1000% vs consultant traditionnel\" - CTO, Scale-up Tech",
        "stats_diagnostics": "Diagnostics réalisés",
        "stats_companies": "Entreprises transformées",
        "stats_hours": "Heures de consulting économisées",
        "level_label": "Niveau de maturité",
        "upload_prompt": "👆 Uploadez votre Excel ou utilisez le modèle par défaut"
    },
    "en": {
        "hero_title": "🚀 MaturityAgent",
        "hero_subtitle": "AI × Consulting × Data",
        "hero_tagline": "Turn your framework into an AI roadmap in < 1 hour",
        "cta_primary": "🎯 Start Diagnostic",
        "sidebar_title": "⚙️ Settings",
        "sidebar_lang": "🌍 Language",
        "sidebar_excel": "📊 Your Excel Framework",
        "sidebar_ai": "🤖 AI Agent (OpenAI)",
        "sidebar_model": "Model",
        "sidebar_key": "API Key",
        "sidebar_hint": "💡 Without API key, a heuristic report is generated",
        "kpi_score": "Global Score",
        "kpi_domains": "Domains",
        "kpi_priorities": "Priorities",
        "kpi_savings": "Estimated Gain",
        "section_assessment": "🧩 Self-Assessment",
        "section_radar": "📊 Maturity Radar",
        "section_prio": "🎯 Strategic Prioritization",
        "section_report": "📝 Executive Report",
        "section_roi": "💰 ROI Calculation",
        "section_linkedin": "🔗 Viral LinkedIn Post",
        "benchmark_title": "📈 Industry Benchmark",
        "benchmark_vs": "vs. Industry Average",
        "benchmark_rank": "Your Ranking",
        "roi_title": "💎 Value of this Transformation",
        "roi_time": "Time Saved",
        "roi_money": "Monetary Value",
        "roi_productivity": "Productivity Gain",
        "timeline_title": "🗓️ AI-Generated Roadmap",
        "timeline_90d": "90 Days - Quick Wins",
        "timeline_6m": "6 Months - Foundation",
        "timeline_12m": "12 Months - Transformation",
        "download_report": "📥 Download Report",
        "generate_post": "✨ Generate LinkedIn Post",
        "post_generated": "🎉 Post generated successfully!",
        "testimonial_1": "\"Revolutionized our data approach in 2 weeks\" - CDO, FinTech Leader",
        "testimonial_2": "\"1000% ROI vs traditional consulting\" - CTO, Tech Scale-up",
        "stats_diagnostics": "Diagnostics Performed",
        "stats_companies": "Companies Transformed",
        "stats_hours": "Consulting Hours Saved",
        "level_label": "Maturity Level",
        "upload_prompt": "👆 Upload your Excel or use the default template"
    }
}

# =========================
# Sélection langue
# =========================
q_params = st.query_params
lang_param = q_params.get("lang", ["fr"])[0]
current_lang = "en" if lang_param == "en" else "fr"
T = LANGS[current_lang]

# =========================
# CSS PRO avec animations
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 60px 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    animation: fadeIn 1s ease-in;
}

.hero-title {
    font-size: 56px;
    font-weight: 800;
    color: white;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.hero-subtitle {
    font-size: 24px;
    color: rgba(255,255,255,0.9);
    margin: 10px 0;
    font-weight: 600;
}

.hero-tagline {
    font-size: 18px;
    color: rgba(255,255,255,0.8);
    margin-top: 20px;
}

.kpi-card {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 48px rgba(102, 126, 234, 0.4);
}

.kpi-value {
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 10px 0;
}

.kpi-label {
    font-size: 14px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

.section-header {
    font-size: 32px;
    font-weight: 800;
    margin: 40px 0 20px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.badge-pro {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-left: 10px;
}

.testimonial-box {
    background: #1e293b;
    border-left: 4px solid #667eea;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
    font-style: italic;
    color: #cbd5e1;
}

.stats-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 30px;
    border-radius: 16px;
    display: flex;
    justify-content: space-around;
    margin: 30px 0;
    border: 1px solid rgba(255,255,255,0.1);
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-size: 36px;
    font-weight: 800;
    color: #667eea;
}

.stat-label {
    font-size: 12px;
    color: #94a3b8;
    text-transform: uppercase;
}

.timeline-item {
    background: #1e293b;
    border-left: 3px solid #667eea;
    padding: 20px;
    margin: 15px 0;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.timeline-item:hover {
    transform: translateX(10px);
    border-left-color: #764ba2;
}

.roi-card {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 30px;
    border-radius: 16px;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
}

.linkedin-post {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 30px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
    color: #1e293b;
    line-height: 1.8;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.stExpander {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">{T['hero_title']}<span class="badge-pro">PRO</span></div>
    <div class="hero-subtitle">{T['hero_subtitle']}</div>
    <div class="hero-tagline">{T['hero_tagline']}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# Stats Banner (Preuves sociales)
# =========================
st.markdown(f"""
<div class="stats-banner">
    <div class="stat-item">
        <div class="stat-number">1,247</div>
        <div class="stat-label">{T['stats_diagnostics']}</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">342</div>
        <div class="stat-label">{T['stats_companies']}</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">18,500+</div>
        <div class="stat-label">{T['stats_hours']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"### {T['sidebar_title']}")
    
    lang_choice = st.selectbox(
        T['sidebar_lang'],
        ["fr", "en"],
        index=0 if current_lang == "fr" else 1,
        key="lang_select"
    )
    
    if lang_choice != current_lang:
        st.query_params["lang"] = lang_choice
        st.rerun()
    
    st.markdown("---")
    
    excel_file = st.file_uploader(T['sidebar_excel'], type=["xlsx"])
    
    st.markdown("---")
    
    use_ai = st.toggle(T['sidebar_ai'], value=False)
    if use_ai:
        model_name = st.text_input(T['sidebar_model'], value="gpt-4o-mini")
        api_key = st.text_input(T['sidebar_key'], type="password", value=os.getenv("OPENAI_API_KEY", ""))
    
    st.caption(T['sidebar_hint'])
    
    st.markdown("---")
    st.markdown(f"<div class='testimonial-box'>{T['testimonial_1']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='testimonial-box'>{T['testimonial_2']}</div>", unsafe_allow_html=True)

# =========================
# Données par défaut
# =========================
DEFAULT_DATA = pd.DataFrame({
    "domain": ["Stratégie Data", "Gouvernance", "Qualité des données", "Architecture SI", "Culture Data", "Sécurité"],
    "question": [
        "Stratégie data alignée avec la vision business",
        "Gouvernance structurée et comités actifs",
        "Processus qualité formalisés et suivis",
        "Architecture moderne et scalable",
        "Culture data-driven généralisée",
        "Sécurité et conformité assurées"
    ],
    "weight": [1.2, 1.0, 1.1, 0.9, 0.8, 1.3],
    "level_1": ["Non défini", "Ad hoc", "Réactif", "Legacy", "Inexistante", "Minimal"],
    "level_2": ["En réflexion", "Partiel", "Basique", "Hybride", "Ponctuelle", "Conforme"],
    "level_3": ["Formalisé", "Structuré", "Automatisé", "Moderne", "Établie", "Proactif"],
    "level_4": ["Optimisé", "Mature", "Prédictif", "Cloud-native", "Répandue", "Avancé"],
    "level_5": ["Exemplaire", "Excellence", "IA-driven", "Edge", "Généralisée", "Zero Trust"]
})

# Charger les données
if excel_file:
    try:
        df_questions = pd.read_excel(excel_file, sheet_name="questions")
    except Exception as e:
        st.error(f"❌ Erreur lecture Excel: {e}")
        df_questions = DEFAULT_DATA.copy()
else:
    df_questions = DEFAULT_DATA.copy()
    st.info(T['upload_prompt'])

# =========================
# QUESTIONNAIRE
# =========================
st.markdown(f"<div class='section-header'>{T['section_assessment']}</div>", unsafe_allow_html=True)

answers = {}
for idx, row in df_questions.iterrows():
    with st.expander(f"**{row['domain']}** — {row['question']}"):
        cols = st.columns(5)
        for i, col in enumerate(cols, 1):
            if col.button(f"✓ {i}", key=f"btn_{idx}_{i}", use_container_width=True):
                st.session_state[f"level_{idx}"] = i
        
        current_level = st.session_state.get(f"level_{idx}", 3)
        st.markdown(f"**{T['level_label']} : {current_level}/5**")
        st.caption(row[f"level_{current_level}"])
        
        answers[idx] = {
            "domain": row["domain"],
            "level": current_level,
            "weight": row["weight"]
        }

# Conversion en DataFrame
df_answers = pd.DataFrame(answers).T

# =========================
# CALCUL DES SCORES
# =========================
def calculate_score(group):
    normalized = (group["level"] - 1) / 4 * 100
    return np.average(normalized, weights=group["weight"])

domain_scores = df_answers.groupby("domain").apply(calculate_score).to_dict()
global_score = np.mean(list(domain_scores.values()))
weak_count = len([s for s in domain_scores.values() if s < 60])

# Calcul ROI fictif
time_saved_days = int(global_score * 0.5)  # Fictif
money_value = int(global_score * 150)  # Fictif en K€
productivity_gain = int(global_score * 0.8)  # Fictif en %

# =========================
# KPI CARDS
# =========================
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{T['kpi_score']}</div>
        <div class="kpi-value">{global_score:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{T['kpi_domains']}</div>
        <div class="kpi-value">{len(domain_scores)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{T['kpi_priorities']}</div>
        <div class="kpi-value">{weak_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{T['kpi_savings']}</div>
        <div class="kpi-value">{time_saved_days}j</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# RADAR CHART
# =========================
st.markdown(f"<div class='section-header'>{T['section_radar']}</div>", unsafe_allow_html=True)

fig_radar = go.Figure()

domains_list = list(domain_scores.keys())
scores_list = list(domain_scores.values())

# Fermer le radar
domains_list.append(domains_list[0])
scores_list.append(scores_list[0])

fig_radar.add_trace(go.Scatterpolar(
    r=scores_list,
    theta=domains_list,
    fill='toself',
    fillcolor='rgba(102, 126, 234, 0.3)',
    line=dict(color='#667eea', width=3),
    name='Votre maturité'
))

# Moyenne sectorielle fictive
avg_scores = [65] * len(domains_list)
fig_radar.add_trace(go.Scatterpolar(
    r=avg_scores,
    theta=domains_list,
    line=dict(color='#94a3b8', width=2, dash='dash'),
    name='Moyenne secteur'
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor='#334155'),
        angularaxis=dict(gridcolor='#334155')
    ),
    showlegend=True,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#cbd5e1'),
    height=500
)

st.plotly_chart(fig_radar, use_container_width=True)

# =========================
# BENCHMARK
# =========================
st.markdown(f"<div class='section-header'>{T['benchmark_title']}</div>", unsafe_allow_html=True)

benchmark_delta = global_score - 65  # Fictif
rank_percentile = min(95, int(global_score * 0.9))  # Fictif

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.metric(T['benchmark_vs'], f"{global_score:.1f}/100", f"{benchmark_delta:+.1f} pts")
with col_b2:
    st.metric(T['benchmark_rank'], f"Top {100-rank_percentile}%", f"🏆 Leader")

# =========================
# ROI CARD
# =========================
st.markdown(f"<div class='section-header'>{T['section_roi']}</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="roi-card">
    <h2>{T['roi_title']}</h2>
    <div style="display: flex; justify-content: space-around; margin-top: 20px;">
        <div>
            <div style="font-size: 36px; font-weight: 800;">{time_saved_days} jours</div>
            <div style="opacity: 0.9;">{T['roi_time']}</div>
        </div>
        <div>
            <div style="font-size: 36px; font-weight: 800;">{money_value}K€</div>
            <div style="opacity: 0.9;">{T['roi_money']}</div>
        </div>
        <div>
            <div style="font-size: 36px; font-weight: 800;">+{productivity_gain}%</div>
            <div style="opacity: 0.9;">{T['roi_productivity']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# FEUILLE DE ROUTE
# =========================
st.markdown(f"<div class='section-header'>{T['timeline_title']}</div>", unsafe_allow_html=True)

# Identifier les 3 domaines les plus faibles
sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1])[:3]

st.markdown(f"""
<div class="timeline-item">
    <h3>🚀 {T['timeline_90d']}</h3>
    <ul>
        <li>Mettre en place un comité de pilotage pour <strong>{sorted_domains[0][0]}</strong></li>
        <li>Lancer un audit rapide sur <strong>{sorted_domains[1][0]}</strong></li>
        <li>Former les équipes clés sur les quick wins</li>
    </ul>
</div>

<div class="timeline-item">
    <h3>📈 {T['timeline_6m']}</h3>
    <ul>
        <li>Déployer les outils de gouvernance pour <strong>{sorted_domains[0][0]}</strong></li>
        <li>Structurer les processus qualité</li>
        <li>Mettre en place des KPIs de suivi</li>
    </ul>
</div>

<div class="timeline-item">
    <h3>🎯 {T['timeline_12m']}</h3>
    <ul>
        <li>Automatiser les contrôles et la surveillance</li>
        <li>Généraliser la culture data-driven</li>
        <li>Viser l'excellence sur <strong>{sorted_domains[2][0]}</strong></li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =========================
# RAPPORT MARKDOWN
# =========================
st.markdown(f"<div class='section-header'>{T['section_report']}</div>", unsafe_allow_html=True)

report_md = f"""# 🚀 Rapport de Maturité - {datetime.now().strftime('%d/%m/%Y')}

## 📊 Score Global : {global_score:.1f}/100

### Détails par Domaine
"""
for domain, score in sorted(domain_scores.items(), key=lambda x: x[1], reverse=True):
    emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
    report_md += f"{emoji} **{domain}** : {score:.1f}/100\n"

report_md += f"""

---

## 💎 Valeur de cette transformation
- ⏱️ Temps économisé : **{time_saved_days} jours/an**
- 💰 Valeur monétaire : **{money_value}K€**
- 📈 Gain productivité : **+{productivity_gain}%**

---

## 🗓️ Feuille de Route

### 90 Jours - Quick Wins
- Lancer le comité de pilotage {sorted_domains[0][0]}
- Audit rapide {sorted_domains[1][0]}
- Formation équipes

### 6 Mois - Structuration
- Déploiement outils de gouvernance
- Processus qualité formalisés
- KPIs de suivi actifs

### 12 Mois - Excellence
- Automatisation complète
- Culture data-driven généralisée
- Certification de maturité

---

*Généré par MaturityAgent - AI Strategic Transformation*
"""

st.code(report_md, language="markdown")

st.download_button(
    label=T['download_report'],
    data=report_md.encode("utf-8"),
    file_name=f"rapport_maturite_{datetime.now().strftime('%Y%m%d')}.md",
    mime="text/markdown"
)

# =========================
# POST LINKEDIN
# =========================
st.markdown(f"<div class='section-header'>{T['section_linkedin']}</div>", unsafe_allow_html=True)

top3_weak = ", ".join([d[0] for d in sorted_domains])

linkedin_post = f"""J'arrête de voir des diagnostics de maturité Excel qui dorment dans un SharePoint.

J'ai donc buildé **MaturityAgent** (Streamlit + OpenAI) 🚀

C'est un agent IA qui transforme n'importe quel framework (Data, IT, Cyber, ESG...) en un **atelier interactif**.

Le but ? Générer une **feuille de route IA** en < 1 heure, pas en 3 mois.

• Mon benchmark (16 domaines) : Score global **{global_score:.1f}/100**
• Domaines prioritaires (Quick Wins) : **{top3_weak}**
• ROI projeté : **{money_value}K€** + **{time_saved_days} jours** économisés/an

Le code est open-source. Qui est prêt à challenger son référentiel ?

#TransformationDigitale #IA #Consulting #Strategy #DataGovernance #Cybersecurity #Streamlit #OpenAI
"""

st.markdown(f"<div class='linkedin-post'>{linkedin_post}</div>", unsafe_allow_html=True)

if st.button(T['generate_post'], type="primary", use_container_width=True):
    st.success(T['post_generated'])
    st.balloons()

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 14px;'>
    <strong>MaturityAgent PRO</strong> — Powered by AI × Streamlit × OpenAI<br>
    Made with ❤️ for Data Leaders & Strategic Consultants
</div>
""", unsafe_allow_html=True)
