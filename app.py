import os
import json
from datetime import datetime, timezone

import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# ── Configuration Supabase ──────────────────────────────────────────────
# Sur l'hébergeur (Render), définis ces deux variables d'environnement :
#   SUPABASE_URL  = https://xxxxxxxx.supabase.co
#   SUPABASE_KEY  = <clé service_role>   (côté serveur uniquement, jamais dans le HTML)
# En local, si elles ne sont pas définies, l'app retombe sur data.json.
SUPABASE_URL = os.environ.get('SUPABASE_URL', '').rstrip('/')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

TABLE = 'app_state'
ROW_ID = 'contenu_instagram'
LOCAL_FILE = 'data.json'

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
}


def default_data():
    """Données de départ : le data.json committé dans le repo s'il existe,
    sinon un squelette vide. Sert de graine au tout premier lancement."""
    try:
        with open(LOCAL_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {
            "contenus": [],
            "idees": [],
            "hooks_banque": [],
            "inspirations": [],
            "tournage": [],
            "piliers": [],
        }


def read_state():
    if not USE_SUPABASE:
        return default_data()
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{ROW_ID}&select=data"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    rows = r.json()
    if rows:
        return rows[0]['data']
    # Aucune ligne encore : on sème avec les données par défaut.
    seed = default_data()
    write_state(seed)
    return seed


def write_state(data):
    if not USE_SUPABASE:
        with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}?on_conflict=id"
    headers = dict(HEADERS)
    headers['Prefer'] = 'resolution=merge-duplicates,return=minimal'
    body = [{
        "id": ROW_ID,
        "data": data,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }]
    r = requests.post(url, headers=headers, data=json.dumps(body), timeout=20)
    r.raise_for_status()


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/api/data', methods=['GET'])
def get_data():
    resp = jsonify(read_state())
    resp.headers['Cache-Control'] = 'no-store'
    return resp


@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json(force=True)
    write_state(data)
    return jsonify({"ok": True})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
