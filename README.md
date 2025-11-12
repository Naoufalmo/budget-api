# 💰 Budget API - Gestion de Budget Personnel

API RESTful moderne pour gérer vos finances personnelles avec authentification JWT et base de données MySQL.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Coverage-99%25-brightgreen)

## Fonctionnalités

- ✅ **Authentification JWT** sécurisée
- ✅ **CRUD complet** pour les transactions (Créer, Lire, Mettre à jour, Supprimer)
- ✅ **Gestion des revenus et dépenses**
- ✅ **Filtrage par catégorie et pagination**
- ✅ **Statistiques financières** en temps réel
- ✅ **Documentation API interactive** (Swagger/OpenAPI)
- ✅ **Tests unitaires** avec pytest (99% de couverture)
- ✅ **Base de données relationnelle** MySQL
- ✅ **Conteneurisation** avec Docker

## Prérequis

- Python 3.12+
- MySQL 8.0+
- Docker & Docker Compose (optionnel)

## Installation

### Option 1 : Installation locale

1. **Cloner le dépôt**
```bash
git clone https://github.com/votre-username/budget-api.git
cd budget-api
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet :
```env
# Configuration de la base de données MySQL
DATABASE_URL=mysql+pymysql://root:votre_mot_de_passe@localhost:3306/budget_db

# Clé secrète pour JWT (générez une clé unique et sécurisée)
SECRET_KEY=votre_cle_secrete_tres_longue_au_moins_32_caracteres_aleatoires

# Algorithme de chiffrement
ALGORITHM=HS256

# Durée de validité du token (en minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Pour générer une clé secrète sécurisée :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

5. **Créer la base de données MySQL**

Connectez-vous à MySQL :
```bash
mysql -u root -p
```

Créez la base de données :
```sql
CREATE DATABASE budget_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

6. **Lancer l'application**
```bash
uvicorn app.main:app --reload
```

L'API sera accessible sur `http://localhost:8000`

### Option 2 : Avec Docker
```bash
docker-compose up --build
```

L'API sera accessible sur `http://localhost:8000`

## Documentation API

Une fois l'application lancée, accédez à :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## Endpoints

### Authentication

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/register` | Créer un compte |
| POST | `/api/auth/login` | Se connecter (obtenir token) |

### Transactions

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/api/transactions/` | Créer une transaction | ✅ |
| GET | `/api/transactions/` | Liste des transactions (avec filtres) | ✅ |
| GET | `/api/transactions/{id}` | Détails d'une transaction | ✅ |
| PUT | `/api/transactions/{id}` | Modifier une transaction | ✅ |
| DELETE | `/api/transactions/{id}` | Supprimer une transaction | ✅ |
| GET | `/api/transactions/stats/summary` | Statistiques financières | ✅ |

## Exemples d'utilisation

### 1. Créer un compte
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword"
  }'
```

### 2. Se connecter
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword"
```

### 3. Créer une transaction
```bash
curl -X POST "http://localhost:8000/api/transactions/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Salaire",
    "amount": 3000.0,
    "category": "income",
    "description": "Salaire mensuel"
  }'
```

### 4. Filtrer les transactions par catégorie
```bash
curl -X GET "http://localhost:8000/api/transactions/?category=expense&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. Obtenir les statistiques
```bash
curl -X GET "http://localhost:8000/api/transactions/stats/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Tests

Lancer les tests avec pytest :
```bash
pytest
```

Avec couverture de code :
```bash
pytest --cov=app tests/
```

Rapport de couverture détaillé :
```bash
pytest --cov=app --cov-report=term-missing tests/
```

Générer un rapport HTML :
```bash
pytest --cov=app --cov-report=html tests/
```

## Structure du projet
```
budget-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée de l'application
│   ├── database.py          # Configuration de la base de données
│   ├── models.py            # Modèles SQLAlchemy
│   ├── schemas.py           # Schémas Pydantic
│   ├── auth.py              # Logique d'authentification JWT
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Routes d'authentification
│       └── transactions.py  # Routes des transactions
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Tests unitaires (99% de couverture)
├── .env                     # Variables d'environnement (non versionné)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Captures d'écran de Swagger UI
### Documentation interactive (Swagger UI)
![Swagger UI - Vue d'ensemble](screenshots/swagger-overview.png)
*Interface Swagger montrant tous les endpoints disponibles*

### Création d'un compte
![Inscription utilisateur](screenshots/register.png)
*Formulaire d'inscription avec validation des données*

### Authentification
![Login JWT](screenshots/login.png)
*Connexion et obtention du token JWT*

### Gestion des transactions
![Liste des transactions](screenshots/transactions-list.png)
*Affichage des transactions avec filtres et pagination*

### Statistiques financières
![Dashboard statistiques](screenshots/stats.png)
*Vue d'ensemble des revenus et dépenses*

## Sécurité

- Mots de passe hashés avec bcrypt
- Authentification JWT avec expiration configurable
- Validation des données avec Pydantic
- Protection CORS configurable
- Variables d'environnement pour les secrets
- Tests de sécurité (tokens invalides, expirés, etc.)

## Déploiement

### Railway (Recommandé)

1. Créer un compte sur [Railway](https://railway.app)
2. Créer une base de données MySQL
3. Déployer l'application avec les variables d'environnement
4. Railway configurera automatiquement le port

### Render

1. Créer un compte sur [Render](https://render.com)
2. Créer une base de données MySQL
3. Créer un Web Service avec les paramètres :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Ajouter les variables d'environnement

## Technologies utilisées

- **FastAPI** - Framework web moderne et rapide
- **SQLAlchemy** - ORM Python
- **PyMySQL** - Driver MySQL pour Python
- **Pydantic** - Validation des données
- **python-jose** - Gestion des JWT
- **passlib & bcrypt** - Hachage des mots de passe
- **pytest** - Framework de tests

## Améliorations futures

- [ ] Filtrage des transactions par date
- [ ] Catégories personnalisables
- [ ] Budgets mensuels et alertes
- [ ] Graphiques de dépenses
- [ ] Export CSV/PDF
- [ ] Notifications par email
- [ ] Authentification OAuth2 (Google, GitHub)
- [ ] Multi-devises
- [ ] API de taux de change

## Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## Auteur

**Bonkannon Kooly Naoufal MAMA OROU**
- Email: naoufal.mama-orou@polymtl.ca

## Remerciements

- [FastAPI](https://fastapi.tiangolo.com/) pour le framework web incroyable
- [SQLAlchemy](https://www.sqlalchemy.org/) pour l'ORM puissant
- [MySQL](https://www.mysql.com/) pour la base de données fiable
- [Pydantic](https://pydantic-docs.helpmanual.io/) pour la validation des données
