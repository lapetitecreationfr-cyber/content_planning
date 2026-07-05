import os, json, threading, webbrowser
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DATA_FILE = os.environ.get("DATA_FILE", os.path.join(os.path.dirname(__file__), "data.json"))

DEFAULT_DATA = {
    "piliers": [
        {"id":"P001","nom":"Voix","emoji":"🎙️","couleur":"#e8b4a8","description":"Mes opinions, ma vision, mon histoire"},
        {"id":"P002","nom":"Ambiance","emoji":"🕯️","couleur":"#d4b8d4","description":"Rituels, objets qui réconfortent, esthétique slow"},
        {"id":"P003","nom":"Atelier","emoji":"🧶","couleur":"#dbb896","description":"Fait main, coulisses, processus de création"},
        {"id":"P004","nom":"Produit","emoji":"🛍️","couleur":"#b8d4a8","description":"Mise en avant des créations, lancement"},
        {"id":"P005","nom":"Loin du Scroll","emoji":"📵","couleur":"#b5c4d4","description":"Invitation à ralentir, déconnexion"}
    ],
    "contenus": [],
    "inspirations": [
        {"id":"I001","compte":"@slowliving.fr","lien":"https://instagram.com/slowliving.fr","niche":"Slow living","ce_que_jaime":"Esthétique épurée, captions longues et sincères","notes":""},
        {"id":"I002","compte":"@julie.mrgn","lien":"https://instagram.com/julie.mrgn","niche":"Artisanat / couture","ce_que_jaime":"B-rolls très sensuels, montage lent","notes":""},
        {"id":"I003","compte":"@lesfillesducreateur","lien":"https://instagram.com/lesfillesducreateur","niche":"Création textile","ce_que_jaime":"Hooks forts, voix authentique","notes":""}
    ],
    "idees": [],
    "hooks_banque": [
        {"id":"HK001","pattern":"POV","texte":"POV : tu réalises que tu n'as pas besoin de plus, juste de mieux","pilier":"P001","score":0},
        {"id":"HK002","pattern":"Arrête de scroller","texte":"Arrête de scroller 5 secondes. Regarde ça.","pilier":"P003","score":0},
        {"id":"HK003","pattern":"On m'a dit","texte":"On m'a dit que ralentir c'était abandonner. Ils avaient tort.","pilier":"P001","score":0},
        {"id":"HK004","pattern":"J'ai arrêté","texte":"J'ai arrêté d'optimiser ma vie. Voici ce qui s'est passé.","pilier":"P001","score":0},
        {"id":"HK005","pattern":"Appel","texte":"Appel à toutes celles qui préfèrent un puzzle à une soirée bruyante.","pilier":"P005","score":0}
    ]
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        d = json.load(f)
    for k, v in DEFAULT_DATA.items():
        if k not in d:
            d[k] = v
    return d

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(load_data())

@app.route("/api/data", methods=["POST"])
def post_data():
    save_data(request.get_json())
    return jsonify({"ok": True})

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    is_render = os.environ.get("RENDER", False)
    if not is_render:
        threading.Thread(target=lambda: (__import__('time').sleep(1), webbrowser.open(f'http://127.0.0.1:{port}')), daemon=True).start()
    app.run(host="0.0.0.0", port=port, debug=False)
