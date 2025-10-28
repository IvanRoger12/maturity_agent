# 🧭 MaturityAgent — Enterprise Maturity AI (FR/EN)

Agent IA Streamlit pour évaluer la **maturité d’entreprise** (Data, IT, Sécurité, Gouvernance, Produit) :
- Questionnaire dynamique (Excel import ou modèle par défaut)
- Score global + scores par domaine
- Radar & priorisation (faible maturité × poids)
- Synthèse exécutive & feuille de route (IA OpenAI optionnelle)
- Export **Markdown** + post LinkedIn prêt à copier-coller
- **Multilingue** : Français / English

## 🚀 Lancer en local
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
