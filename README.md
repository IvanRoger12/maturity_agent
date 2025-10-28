# 🚀 Agent IA de Transformation Stratégique

Ce n'est pas un simple "calculateur de maturité". C'est un **agent IA** conçu pour transformer un framework stratégique (Data, IT, Cyber, ESG...) en une **feuille de route actionnable**.

L'objectif : arrêter de produire des diagnostics Excel qui finissent dans un SharePoint.
Le but : utiliser l'IA pour générer une analyse de niveau consultant en **moins d'une heure**, pas en trois mois.

## ✨ Features

-   **Diagnostic Dynamique :** Basé sur votre propre référentiel Excel (16 domaines, 6 axes).
-   **Analyse "SaaS" :** Score global, radar de maturité et dashboard de priorisation.
-   **Agent IA (Optionnel) :** Génération d'une synthèse exécutive et d'une feuille de route (90j / 6m / 1an) via OpenAI (GPT-4o).
-   **Design "Magnifique" :** Une interface Dark Mode (SaaS) conçue pour impressionner en COMEX.
-   **Export 1-Click :** Génère un rapport Markdown complet et un post LinkedIn pour partager vos résultats.

## 🎯 Pour les Recruteurs & Managers

Ce projet n'est pas un exercice technique. C'est un **produit**. Il démontre ma capacité à :

1.  **Comprendre un Besoin Métier :** Traduire un "pain point" de consultant (les diagnostics longs et coûteux) en une solution logicielle.
2.  **Penser "Produit" :** Concevoir une UX/UI (Dark Mode, `st.radio`) qui sert l'utilisateur final (consultant, DSI) et valorise l'analyse.
3.  **Intégrer l'IA (Pragmatique) :** Utiliser un LLM non pas comme un gadget, mais comme un *accélérateur* pour une tâche à haute valeur ajoutée (synthèse, roadmap).
4.  **Livrer (End-to-End) :** Du `pandas` pour la logique métier au `CSS` pour le design, jusqu'au `README.md` pour le marketing.

C'est ce que j'apporte à une équipe : la capacité de **bâtir et de livrer**.

## 🚀 Lancement

### 1. Local

```bash
git clone [VOTRE_REPO_URL]
cd maturity-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optionnel (pour l'IA)
export OPENAI_API_KEY="sk-..." 

streamlit run app.py
