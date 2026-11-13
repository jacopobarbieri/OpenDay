from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def home():
    try:
        # Correzione: encoding deve essere una stringa ("utf-8")
        with open("dati.json", "r", encoding="utf-8") as f:
            dati_da_mostrare = json.load(f)
    except FileNotFoundError:
        # Evita il crash se il file non viene trovato
        dati_da_mostrare = {"errore": "File dati.json non trovato"}
        
    return render_template("index.html", dati=dati_da_mostrare)

if __name__ == "__main__":
    # host="0.0.0.0" rende la pagina visibile sulla rete locale
    app.run(host="0.0.0.0", port=5000, debug=True)
