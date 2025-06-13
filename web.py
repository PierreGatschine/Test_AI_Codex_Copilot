import sqlite3
from flask import Flask, request, render_template_string
import db

app = Flask(__name__)

db.init_db()

FORM = """
<!doctype html>
<title>Assistant Parc</title>
<h1>Recherche de reponse</h1>
<form method=post>
  <label>Catégorie:
    <input type=text name=categorie required>
  </label>
  <input type=submit value="Chercher">
</form>
{% if reponse %}
<h2>Réponse :</h2>
<pre>{{ reponse }}</pre>
{% elif demande %}
<p>Aucune réponse trouvée pour la catégorie {{ demande }}.</p>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    reponse = None
    demande = None
    if request.method == 'POST':
        demande = request.form.get('categorie', '').strip()
        if demande:
            reponse = db.chercher_texte_reponse(demande)
    return render_template_string(FORM, reponse=reponse, demande=demande)

if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Serveur Web de l'assistant")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", 5000)),
        help="Port d'\xE9coute (5000 par d\xE9faut)",
    )
    args = parser.parse_args()

    app.run(debug=True, port=args.port)
