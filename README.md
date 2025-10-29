# MaturityAgent PRO — v10

**Dernière génération** : 2025-10-29 02:05 UTC

## Démarrage rapide

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### (Optionnel) Export PDF
- Recommandé : `pip install weasyprint tinycss2 cssselect2`
- Alternative : `pip install pdfkit` + installer le binaire `wkhtmltopdf`

### (Optionnel) Mode IA OpenAI
- Installer : `pip install openai`
- Ajouter la clé : **Streamlit Cloud → Manage app → Settings → Secrets**
  ```toml
  OPENAI_API_KEY="sk-xxxxx"
  ```
  ou définir `OPENAI_API_KEY` dans vos variables d’environnement.

## Modèle Excel
- Fichier : `questions.xlsx`
- Onglet **questions** : utilisé par défaut
- Onglet **sql_template_optional** : gabarit pour le module SQL (si activé)

## Astuces
- Vous pouvez fusionner vos propres questions dans l’onglet *questions*.
- Le module SQL est activable depuis la sidebar.
- Le bouton PDF tente WeasyPrint puis pdfkit.
