# 🚀 DÉMARRAGE RAPIDE - 5 minutes

## Étape 1 : Télécharger le projet

Tu as déjà le dossier `budget-api-template/` !

## Étape 2 : Installer Python

Si pas déjà fait :
- Windows : python.org/downloads
- Mac : `brew install python`
- Linux : `sudo apt install python3 python3-pip`

## Étape 3 : Setup (5 minutes)

```bash
# 1. Aller dans le dossier
cd budget-api-template

# 2. Créer environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Windows :
.venv\Scripts\activate
# Mac/Linux :
source venv/Scripts/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Installer PostgreSQL
# Windows : télécharger depuis postgresql.org
# Mac : brew install postgresql
# Linux : sudo apt install postgresql

# 6. Créer la base de données
mysql -u root -p
# Puis tape : CREATE DATABASE budget_db;
# Puis tape : EXIT;

# 7. Copier le fichier .env
cp .env.example .env
# Puis éditer .env avec tes paramètres

# 8. Lancer l'API
uvicorn app.main:app --reload
```

## Étape 4 : Tester

Ouvre ton navigateur : http://localhost:8000/docs

Tu verras la documentation Swagger interactive ! 🎉

## Étape 5 : Créer un compte

Dans Swagger UI :
1. Va à POST `/api/auth/register`
2. Clique sur "Try it out"
3. Entre :
```json
{
  "email": "test@example.com",
  "username": "test",
  "password": "test123"
}
```
4. Execute

✅ Compte créé !

## Prochaines étapes

Ouvre le fichier **GUIDE_JOUR_PAR_JOUR.md** pour suivre le plan détaillé jour par jour.

---

## 📁 Structure du projet

```
budget-api-template/
├── app/                    # Code de l'application
│   ├── main.py            # Point d'entrée
│   ├── database.py        # Config BD
│   ├── models.py          # Tables
│   ├── schemas.py         # Validation
│   ├── auth.py            # JWT
│   └── routers/           # Endpoints
│       ├── auth.py
│       └── transactions.py
├── tests/                 # Tests unitaires
├── frontend/              # Interface web (vide pour l'instant)
├── requirements.txt       # Dépendances
├── .env.example          # Variables d'environnement
├── docker-compose.yml    # Pour Docker
├── Dockerfile
├── README.md             # Documentation
├── GUIDE_JOUR_PAR_JOUR.md # Guide détaillé ⭐
└── DEMARRAGE_RAPIDE.md   # Ce fichier

```

## ❓ Problèmes fréquents

### "Command not found: uvicorn"
→ Assure-toi que l'environnement virtuel est activé

### "Could not connect to database"
→ Vérifie que MySQL est installé et que la BD `budget_db` existe

### "Port already in use"
→ Change le port : `uvicorn app.main:app --reload --port 8001`

---

**Tu es prêt ! Commence par le LUNDI du guide jour par jour ! 💪**
