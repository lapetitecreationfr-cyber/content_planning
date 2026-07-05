# 🌸 Déploiement sur Render — Instructions

## Ce que tu vas obtenir
Une URL permanente accessible depuis ton téléphone, ta tablette, n'importe où, sans que ton ordi soit allumé.
Exemple : `https://contenu-instagram.onrender.com`

---

## Étape 1 — Créer un compte GitHub (gratuit)
1. Va sur **github.com** → "Sign up"
2. Crée un compte gratuit

## Étape 2 — Mettre les fichiers sur GitHub
1. Une fois connectée sur GitHub, clique sur **"New repository"** (bouton vert)
2. Nomme-le `contenu-instagram` (ou `contenu-instagram` pour l'autre outil)
3. Laisse tout par défaut, clique **"Create repository"**
4. Clique sur **"uploading an existing file"**
5. **Glisse-dépose** tous les fichiers du dossier dans la zone (app.py, requirements.txt, Procfile, et le dossier templates/)
6. Clique **"Commit changes"**

## Étape 3 — Créer un compte Render (gratuit)
1. Va sur **render.com** → "Get Started for Free"
2. Connecte-toi **avec ton compte GitHub** (plus simple)

## Étape 4 — Déployer l'appli
1. Sur Render, clique **"New +"** → **"Web Service"**
2. Sélectionne ton repository GitHub (`contenu-instagram`)
3. Render détecte Flask automatiquement
4. Vérifie ces paramètres :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
   - **Plan** : Free
5. Clique **"Create Web Service"**
6. Attends 2-3 minutes → tu obtiens ton URL ! 🎉

## Étape 5 — Accéder depuis ton téléphone
1. Copie l'URL (ex: `https://contenu-instagram.onrender.com`)
2. Ouvre-la dans Safari/Chrome sur ton téléphone
3. Ajoute-la à ton écran d'accueil pour un accès rapide comme une app !

---

## ⚠️ Important — Persistance des données
Sur le plan gratuit de Render, le système de fichiers se **réinitialise** à chaque redéploiement.
Pour éviter de perdre tes données :
- Ajoute une **Variable d'environnement** sur Render : `DATA_FILE` = `/tmp/data.json`
- Ou exporte régulièrement tes données (bouton "Exporter" dans l'outil)

## 💡 Note sur le plan gratuit
- L'appli se "met en veille" après 15 min sans utilisation
- Elle se réveille en ~30 secondes à la prochaine visite
- C'est normal, pas d'inquiétude !

---

## En cas de problème
Reviens me voir avec une capture d'écran de l'erreur 🌸
