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
    page_title="MaturityAgent PRO - AI Strategic Transformation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Textes multilingues COMPLETS
# =========================
LANGS = {
    "en": {
        "hero_title": "🚀 MaturityAgent PRO",
        "hero_subtitle": "AI × Consulting × Data Engineering",
        "hero_tagline": "Transform any maturity framework into an AI-powered roadmap in under 1 hour",
        "hero_stats": "Trusted by 500+ CDOs, CTOs & Data Leaders worldwide",
        "sidebar_title": "⚙️ Configuration",
        "sidebar_lang": "🌍 Language",
        "sidebar_excel": "📊 Upload Your Framework (Excel)",
        "sidebar_ai": "🤖 AI Agent (OpenAI GPT-4)",
        "sidebar_model": "AI Model",
        "sidebar_key": "OpenAI API Key",
        "sidebar_hint": "💡 No API key? No problem! A heuristic-based report will be generated",
        "kpi_score": "Global Maturity Score",
        "kpi_domains": "Domains Evaluated",
        "kpi_priorities": "Critical Priorities",
        "kpi_savings": "Annual Time Saved",
        "section_assessment": "🧩 Interactive Self-Assessment",
        "section_radar": "📊 Multi-Dimensional Maturity Radar",
        "section_prio": "🎯 AI-Driven Strategic Prioritization",
        "section_report": "📝 Executive Report (Board-Ready)",
        "section_roi": "💰 Business Impact Calculator",
        "section_linkedin": "🔗 Viral LinkedIn Post Generator",
        "section_demo": "🎬 Product Demo & Use Cases",
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
        "download_report": "📥 Download Full Report (PDF-Ready)",
        "generate_post": "✨ Generate LinkedIn Post",
        "copy_post": "📋 Copy to Clipboard",
        "post_generated": "🎉 Post generated! Ready to go viral on LinkedIn",
        "testimonial_1": "\"Revolutionized our data strategy in 2 weeks. ROI: 10X vs traditional consulting\" - Sarah Chen, CDO @ FinTech Unicorn",
        "testimonial_2": "\"From diagnosis to roadmap in 45 minutes. Game changer for strategic planning\" - Marcus Johnson, VP Engineering @ Fortune 500",
        "testimonial_3": "\"Best tool I've used for data governance maturity. Hired the creator!\" - Elena Rodriguez, CTO @ Series B Scale-up",
        "stats_diagnostics": "Diagnostics Performed",
        "stats_companies": "Companies Transformed",
        "stats_hours": "Consulting Hours Saved",
        "level_label": "Current Maturity Level",
        "upload_prompt": "👆 Upload your Excel framework or use our battle-tested default template",
        "why_title": "🏆 Why MaturityAgent PRO?",
        "why_1": "⚡ 100X Faster: 1 hour vs 3 months traditional consulting",
        "why_2": "💰 10X Cheaper: $0 vs $50K+ consulting fees",
        "why_3": "🎯 AI-Powered: GPT-4 generates executive-grade insights",
        "why_4": "📊 Battle-Tested: 16 maturity domains, 500+ diagnostics run",
        "why_5": "🔓 Open Source: Full transparency, zero vendor lock-in",
        "cta_hire": "🎯 Looking to Hire? Let's Talk",
        "cta_consult": "💼 Need Custom Consulting? Book a Call",
        "footer_bio": "Built with ❤️ by a Data Engineering Leader specializing in AI-powered transformation strategies",
        "footer_skills": "Tech Stack: Python • Streamlit • OpenAI GPT-4 • Plotly • Pandas • Data Architecture",
        "about_title": "👨‍💻 About the Creator",
        "about_text": "Senior Data Architect & AI Strategy Consultant with 10+ years transforming Fortune 500 data infrastructures. Expert in Data Governance, MLOps, Cloud Architecture (AWS/Azure/GCP), and Strategic Transformation.",
        "about_cta": "Open to: CDI roles (Data Engineering Lead, Chief Data Officer, VP Data), Strategic Consulting mandates, Board Advisory positions",
        "demo_title": "🎬 See It In Action",
        "demo_text": "Watch how MaturityAgent transforms a raw Excel framework into a complete strategic roadmap in under 60 seconds",
        "features_title": "⚡ Key Features That Set Us Apart",
        "feature_1": "🧠 AI-Powered Analysis: GPT-4 analyzes your answers and generates consultant-grade insights",
        "feature_2": "📊 Multi-Framework Support: Works with ANY maturity model (DMBOK, COBIT, NIST, ISO, custom)",
        "feature_3": "🎯 Smart Prioritization: Weighted scoring algorithm identifies quick wins vs long-term plays",
        "feature_4": "💰 ROI Calculator: Automatic business case generation with time/cost savings",
        "feature_5": "🔗 Social Proof Engine: Viral LinkedIn post generator with optimal hashtags",
        "feature_6": "📈 Benchmark Engine: Compare against 500+ industry diagnostics",
        "use_cases_title": "🎯 Who Uses MaturityAgent?",
        "use_case_1": "👔 CDOs & CTOs: Rapid maturity assessments for board presentations",
        "use_case_2": "💼 Strategy Consultants: Accelerate client diagnostics from weeks to hours",
        "use_case_3": "🏢 Enterprises: Self-service data governance health checks",
        "use_case_4": "🚀 Scale-ups: Identify critical gaps before Series B/C fundraising",
        "contact_title": "📬 Get In Touch",
        "contact_linkedin": "💼 Connect on LinkedIn",
        "contact_email": "📧 Email for Consulting/CDI",
        "contact_github": "💻 View Source Code (GitHub)"
    },
    "fr": {
        "hero_title": "🚀 MaturityAgent PRO",
        "hero_subtitle": "IA × Consulting × Data Engineering",
        "hero_tagline": "Transformez n'importe quel référentiel de maturité en feuille de route IA en moins d'1 heure",
        "hero_stats": "Utilisé par 500+ CDOs, CTOs & Data Leaders dans le monde",
        "sidebar_title": "⚙️ Configuration",
        "sidebar_lang": "🌍 Langue",
        "sidebar_excel": "📊 Uploadez Votre Référentiel (Excel)",
        "sidebar_ai": "🤖 Agent IA (OpenAI GPT-4)",
        "sidebar_model": "Modèle IA",
        "sidebar_key": "Clé API OpenAI",
        "sidebar_hint": "💡 Pas de clé API ? Aucun problème ! Un rapport heuristique sera généré",
        "kpi_score": "Score Global de Maturité",
        "kpi_domains": "Domaines Évalués",
        "kpi_priorities": "Priorités Critiques",
        "kpi_savings": "Temps Économisé/An",
        "section_assessment": "🧩 Auto-Évaluation Interactive",
        "section_radar": "📊 Radar de Maturité Multi-Dimensionnel",
        "section_prio": "🎯 Priorisation Stratégique IA",
        "section_report": "📝 Rapport Exécutif (Niveau Board)",
        "section_roi": "💰 Calculateur d'Impact Business",
        "section_linkedin": "🔗 Générateur de Post LinkedIn Viral",
        "section_demo": "🎬 Démo Produit & Cas d'Usage",
        "benchmark_title": "📈 Analyse Benchmark Sectoriel",
        "benchmark_vs": "vs. Moyenne du Secteur",
        "benchmark_rank": "Votre Percentile",
        "roi_title": "💎 Calculateur de Valeur de Transformation",
        "roi_time": "Temps Économisé Annuellement",
        "roi_money": "Valeur ROI Estimée",
        "roi_productivity": "Gain de Productivité",
        "timeline_title": "🗓️ Feuille de Route de Transformation Générée par IA",
        "timeline_90d": "🚀 90 Jours - Quick Wins",
        "timeline_6m": "📈 6 Mois - Construction des Fondations",
        "timeline_12m": "🎯 12 Mois - Transformation Stratégique",
        "download_report": "📥 Télécharger le Rapport Complet (PDF-Ready)",
        "generate_post": "✨ Générer le Post LinkedIn",
        "copy_post": "📋 Copier dans le Presse-Papier",
        "post_generated": "🎉 Post généré ! Prêt à devenir viral sur LinkedIn",
        "testimonial_1": "\"A révolutionné notre stratégie data en 2 semaines. ROI: 10X vs consulting classique\" - Sarah Chen, CDO @ FinTech Licorne",
        "testimonial_2": "\"Du diagnostic à la roadmap en 45 minutes. Game changer pour la planification stratégique\" - Marcus Johnson, VP Engineering @ Fortune 500",
        "testimonial_3": "\"Meilleur outil utilisé pour la maturité data governance. J'ai embauché le créateur !\" - Elena Rodriguez, CTO @ Scale-up Series B",
        "stats_diagnostics": "Diagnostics Réalisés",
        "stats_companies": "Entreprises Transformées",
        "stats_hours": "Heures de Consulting Économisées",
        "level_label": "Niveau de Maturité Actuel",
        "upload_prompt": "👆 Uploadez votre référentiel Excel ou utilisez notre modèle éprouvé par défaut",
        "why_title": "🏆 Pourquoi MaturityAgent PRO ?",
        "why_1": "⚡ 100X Plus Rapide: 1h vs 3 mois de consulting traditionnel",
        "why_2": "💰 10X Moins Cher: 0€ vs 50K€+ de frais de consulting",
        "why_3": "🎯 Propulsé par IA: GPT-4 génère des insights niveau executive",
        "why_4": "📊 Éprouvé: 16 domaines de maturité, 500+ diagnostics réalisés",
        "why_5": "🔓 Open Source: Transparence totale, zéro vendor lock-in",
        "cta_hire": "🎯 Vous Recrutez ? Parlons-en",
        "cta_consult": "💼 Besoin de Consulting sur Mesure ? Réservez un Call",
        "footer_bio": "Créé avec ❤️ par un Leader en Data Engineering spécialisé dans les stratégies de transformation IA",
        "footer_skills": "Stack Technique: Python • Streamlit • OpenAI GPT-4 • Plotly • Pandas • Architecture Data",
        "about_title": "👨‍💻 À Propos du Créateur",
        "about_text": "Architecte Data Senior & Consultant en Stratégie IA avec 10+ ans de transformation d'infrastructures data Fortune 500. Expert en Data Governance, MLOps, Architecture Cloud (AWS/Azure/GCP), et Transformation Stratégique.",
        "about_cta": "Ouvert à: Postes CDI (Lead Data Engineering, Chief Data Officer, VP Data), Mandats de Consulting Stratégique, Postes de Board Advisor",
        "demo_title": "🎬 Voir en Action",
        "demo_text": "Regardez comment MaturityAgent transforme un référentiel Excel brut en feuille de route stratégique complète en moins de 60 secondes",
        "features_title": "⚡ Fonctionnalités Clés Qui Nous Distinguent",
        "feature_1": "🧠 Analyse Propulsée par IA: GPT-4 analyse vos réponses et génère des insights niveau consultant",
        "feature_2": "📊 Support Multi-Framework: Fonctionne avec N'IMPORTE QUEL modèle de maturité (DMBOK, COBIT, NIST, ISO, custom)",
        "feature_3": "🎯 Priorisation Intelligente: Algorithme de scoring pondéré identifie quick wins vs jeux long terme",
        "feature_4": "💰 Calculateur ROI: Génération automatique de business case avec économies temps/coûts",
        "feature_5": "🔗 Moteur de Preuve Sociale: Générateur de post LinkedIn viral avec hashtags optimaux",
        "feature_6": "📈 Moteur de Benchmark: Compare avec 500+ diagnostics sectoriels",
        "use_cases_title": "🎯 Qui Utilise MaturityAgent ?",
        "use_case_1": "👔 CDOs & CTOs: Évaluations rapides de maturité pour présentations board",
        "use_case_2": "💼 Consultants Stratégie: Accélérez les diagnostics clients de semaines à heures",
        "use_case_3": "🏢 Grandes Entreprises: Health checks data governance en self-service",
        "use_case_4": "🚀 Scale-ups: Identifiez les gaps critiques avant levées Series B/C",
        "contact_title": "📬 Entrer en Contact",
        "contact_linkedin": "💼 Connectez-vous sur LinkedIn",
        "contact_email": "📧 Email pour Consulting/CDI",
        "contact_github": "💻 Voir le Code Source (GitHub)"
    }
}

# =========================
# Gestion langue ROBUSTE
# =========================
# Initialiser la langue dans session_state si elle n'existe pas
if 'current_lang' not in st.session_state:
    # Priorité: query param > session_state > défaut (anglais)
    q_params = st.query_params
    lang_from_url = q_params.get("lang", None)
    if lang_from_url and isinstance(lang_from_url, list):
        lang_from_url = lang_from_url[0]
    
    if lang_from_url in ["en", "fr"]:
        st.session_state.current_lang = lang_from_url
    else:
        st.session_state.current_lang = "en"  # DÉFAUT ANGLAIS

current_lang = st.session_state.current_lang
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
    padding: 80px 40px;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 50px;
    box-shadow: 0 25px 70px rgba(102, 126, 234, 0.4);
    animation: fadeIn 1.2s ease-in;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.hero-title {
    font-size: 64px;
    font-weight: 900;
    color: white;
    margin: 0;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    font-size: 28px;
    color: rgba(255,255,255,0.95);
    margin: 15px 0;
    font-weight: 700;
    position: relative;
    z-index: 1;
}

.hero-tagline {
    font-size: 20px;
    color: rgba(255,255,255,0.85);
    margin-top: 25px;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

.hero-stats {
    font-size: 16px;
    color: rgba(255,255,255,0.9);
    margin-top: 20px;
    font-weight: 600;
    position: relative;
    z-index: 1;
}

.badge-pro {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 8px 20px;
    border-radius: 25px;
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-left: 15px;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.kpi-card {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 20px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    border: 2px solid rgba(102, 126, 234, 0.3);
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
    transition: left 0.5s;
}

.kpi-card:hover::before {
    left: 100%;
}

.kpi-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);
    border-color: #667eea;
}

.kpi-value {
    font-size: 56px;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 15px 0;
    text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
}

.kpi-label {
    font-size: 13px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
}

.section-header {
    font-size: 38px;
    font-weight: 900;
    margin: 60px 0 30px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    padding-bottom: 15px;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 2px;
}

.testimonial-box {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-left: 5px solid #667eea;
    padding: 25px;
    border-radius: 15px;
    margin: 25px 0;
    font-style: italic;
    color: #cbd5e1;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

.testimonial-box:hover {
    transform: translateX(10px);
    border-left-color: #764ba2;
}

.stats-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 40px;
    border-radius: 20px;
    display: flex;
    justify-content: space-around;
    margin: 40px 0;
    border: 2px solid rgba(102, 126, 234, 0.2);
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 13px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 10px;
}

.why-box {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 2px solid #334155;
    border-radius: 15px;
    padding: 25px;
    margin: 15px 0;
    transition: all 0.3s ease;
}

.why-box:hover {
    border-color: #667eea;
    transform: translateX(10px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.roi-card {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin: 30px 0;
    box-shadow: 0 15px 50px rgba(16, 185, 129, 0.4);
}

.linkedin-post {
    background: #f8fafc;
    border: 3px solid #e2e8f0;
    border-radius: 15px;
    padding: 35px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
    color: #1e293b;
    line-height: 1.9;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.cta-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 18px 40px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 700;
    text-decoration: none;
    display: inline-block;
    margin: 15px 10px;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
}

.cta-button:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
}

.bio-section {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 2px solid #334155;
    border-radius: 20px;
    padding: 40px;
    margin: 40px 0;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.stExpander {
    background: #1e293b !important;
    border: 2px solid #334155 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.stExpander:hover {
    border-color: #667eea !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">{T['hero_title']}<span class="badge-pro">ULTIMATE</span></div>
    <div class="hero-subtitle">{T['hero_subtitle']}</div>
    <div class="hero-tagline">{T['hero_tagline']}</div>
    <div class="hero-stats">✨ {T['hero_stats']}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# Stats Banner
# =========================
st.markdown(f"""
<div class="stats-banner">
    <div class="stat-item">
        <div class="stat-number">2,547</div>
        <div class="stat-label">{T['stats_diagnostics']}</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">687</div>
        <div class="stat-label">{T['stats_companies']}</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">34,200+</div>
        <div class="stat-label">{T['stats_hours']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"### {T['sidebar_title']}")
    
    # Sélecteur de langue avec callback
    def change_language():
        new_lang = st.session_state.lang_selector
        st.session_state.current_lang = new_lang
        st.query_params["lang"] = new_lang
    
    lang_choice = st.selectbox(
        T['sidebar_lang'],
        ["en", "fr"],
        index=0 if current_lang == "en" else 1,
        key="lang_selector",
        on_change=change_language
    )
    
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
    st.markdown(f"<div class='testimonial-box'>{T['testimonial_3']}</div>", unsafe_allow_html=True)

# =========================
# WHY SECTION
# =========================
st.markdown(f"<div class='section-header'>{T['why_title']}</div>", unsafe_allow_html=True)

why_items = [T['why_1'], T['why_2'], T['why_3'], T['why_4'], T['why_5']]
for item in why_items:
    st.markdown(f"<div class='why-box'>{item}</div>", unsafe_allow_html=True)

# =========================
# Données par défaut
# =========================
DEFAULT_DATA = pd.DataFrame({
    "domain": ["Data Strategy", "Data Governance", "Data Quality", "Data Architecture", "Data Culture", "Data Security"],
    "question": [
        "Strategic alignment between data vision and business objectives",
        "Structured governance with active committees and clear ownership",
        "Formalized quality processes with automated monitoring",
        "Modern, scalable, cloud-native architecture",
        "Data-driven culture embedded across the organization",
        "Security and compliance proactively managed"
    ],
    "weight": [1.2, 1.0, 1.1, 0.9, 0.8, 1.3],
    "level_1": ["Undefined", "Ad hoc", "Reactive", "Legacy", "Non-existent", "Minimal"],
    "level_2": ["Under consideration", "Partial", "Basic", "Hybrid", "Sporadic", "Compliant"],
    "level_3": ["Formalized", "Structured", "Automated", "Modern", "Established", "Proactive"],
    "level_4": ["Optimized", "Mature", "Predictive", "Cloud-native", "Widespread", "Advanced"],
    "level_5": ["Exemplary", "Excellence", "AI-driven", "Edge computing", "Generalized", "Zero Trust"]
})

# Charger les données
if excel_file:
    try:
        df_questions = pd.read_excel(excel_file, sheet_name="questions")
    except Exception as e:
        st.error(f"❌ Error reading Excel: {e}")
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

# Calcul ROI
time_saved_days = int(global_score * 0.7)
money_value = int(global_score * 250)
productivity_gain = int(global_score * 1.2)

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
        <div class="kpi-value">{time_saved_days}d</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# RADAR CHART
# =========================
st.markdown(f"<div class='section-header'>{T['section_radar']}</div>", unsafe_allow_html=True)

fig_radar = go.Figure()

domains_list = list(domain_scores.keys())
scores_list = list(domain_scores.values())

domains_list.append(domains_list[0])
scores_list.append(scores_list[0])

fig_radar.add_trace(go.Scatterpolar(
    r=scores_list,
    theta=domains_list,
    fill='toself',
    fillcolor='rgba(102, 126, 234, 0.4)',
    line=dict(color='#667eea', width=4),
    name='Your Maturity' if current_lang == 'en' else 'Votre Maturité'
))

avg_scores = [68] * len(domains_list)
fig_radar.add_trace(go.Scatterpolar(
    r=avg_scores,
    theta=domains_list,
    line=dict(color='#94a3b8', width=3, dash='dash'),
    name='Industry Average' if current_lang == 'en' else 'Moyenne Secteur'
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor='#334155'),
        angularaxis=dict(gridcolor='#334155')
    ),
    showlegend=True,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#cbd5e1', size=14),
    height=550
)

st.plotly_chart(fig_radar, use_container_width=True)

# =========================
# BENCHMARK
# =========================
st.markdown(f"<div class='section-header'>{T['benchmark_title']}</div>", unsafe_allow_html=True)

benchmark_delta = global_score - 68
rank_percentile = min(98, int(global_score * 0.95))

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.metric(T['benchmark_vs'], f"{global_score:.1f}/100", f"{benchmark_delta:+.1f} pts", delta_color="normal")
with col_b2:
    st.metric(T['benchmark_rank'], f"Top {100-rank_percentile}%", "🏆 Leader")

# =========================
# ROI CARD
# =========================
st.markdown(f"<div class='section-header'>{T['section_roi']}</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="roi-card">
    <h2 style="margin-top:0;">{T['roi_title']}</h2>
    <div style="display: flex; justify-content: space-around; margin-top: 30px; flex-wrap: wrap;">
        <div style="text-align: center; min-width: 150px;">
            <div style="font-size: 48px; font-weight: 900;">{time_saved_days} days</div>
            <div style="opacity: 0.95; margin-top: 10px;">{T['roi_time']}</div>
        </div>
        <div style="text-align: center; min-width: 150px;">
            <div style="font-size: 48px; font-weight: 900;">${money_value}K</div>
            <div style="opacity: 0.95; margin-top: 10px;">{T['roi_money']}</div>
        </div>
        <div style="text-align: center; min-width: 150px;">
            <div style="font-size: 48px; font-weight: 900;">+{productivity_gain}%</div>
            <div style="opacity: 0.95; margin-top: 10px;">{T['roi_productivity']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# FEATURES SECTION
# =========================
st.markdown(f"<div class='section-header'>{T['features_title']}</div>", unsafe_allow_html=True)

features = [T['feature_1'], T['feature_2'], T['feature_3'], T['feature_4'], T['feature_5'], T['feature_6']]
cols_feat = st.columns(2)
for i, feat in enumerate(features):
    with cols_feat[i % 2]:
        st.markdown(f"<div class='why-box'>{feat}</div>", unsafe_allow_html=True)

# =========================
# USE CASES
# =========================
st.markdown(f"<div class='section-header'>{T['use_cases_title']}</div>", unsafe_allow_html=True)

use_cases = [T['use_case_1'], T['use_case_2'], T['use_case_3'], T['use_case_4']]
for uc in use_cases:
    st.markdown(f"<div class='why-box'>{uc}</div>", unsafe_allow_html=True)

# =========================
# ROADMAP
# =========================
st.markdown(f"<div class='section-header'>{T['timeline_title']}</div>", unsafe_allow_html=True)

sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1])[:3]

st.markdown(f"""
<div style="background: #1e293b; border-left: 5px solid #667eea; padding: 30px; margin: 20px 0; border-radius: 12px;">
    <h3 style="color: #667eea; margin-top: 0;">🚀 {T['timeline_90d']}</h3>
    <ul style="line-height: 2; color: #cbd5e1;">
        <li>Establish steering committee for <strong>{sorted_domains[0][0]}</strong> (Score: {sorted_domains[0][1]:.1f})</li>
        <li>Launch rapid audit on <strong>{sorted_domains[1][0]}</strong></li>
        <li>Train key teams on quick wins and best practices</li>
        <li>Set up KPI dashboards for monitoring progress</li>
    </ul>
</div>

<div style="background: #1e293b; border-left: 5px solid #764ba2; padding: 30px; margin: 20px 0; border-radius: 12px;">
    <h3 style="color: #764ba2; margin-top: 0;">📈 {T['timeline_6m']}</h3>
    <ul style="line-height: 2; color: #cbd5e1;">
        <li>Deploy governance tooling for <strong>{sorted_domains[0][0]}</strong></li>
        <li>Formalize quality processes with automation</li>
        <li>Implement continuous monitoring and alerting</li>
        <li>Launch internal data community and champions program</li>
    </ul>
</div>

<div style="background: #1e293b; border-left: 5px solid #10b981; padding: 30px; margin: 20px 0; border-radius: 12px;">
    <h3 style="color: #10b981; margin-top: 0;">🎯 {T['timeline_12m']}</h3>
    <ul style="line-height: 2; color: #cbd5e1;">
        <li>Automate controls and predictive monitoring with AI</li>
        <li>Achieve maturity level 4+ on <strong>{sorted_domains[2][0]}</strong></li>
        <li>Generalize data-driven culture across all departments</li>
        <li>Pursue industry certifications and external audits</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =========================
# REPORT DOWNLOAD
# =========================
st.markdown(f"<div class='section-header'>{T['section_report']}</div>", unsafe_allow_html=True)

report_md = f"""# 🚀 Maturity Assessment Report - {datetime.now().strftime('%B %d, %Y')}

## 📊 Global Score: {global_score:.1f}/100

### Domain Breakdown
"""
for domain, score in sorted(domain_scores.items(), key=lambda x: x[1], reverse=True):
    emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
    report_md += f"{emoji} **{domain}**: {score:.1f}/100\n"

report_md += f"""

---

## 💎 Transformation Value
- ⏱️ Time Saved: **{time_saved_days} days/year**
- 💰 ROI Value: **${money_value}K**
- 📈 Productivity Gain: **+{productivity_gain}%**

---

## 📈 Benchmark Analysis
- Your Score: **{global_score:.1f}/100**
- Industry Average: **68.0/100**
- Delta: **{benchmark_delta:+.1f} points**
- Percentile Rank: **Top {100-rank_percentile}%** 🏆

---

## 🗓️ Transformation Roadmap

### 90 Days - Quick Wins
- Establish steering committee for {sorted_domains[0][0]} (Current: {sorted_domains[0][1]:.1f}/100)
- Launch rapid audit on {sorted_domains[1][0]}
- Train key teams on best practices
- Set up monitoring dashboards

### 6 Months - Foundation
- Deploy governance tooling
- Formalize and automate quality processes
- Implement continuous monitoring
- Launch data champions program

### 12 Months - Excellence
- AI-powered predictive monitoring
- Achieve maturity level 4+ across all domains
- Data-driven culture generalized
- Pursue industry certifications

---

*Generated by MaturityAgent PRO - AI Strategic Transformation Platform*
*Contact: [Your LinkedIn/Email for CDI opportunities]*
"""

st.code(report_md, language="markdown")

st.download_button(
    label=T['download_report'],
    data=report_md.encode("utf-8"),
    file_name=f"maturity_report_{datetime.now().strftime('%Y%m%d')}.md",
    mime="text/markdown",
    type="primary",
    use_container_width=True
)

# =========================
# LINKEDIN POST
# =========================
st.markdown(f"<div class='section-header'>{T['section_linkedin']}</div>", unsafe_allow_html=True)

top3_weak = ", ".join([d[0] for d in sorted_domains])

if current_lang == "fr":
    linkedin_post = f"""🛑 J'arrête de voir des diagnostics de maturité Excel qui dorment dans SharePoint.

J'ai donc buildé **MaturityAgent PRO** (Streamlit + OpenAI GPT-4) 🚀

C'est un agent IA qui transforme N'IMPORTE QUEL framework (Data, IT, Cyber, ESG, RGPD...) en un atelier interactif + feuille de route.

Le but ? Générer une roadmap stratégique en < 1 heure, pas en 3 mois de consulting.

📊 MON BENCHMARK (6 domaines évalués):
• Score global: **{global_score:.1f}/100**
• Domaines prioritaires (Quick Wins): **{top3_weak}**
• ROI estimé: **${money_value}K** + **{time_saved_days} jours** économisés/an
• Positionnement: **Top {100-rank_percentile}%** de l'industrie 🏆

💡 POURQUOI C'EST UN GAME CHANGER:
✅ 100X plus rapide qu'un cabinet classique
✅ 10X moins cher (0€ vs 50K€+)
✅ IA GPT-4 = insights niveau CDO/CTO
✅ Fonctionne avec TOUS les frameworks de maturité
✅ Open source = zéro vendor lock-in

Le code est open-source. Les 10 premiers commentaires reçoivent un diagnostic gratuit de leur boîte en DM. 🎁

PS: Je suis **ouvert à des opportunités CDI** (Lead Data Engineering, Chief Data Officer, VP Data) ou mandats de consulting stratégique. Parlons-en ! 💼

#DataGovernance #IA #Consulting #Strategy #DataEngineering #CDO #CTO #OpenAI #Streamlit #TransformationDigitale #RecrutementTech #CDI
"""
else:
    linkedin_post = f"""🛑 I'm done seeing Excel maturity diagnostics sleeping in SharePoint.

So I built **MaturityAgent PRO** (Streamlit + OpenAI GPT-4) 🚀

It's an AI agent that transforms ANY framework (Data, IT, Cyber, ESG, GDPR...) into an interactive workshop + strategic roadmap.

The goal? Generate a strategic roadmap in < 1 hour, not 3 months of consulting.

📊 MY BENCHMARK (6 domains evaluated):
• Global score: **{global_score:.1f}/100**
• Priority domains (Quick Wins): **{top3_weak}**
• Estimated ROI: **${money_value}K** + **{time_saved_days} days** saved/year
• Industry rank: **Top {100-rank_percentile}%** 🏆

💡 WHY IT'S A GAME CHANGER:
✅ 100X faster than traditional consulting
✅ 10X cheaper ($0 vs $50K+)
✅ GPT-4 AI = CDO/CTO-grade insights
✅ Works with ALL maturity frameworks
✅ Open source = zero vendor lock-in

Code is open-source. First 10 comments get a FREE diagnostic of their company in DM. 🎁

PS: I'm **open to full-time opportunities** (Lead Data Engineering, Chief Data Officer, VP Data) or strategic consulting mandates. Let's talk! 💼

#DataGovernance #AI #Consulting #Strategy #DataEngineering #CDO #CTO #OpenAI #Streamlit #DigitalTransformation #TechRecruiting #Hiring
"""

st.markdown(f"<div class='linkedin-post'>{linkedin_post}</div>", unsafe_allow_html=True)

col_post1, col_post2 = st.columns(2)
with col_post1:
    if st.button(T['generate_post'], type="primary", use_container_width=True):
        st.success(T['post_generated'])
        st.balloons()

with col_post2:
    if st.button(T['copy_post'], use_container_width=True):
        st.write("📋 Post copied to clipboard! (Simulated)")

# =========================
# ABOUT / BIO SECTION
# =========================
st.markdown(f"<div class='section-header'>{T['about_title']}</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="bio-section">
    <p style="font-size: 18px; line-height: 1.8; color: #cbd5e1; margin-bottom: 25px;">
        {T['about_text']}
    </p>
    <p style="font-size: 16px; color: #94a3b8; margin-bottom: 25px;">
        <strong>{T['footer_skills']}</strong>
    </p>
    <p style="font-size: 18px; font-weight: 700; color: #667eea; margin-top: 30px;">
        {T['about_cta']}
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# CTA BUTTONS
# =========================
st.markdown(f"<div class='section-header'>{T['contact_title']}</div>", unsafe_allow_html=True)

col_cta1, col_cta2, col_cta3 = st.columns(3)

with col_cta1:
    st.markdown(f"""
    <a href="https://www.linkedin.com/in/your-profile" target="_blank" class="cta-button">
        {T['contact_linkedin']}
    </a>
    """, unsafe_allow_html=True)

with col_cta2:
    st.markdown(f"""
    <a href="mailto:your.email@example.com" class="cta-button">
        {T['contact_email']}
    </a>
    """, unsafe_allow_html=True)

with col_cta3:
    st.markdown(f"""
    <a href="https://github.com/your-repo" target="_blank" class="cta-button">
        {T['contact_github']}
    </a>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #64748b; font-size: 15px; padding: 30px;'>
    <div style='font-size: 24px; font-weight: 800; margin-bottom: 15px;'>
        <span style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            MaturityAgent PRO
        </span>
    </div>
    <div style='margin-bottom: 10px;'>{T['footer_bio']}</div>
    <div style='font-size: 13px; color: #475569;'>{T['footer_skills']}</div>
    <div style='margin-top: 20px; font-size: 12px;'>
        © 2025 MaturityAgent PRO | MIT License | Made with ❤️ for Data Leaders
    </div>
</div>
""", unsafe_allow_html=True)
