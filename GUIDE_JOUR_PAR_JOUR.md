# 📅 GUIDE JOUR PAR JOUR - Budget API

## 🎯 Objectif : Créer une API REST complète en 3 semaines (10h/semaine)

**Planning** : 1h/jour en semaine + 2-3h/jour le weekend = ~10h/semaine

---

## SEMAINE 1 : Backend & Database (10h)

### 🔷 LUNDI - Session 1h : Setup & Configuration

**Objectif** : Installer tout et comprendre la structure

#### Checklist (60 min)

1. **Cloner le template** (5 min)
   ```bash
   git clone <url-du-template>
   cd budget-api
   ```

2. **Créer l'environnement virtuel** (5 min)
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Installer MySQL** (15 min)
   - Windows : Télécharger depuis mysql.com/downloads
   - Mac : `brew install mysql`
   - Linux : `sudo apt install mysql-server`
   
   Créer la base de données :
```bash
   mysql -u root -p
   CREATE DATABASE budget_db;
   EXIT;
```

4. **Configurer .env** (5 min)
   ```bash
   cp .env.example .env
   ```
   
   Éditer `.env` :
```
   DATABASE_URL=mysql+pymysql://root:ton_mot_de_passe@localhost:3306/budget_db
   SECRET_KEY=change-cette-cle-secrete-ici-123456
```

5. **Tester que ça marche** (10 min)
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Ouvrir http://localhost:8000/docs
   ✅ Tu devrais voir la documentation Swagger !

6. **Lire et comprendre les fichiers** (20 min)
   - `app/main.py` : Point d'entrée
   - `app/models.py` : Tables de la BD
   - `app/schemas.py` : Validation des données
   - `app/routers/auth.py` : Routes d'authentification

**✅ Critères de réussite** :
- [ ] L'API démarre sans erreur
- [ ] Tu vois la doc Swagger
- [ ] Tu comprends la structure globale

---

### 🔷 MARDI - Session 1h : Tester l'authentification

**Objectif** : Comprendre comment fonctionne l'auth JWT

#### Checklist (60 min)

1. **Lancer l'API** (2 min)
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Tester l'inscription** (15 min)
   
   Sur http://localhost:8000/docs, aller à POST `/api/auth/register` :
   ```json
   {
     "email": "naoufal@example.com",
     "username": "naoufalmo",
     "password": "naoufal123"
   }
   ```
   
   ✅ Tu devrais recevoir un statut 201 Created

3. **Tester la connexion** (15 min)
   
   POST `/api/auth/login` avec :
   - username: `naoufal`
   - password: `motdepasse123`
   
   ✅ Tu reçois un `access_token`
   
   **IMPORTANT** : Copier ce token quelque part !

4. **Comprendre le code d'authentification** (20 min)
   
   Lire attentivement :
   - `app/auth.py` : Comment JWT fonctionne
   - `app/routers/auth.py` : Routes register/login
   
   **Questions à te poser** :
   - Comment le mot de passe est-il hashé ?
   - Comment le token est-il généré ?
   - Quelle est la durée de vie du token ?

5. **Ajouter des commentaires** (8 min)
   
   Dans `app/auth.py`, ajoute des commentaires pour expliquer ce que tu comprends.

**✅ Critères de réussite** :
- [ ] Tu as créé un compte
- [ ] Tu as obtenu un token JWT
- [ ] Tu comprends comment l'auth fonctionne

---

### 🔷 MERCREDI - Session 1h : Tester les transactions

**Objectif** : Utiliser l'API avec authentification

#### Checklist (60 min)

1. **Se connecter et récupérer le token** (5 min)
   ```bash
   # Garde ce token sous la main !
   ```

2. **Créer des transactions** (20 min)
   
   Dans Swagger, cliquer sur 🔒 "Authorize" en haut à droite
   
   Entrer : `Bearer <ton-token>`
   
   Puis POST `/api/transactions/` :
   ```json
   {
     "title": "Salaire octobre",
     "amount": 3000,
     "category": "income",
     "description": "Paie mensuelle"
   }
   ```
   
   Créer 5-6 transactions de test (revenus ET dépenses)

3. **Tester tous les endpoints** (20 min)
   
   - GET `/api/transactions/` → Liste toutes tes transactions
   - GET `/api/transactions/1` → Voir transaction #1
   - PUT `/api/transactions/1` → Modifier
   - GET `/api/transactions/stats/summary` → Voir statistiques
   - DELETE `/api/transactions/1` → Supprimer

4. **Comprendre le code des transactions** (15 min)
   
   Lire `app/routers/transactions.py` :
   - Comment les transactions sont filtrées par user ?
   - Comment les stats sont calculées ?

**✅ Critères de réussite** :
- [ ] Tu as créé plusieurs transactions
- [ ] Tu as testé tous les endpoints CRUD
- [ ] Tu vois tes statistiques

---

### 🔷 JEUDI - Session 1h : Ajouter une fonctionnalité

**Objectif** : Modifier le code pour ajouter quelque chose

#### Checklist (60 min)

**Nouveau endpoint : Filtrer par catégorie**

1. **Comprendre le besoin** (5 min)
   
   On veut : GET `/api/transactions/?category=income`
   
   Pour filtrer uniquement les revenus ou les dépenses.

2. **Modifier le code** (30 min)
   
   Dans `app/routers/transactions.py`, modifier `get_transactions()` :
   
   ```python
   @router.get("/", response_model=List[TransactionResponse])
   def get_transactions(
       skip: int = 0,
       limit: int = 100,
       category: str = None,  # AJOUT
       db: Session = Depends(get_db),
       current_user: User = Depends(get_current_user)
   ):
       """Récupérer toutes les transactions de l'utilisateur"""
       
       query = db.query(Transaction).filter(
           Transaction.user_id == current_user.id
       )
       
       # AJOUT : Filtrer par catégorie si spécifié
       if category:
           query = query.filter(Transaction.category == category)
       
       transactions = query.offset(skip).limit(limit).all()
       
       return transactions
   ```

3. **Tester** (15 min)
   
   Relancer l'API et tester :
   - GET `/api/transactions/` → Tout
   - GET `/api/transactions/?category=income` → Que les revenus
   - GET `/api/transactions/?category=expense` → Que les dépenses

4. **Commit Git** (10 min)
   ```bash
   git add .
   git commit -m "feat: Ajouter filtrage par catégorie"
   ```

**✅ Critères de réussite** :
- [ ] Le filtre fonctionne
- [ ] Tu as fait ton premier commit

---

### 🔷 VENDREDI - Session 1h : Comprendre la base de données

**Objectif** : Voir les données réelles dans MySQL

#### Checklist (60 min)

1. **Ouvrir MySQL Workbench** (10 min)
   
   MySQL Workbench devrait être installé avec MySQL.
   
   - Ouvrir MySQL Workbench
   - Cliquer sur ta connexion locale (généralement "Local instance MySQL")
   - Entrer ton mot de passe root

2. **Sélectionner la base de données** (5 min)
   
   Dans le panneau de gauche sous "SCHEMAS" :
   - Double-cliquer sur `budget_db`
   - Ou exécuter : `USE budget_db;`

3. **Explorer les tables avec Workbench** (20 min)
   
   **Via l'interface graphique** :
   - Dans le panneau gauche, dérouler `budget_db` → `Tables`
   - Clic droit sur `users` → "Select Rows - Limit 1000"
   - Faire pareil pour `transactions`
   
   **Via des requêtes SQL** (dans l'onglet Query) :
```sql
   -- Voir tous les utilisateurs
   SELECT * FROM users;
   
   -- Voir toutes les transactions
   SELECT * FROM transactions;
   
   -- Transactions avec info utilisateur
   SELECT t.*, u.username 
   FROM transactions t 
   JOIN users u ON t.user_id = u.id;
   
   -- Stats par catégorie
   SELECT 
       category, 
       COUNT(*) as nombre, 
       SUM(amount) as total 
   FROM transactions 
   GROUP BY category;
```

4. **Comprendre les modèles SQLAlchemy** (20 min)
   
   Relire `app/models.py` et comprendre :
   - Les colonnes
   - Les relations (User ↔ Transaction)
   - Les contraintes (unique, nullable)
   
   **Dans Workbench**, tu peux voir la structure des tables :
   - Clic droit sur une table → "Alter Table"
   - Onglet "Columns" : voir tous les champs
   - Onglet "Foreign Keys" : voir les relations

5. **Vérifier les Foreign Keys** (5 min)
   
   Exécuter :
```sql
   SHOW CREATE TABLE transactions;
```
   
   Tu verras la contrainte `FOREIGN KEY (user_id) REFERENCES users(id)` !

**✅ Critères de réussite** :
- [ ] Tu vois tes données dans MySQL Workbench
- [ ] Tu comprends les relations entre tables
- [ ] Tu sais exécuter des requêtes SQL

### 🔷 WEEKEND (Samedi) - Session 2-3h : Tests unitaires

**Objectif** : Écrire des tests automatisés

#### Checklist (2-3h)

1. **Comprendre les tests existants** (30 min)
   
   Lire `tests/test_api.py` ligne par ligne
   
   Comprendre :
   - Comment pytest fonctionne
   - Comment TestClient simule des requêtes
   - Le setup/teardown de la BD

2. **Lancer les tests** (10 min)
   ```bash
   pytest
   ```
   
   Tous devraient passer ✅

3. **Ajouter de nouveaux tests** (60-90 min)
   
   Dans `tests/test_api.py`, ajouter :
   
   ```python
   def test_get_transactions():
       """Test de récupération des transactions"""
       # 1. Créer utilisateur et se connecter
       # 2. Créer 3 transactions
       # 3. Récupérer la liste
       # 4. Vérifier qu'on a bien 3 transactions
       pass  # À compléter !
   
   def test_update_transaction():
       """Test de modification d'une transaction"""
       # 1. Créer utilisateur et transaction
       # 2. Modifier le montant
       # 3. Vérifier que c'est bien modifié
       pass  # À compléter !
   
   def test_delete_transaction():
       """Test de suppression d'une transaction"""
       pass  # À compléter !
   
   def test_get_summary():
       """Test des statistiques"""
       # 1. Créer 2 revenus et 3 dépenses
       # 2. Vérifier les sommes
       pass  # À compléter !
   ```

4. **Exécuter avec couverture** (10 min)
   ```bash
   pytest --cov=app tests/
   ```
   
   **Objectif** : Atteindre 60-70% de couverture

5. **Commit** (10 min)
   ```bash
   git add tests/
   git commit -m "test: Ajouter tests pour transactions"
   ```

**✅ Critères de réussite** :
- [ ] Tous les tests passent
- [ ] Couverture > 60%
- [ ] Tu comprends comment écrire des tests

---

### 🔷 WEEKEND (Dimanche) - Session 2-3h : Documentation

**Objectif** : Améliorer le README et la documentation

#### Checklist (2-3h)

1. **Personnaliser le README** (60 min)
   
   Modifier `README.md` :
   - Ajouter ton nom/email
   - Ajouter des screenshots (prendre avec Swagger)
   - Personnaliser la section "Auteur"
   - Ajouter badge de couverture des tests

2. **Ajouter un fichier ARCHITECTURE.md** (30 min)
   
   Créer `ARCHITECTURE.md` qui explique :
   ```markdown
   # Architecture du projet
   
   ## Couches
   
   1. **Routes** (routers/) : Points d'entrée API
   2. **Schémas** (schemas.py) : Validation Pydantic
   3. **Modèles** (models.py) : Tables PostgreSQL
   4. **Business Logic** : Dans les routers
   5. **Database** (database.py) : Connexion SQLAlchemy
   
   ## Flow d'une requête
   
   [Dessiner un schéma simple du flow]
   ```

3. **Améliorer les docstrings** (30 min)
   
   Dans `app/routers/transactions.py`, améliorer :
   
   ```python
   @router.post("/", response_model=TransactionResponse)
   def create_transaction(...):
       """
       Créer une nouvelle transaction
       
       Args:
           transaction: Données de la transaction
           
       Returns:
           TransactionResponse: Transaction créée
           
       Raises:
           HTTPException 400: Si catégorie invalide
       """
   ```

4. **Tester la doc Swagger** (20 min)
   
   Relancer l'API, aller sur /docs
   
   Vérifier que toutes les descriptions sont claires

**✅ Fin de Semaine 1** :
- [ ] API fonctionnelle avec auth JWT
- [ ] CRUD complet pour transactions
- [ ] Tests unitaires (60%+ couverture)
- [ ] Documentation solide

**Temps total Semaine 1** : ~10h

---

## SEMAINE 2 : Frontend & Amélioration (10h)

### 🔷 LUNDI - Session 1h : Créer le frontend HTML

**Objectif** : Interface simple pour visualiser les données

#### Checklist (60 min)

1. **Créer le dossier frontend** (5 min)
   ```bash
   mkdir frontend
   cd frontend
   "" > index.html
   "" > style.css
   "" > app.js
   ```

2. **Coder index.html** (25 min)
   
   Structure de base :
   ```html
   <!DOCTYPE html>
   <html lang="fr">
   <head>
       <meta charset="UTF-8">
       <title>Budget Tracker</title>
       <link rel="stylesheet" href="style.css">
   </head>
   <body>
       <div class="container">
           <h1>💰 Mes Finances</h1>
           
           <!-- Section Login -->
           <div id="auth-section">
               <input type="text" id="username" placeholder="Nom d'utilisateur">
               <input type="password" id="password" placeholder="Mot de passe">
               <button onclick="login()">Connexion</button>
           </div>
           
           <!-- Section Dashboard (caché au début) -->
           <div id="dashboard" style="display:none;">
               <div class="stats">
                   <div class="stat-card">
                       <h3>Revenus</h3>
                       <p id="total-income">0 $</p>
                   </div>
                   <div class="stat-card">
                       <h3>Dépenses</h3>
                       <p id="total-expense">0 $</p>
                   </div>
                   <div class="stat-card">
                       <h3>Balance</h3>
                       <p id="balance">0 $</p>
                   </div>
               </div>
               
               <h2>Transactions récentes</h2>
               <div id="transactions-list"></div>
           </div>
       </div>
       
       <script src="app.js"></script>
   </body>
   </html>
   ```

3. **Styler avec CSS** (20 min)
   
   Dans `style.css` :
   ```css
   * {
       margin: 0;
       padding: 0;
       box-sizing: border-box;
   }
   
   body {
       font-family: Arial, sans-serif;
       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
       padding: 20px;
   }
   
   .container {
       max-width: 900px;
       margin: 0 auto;
       background: white;
       padding: 30px;
       border-radius: 10px;
       box-shadow: 0 10px 30px rgba(0,0,0,0.2);
   }
   
   h1 {
       text-align: center;
       color: #333;
       margin-bottom: 30px;
   }
   
   .stats {
       display: grid;
       grid-template-columns: repeat(3, 1fr);
       gap: 20px;
       margin-bottom: 30px;
   }
   
   .stat-card {
       background: #f8f9fa;
       padding: 20px;
       border-radius: 8px;
       text-align: center;
   }
   
   .stat-card h3 {
       color: #666;
       font-size: 14px;
       margin-bottom: 10px;
   }
   
   .stat-card p {
       font-size: 24px;
       font-weight: bold;
       color: #667eea;
   }
   
   input, button {
       display: block;
       width: 100%;
       padding: 12px;
       margin: 10px 0;
       border: 1px solid #ddd;
       border-radius: 5px;
       font-size: 16px;
   }
   
   button {
       background: #667eea;
       color: white;
       border: none;
       cursor: pointer;
       transition: background 0.3s;
   }
   
   button:hover {
       background: #5568d3;
   }
   ```

4. **Commit** (10 min)
   ```bash
   git add frontend/
   git commit -m "feat: Ajouter interface frontend de base"
   ```

**✅ Critères de réussite** :
- [ ] Page HTML créée
- [ ] Design responsive

---

### 🔷 MARDI - Session 1h : Connecter frontend à l'API

**Objectif** : Faire fonctionner la connexion

#### Checklist (60 min)

1. **Coder app.js pour la connexion** (40 min)
   
   ```javascript
   const API_URL = 'http://localhost:8000';
   let token = null;
   
   async function login() {
       const username = document.getElementById('username').value;
       const password = document.getElementById('password').value;
       
       try {
           // Connexion
           const formData = new FormData();
           formData.append('username', username);
           formData.append('password', password);
           
           const response = await fetch(`${API_URL}/api/auth/login`, {
               method: 'POST',
               body: formData
           });
           
           if (!response.ok) {
               alert('Erreur de connexion');
               return;
           }
           
           const data = await response.json();
           token = data.access_token;
           
           // Afficher le dashboard
           document.getElementById('auth-section').style.display = 'none';
           document.getElementById('dashboard').style.display = 'block';
           
           // Charger les données
           loadData();
           
       } catch (error) {
           console.error('Erreur:', error);
           alert('Erreur de connexion');
       }
   }
   
   async function loadData() {
       try {
           // Récupérer les statistiques
           const statsResponse = await fetch(`${API_URL}/api/transactions/stats/summary`, {
               headers: {
                   'Authorization': `Bearer ${token}`
               }
           });
           
           const stats = await statsResponse.json();
           
           document.getElementById('total-income').textContent = stats.total_income + ' $';
           document.getElementById('total-expense').textContent = stats.total_expense + ' $';
           document.getElementById('balance').textContent = stats.balance + ' $';
           
           // Récupérer les transactions
           const transResponse = await fetch(`${API_URL}/api/transactions/`, {
               headers: {
                   'Authorization': `Bearer ${token}`
               }
           });
           
           const transactions = await transResponse.json();
           displayTransactions(transactions);
           
       } catch (error) {
           console.error('Erreur:', error);
       }
   }
   
   function displayTransactions(transactions) {
       const listDiv = document.getElementById('transactions-list');
       listDiv.innerHTML = '';
       
       transactions.forEach(t => {
           const div = document.createElement('div');
           div.className = 'transaction-item';
           div.innerHTML = `
               <strong>${t.title}</strong> - ${t.amount} $ (${t.category})
               <br><small>${new Date(t.date).toLocaleDateString()}</small>
           `;
           listDiv.appendChild(div);
       });
   }
   ```

2. **Ajouter styles pour transactions** (10 min)
   
   Dans `style.css` :
   ```css
   .transaction-item {
       background: #f8f9fa;
       padding: 15px;
       margin: 10px 0;
       border-radius: 5px;
       border-left: 4px solid #667eea;
   }
   ```

3. **Tester** (10 min)
   
   Ouvrir `frontend/index.html` dans le navigateur
   
   ⚠️ **IMPORTANT** : Activer CORS dans l'API !
   
   L'API a déjà CORS activé dans `main.py`, ça devrait fonctionner

**✅ Critères de réussite** :
- [ ] Tu peux te connecter
- [ ] Les stats s'affichent
- [ ] Les transactions s'affichent

---

### 🔷 MERCREDI - Session 1h : Améliorer le frontend

**Objectif** : Ajouter des fonctionnalités

#### Checklist (60 min)

1. **Ajouter formulaire de création** (30 min)
   
   Dans `index.html`, après les stats :
   ```html
   <h2>Nouvelle transaction</h2>
   <input type="text" id="new-title" placeholder="Titre">
   <input type="number" id="new-amount" placeholder="Montant">
   <select id="new-category">
       <option value="income">Revenu</option>
       <option value="expense">Dépense</option>
   </select>
   <button onclick="createTransaction()">Ajouter</button>
   ```
   
   Dans `app.js` :
   ```javascript
   async function createTransaction() {
       const title = document.getElementById('new-title').value;
       const amount = parseFloat(document.getElementById('new-amount').value);
       const category = document.getElementById('new-category').value;
       
       try {
           const response = await fetch(`${API_URL}/api/transactions/`, {
               method: 'POST',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify({
                   title,
                   amount,
                   category,
                   description: ''
               })
           });
           
           if (response.ok) {
               alert('Transaction ajoutée !');
               // Recharger les données
               loadData();
               // Vider le formulaire
               document.getElementById('new-title').value = '';
               document.getElementById('new-amount').value = '';
           }
       } catch (error) {
           console.error('Erreur:', error);
       }
   }
   ```

2. **Améliorer l'affichage** (20 min)
   
   Ajouter des couleurs selon le type :
   ```javascript
   function displayTransactions(transactions) {
       const listDiv = document.getElementById('transactions-list');
       listDiv.innerHTML = '';
       
       transactions.forEach(t => {
           const div = document.createElement('div');
           div.className = 'transaction-item';
           
           // Couleur selon type
           const color = t.category === 'income' ? '#10b981' : '#ef4444';
           div.style.borderLeftColor = color;
           
           div.innerHTML = `
               <strong>${t.title}</strong> - 
               <span style="color: ${color};">${t.amount} $</span>
               (${t.category === 'income' ? 'Revenu' : 'Dépense'})
               <br><small>${new Date(t.date).toLocaleDateString('fr-FR')}</small>
           `;
           listDiv.appendChild(div);
       });
   }
   ```

3. **Commit** (10 min)
   ```bash
   git add frontend/
   git commit -m "feat: Ajouter création de transactions au frontend"
   ```

**✅ Critères de réussite** :
- [ ] Tu peux ajouter des transactions
- [ ] Les couleurs fonctionnent
- [ ] L'interface se recharge automatiquement

---

### 🔷 JEUDI - Session 1h : Documentation Swagger personnalisée

**Objectif** : Améliorer la doc API

#### Checklist (60 min)

1. **Ajouter descriptions détaillées** (30 min)
   
   Dans `app/main.py` :
   ```python
   app = FastAPI(
       title="Budget API",
       description="""
       # 💰 API de Gestion de Budget Personnel
       
       Cette API permet de gérer vos finances personnelles de manière simple et sécurisée.
       
       ## Fonctionnalités
       
       * **Authentification JWT** sécurisée
       * **CRUD complet** des transactions
       * **Statistiques** financières en temps réel
       * **Filtrage** par catégorie
       
       ## Utilisation
       
       1. Créer un compte avec `/api/auth/register`
       2. Se connecter avec `/api/auth/login` pour obtenir un token
       3. Utiliser le token dans l'en-tête `Authorization: Bearer <token>`
       4. Gérer vos transactions !
       
       ## Support
       
       Email: naoufal.mama-orou@etud.polymtl.ca
       """,
       version="1.0.0",
       contact={
           "name": "Naoufal MAMA OROU",
           "email": "naoufal.mama-orou@etud.polymtl.ca",
           "url": "https://www.linkedin.com/in/naoufal-mama-orou-4191b4291"
       },
       license_info={
           "name": "MIT",
       }
   )
   ```

2. **Ajouter des exemples** (20 min)
   
   Dans `app/schemas.py` :
   ```python
   class TransactionCreate(TransactionBase):
       class Config:
           json_schema_extra = {
               "example": {
                   "title": "Salaire octobre",
                   "amount": 3000.0,
                   "category": "income",
                   "description": "Paie mensuelle"
               }
           }
   ```

3. **Tester** (10 min)
   
   Relancer l'API et vérifier /docs
   
   Prendre des screenshots pour le README !

**✅ Critères de réussite** :
- [ ] Doc Swagger améliorée
- [ ] Exemples clairs
- [ ] Screenshots pris

---

### 🔷 VENDREDI - Session 1h : Préparer le déploiement

**Objectif** : Préparer les fichiers pour déployer

#### Checklist (60 min)

1. **Créer requirements.txt de production** (10 min)
   
   Créer `requirements-prod.txt` :
   ```
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   sqlalchemy==2.0.23
   psycopg2-binary==2.9.9
   python-jose[cryptography]==3.3.0
   passlib[bcrypt]==1.7.4
   python-dotenv==1.0.0
   pydantic==2.5.0
   pydantic-settings==2.1.0
   ```

2. **Créer un script de démarrage** (15 min)
   
   Créer `start.sh` :
   ```bash
   #!/bin/bash
   
   # Script de démarrage pour production
   
   # Créer les tables si nécessaire
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   
   # Lancer l'application
   uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
   
   Rendre exécutable :
   ```bash
   chmod +x start.sh
   ```

3. **Créer render.yaml** (20 min)
   
   Pour déployer sur Render :
   ```yaml
   services:
     - type: web
       name: budget-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: ./start.sh
       envVars:
         - key: DATABASE_URL
           sync: false
         - key: SECRET_KEY
           generateValue: true
         - key: PYTHON_VERSION
           value: 3.11.0
   
   databases:
     - name: budget-db
       databaseName: budget_db
       user: budget_user
   ```

4. **Mettre à jour .gitignore** (5 min)
   
   Ajouter :
   ```
   # Production
   start.sh.log
   *.log
   
   # Frontend build (si tu builds plus tard)
   frontend/dist/
   ```

5. **Commit final** (10 min)
   ```bash
   git add .
   git commit -m "chore: Préparer le déploiement"
   git push
   ```

**✅ Critères de réussite** :
- [ ] Fichiers de déploiement créés
- [ ] Code sur GitHub
- [ ] Prêt pour déployer

---

### 🔷 WEEKEND (Samedi) - Session 2-3h : Déploiement sur Render

**Objectif** : Mettre l'API en ligne !

#### Checklist (2-3h)

1. **Créer compte Render** (10 min)
   
   Aller sur https://render.com et s'inscrire (gratuit)

2. **Créer la base de données PostgreSQL** (15 min)
   
   Sur Render :
   - New > PostgreSQL
   - Nom : budget-db
   - Gratuit (Free)
   - Créer
   
   **IMPORTANT** : Noter l'URL de connexion !

3. **Créer le Web Service** (20 min)
   
   - New > Web Service
   - Connecter ton repo GitHub
   - Nom : budget-api
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Ajouter les variables d'environnement** (15 min)
   
   Dans les settings du Web Service :
   ```
   DATABASE_URL = <URL de ta BD PostgreSQL>
   SECRET_KEY = <générer une clé aléatoire>
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   ```

5. **Déployer** (10 min)
   
   Cliquer sur "Deploy"
   
   Attendre 3-5 minutes...
   
   ✅ Ton API est en ligne !

6. **Tester l'API en ligne** (30 min)
   
   URL : `https://budget-api-xxx.onrender.com`
   
   Tester avec Postman ou depuis /docs :
   - Créer un compte
   - Se connecter
   - Créer des transactions
   
   **TOUT DOIT FONCTIONNER** 🎉

7. **Déployer le frontend sur Netlify** (45 min)
   
   - Créer compte Netlify
   - Dans `frontend/app.js`, changer :
     ```javascript
     const API_URL = 'https://budget-api-xxx.onrender.com';
     ```
   - Drag & drop le dossier `frontend` sur Netlify
   - ✅ Frontend en ligne !

8. **Mettre à jour le README** (15 min)
   
   Ajouter :
   ```markdown
   ## 🌐 Demo Live
   
   - **API** : https://budget-api-xxx.onrender.com
   - **Frontend** : https://budget-frontend-xxx.netlify.app
   - **Documentation** : https://budget-api-xxx.onrender.com/docs
   ```

**✅ Critères de réussite** :
- [ ] API déployée et accessible
- [ ] Frontend déployé
- [ ] Tu peux te connecter et utiliser l'app !

---

### 🔷 WEEKEND (Dimanche) - Session 2-3h : Finitions & CV

**Objectif** : Polir le projet et l'ajouter au CV

#### Checklist (2-3h)

1. **Prendre de beaux screenshots** (30 min)
   
   Capturer :
   - Page d'accueil du frontend
   - Dashboard avec données
   - Documentation Swagger
   - Résultats des tests
   
   Les mettre dans un dossier `screenshots/`

2. **Améliorer le README final** (45 min)
   
   Ajouter :
   - Badges (build, coverage, license)
   - GIF ou vidéo démo
   - Section "Défis techniques"
   - Section "Ce que j'ai appris"

3. **Créer CHANGELOG.md** (20 min)
   
   Documenter toutes les fonctionnalités :
   ```markdown
   # Changelog
   
   ## [1.0.0] - 2025-10-XX
   
   ### Ajouté
   - Authentification JWT avec register/login
   - CRUD complet pour les transactions
   - Statistiques financières
   - Filtrage par catégorie
   - Interface web responsive
   - Tests unitaires (70% couverture)
   - Déploiement Render + Netlify
   - Documentation Swagger complète
   ```

4. **Écrire un article de blog** (60 min)
   
   Créer `BLOG.md` :
   ```markdown
   # Comment j'ai créé une API de gestion de budget en 2 semaines
   
   ## Le contexte
   [Expliquer pourquoi]
   
   ## Les technologies choisies
   [Expliquer FastAPI, PostgreSQL, etc.]
   
   ## Les défis rencontrés
   - Authentification JWT
   - Déploiement PostgreSQL
   - CORS
   
   ## Ce que j'ai appris
   [Liste détaillée]
   
   ## Statistiques
   - Lignes de code : ~800
   - Tests : 15
   - Couverture : 70%
   - Temps : 20 heures
   ```

5. **Ajouter au CV** (20 min)
   
   Dans ton CV :
   ```
   API REST de gestion de budget personnel | Python/FastAPI + PostgreSQL
   - Développement d'une API RESTful avec 8 endpoints authentifiés (JWT)
   - Base de données PostgreSQL avec 2 tables relationnelles (Users, Transactions)
   - Interface web responsive avec JavaScript vanilla pour visualisation
   - Tests automatisés avec pytest (70% de couverture)
   - Documentation interactive avec Swagger/OpenAPI
   - Déployé sur Render (backend) et Netlify (frontend) avec CI/CD
   - 800+ lignes de code, 15 tests, disponible en ligne
   ```

6. **Publier sur LinkedIn** (20 min)
   
   Post avec :
   - Screenshot du projet
   - Lien GitHub
   - Lien live demo
   - Hashtags : #Python #FastAPI #PostgreSQL #WebDev

**✅ FIN DE SEMAINE 2** :
- [ ] Projet déployé et accessible
- [ ] Documentation complète
- [ ] Ajouté au CV
- [ ] Publié sur LinkedIn

---

## SEMAINE 3 : Polish & Avancé (Optionnel)

### Si tu as encore du temps et de la motivation...

#### Options d'amélioration :

1. **GitHub Actions CI/CD** (2h)
   - Tests automatiques sur chaque push
   - Badge de build

2. **Docker Compose local** (1h)
   - Faciliter le setup pour d'autres devs

3. **Nouvelle fonctionnalité** (3h)
   - Graphiques avec Chart.js
   - Export CSV
   - Catégories personnalisables

4. **Contribution open source** (5h+)
   - Trouver un projet FastAPI sur GitHub
   - Corriger un bug ou ajouter une feature

---

## 📊 RÉCAPITULATIF FINAL

### Ce que tu auras accompli :

✅ **API REST complète**
- 8 endpoints fonctionnels
- Authentification JWT
- Base de données PostgreSQL
- Tests unitaires (70%)
- Documentation Swagger

✅ **Frontend web**
- Interface responsive
- Connexion/visualisation
- Ajout de transactions

✅ **Déploiement**
- API sur Render
- Frontend sur Netlify
- Accessible publiquement

✅ **Compétences développées**
- Python/FastAPI
- SQL/PostgreSQL
- JavaScript
- Git/GitHub
- Tests automatisés
- Déploiement cloud

✅ **Prêt pour le CV** !

### Statistiques finales :
- **Temps investi** : ~20-25 heures sur 2-3 semaines
- **Lignes de code** : ~800
- **Tests** : 15+
- **Couverture** : 70%+
- **Commits** : 15-20
- **Technologies** : 10+

---

## 🎯 CONSEILS POUR RÉUSSIR

### Mindset
- ✅ Fais 1h par jour minimum (constance > intensité)
- ✅ Commit tous les jours (streak GitHub)
- ✅ Documente au fur et à mesure
- ✅ Teste chaque nouvelle fonctionnalité

### Si tu bloques
1. Lis la doc officielle (fastapi.tiangolo.com)
2. Cherche sur Stack Overflow
3. Demande à ChatGPT/Claude
4. Ne reste jamais bloqué plus de 30 min

### Gestion du temps
- **1h en semaine** : 1 tâche précise
- **2-3h weekend** : 1 grosse fonctionnalité
- Utilise un timer (Pomodoro : 25 min focus)

---

## 🚀 APRÈS LE PROJET

### Prochaines étapes :

1. **Partager** :
   - LinkedIn
   - Portfolio personnel
   - Communautés dev (Reddit, Discord)

2. **Améliorer** :
   - Écouter les feedbacks
   - Ajouter des features demandées

3. **Enchaîner** :
   - Projet 2 : CLI Tool Python
   - Projet 3 : Contribution open source

---

## 💡 QUESTIONS FRÉQUENTES

**Q : Je suis en retard sur le planning, c'est grave ?**
A : Pas du tout ! C'est un guide, pas une obligation. L'important c'est de finir.

**Q : Je ne comprends pas un concept, je continue ?**
A : Non ! Prends 20-30 min pour bien comprendre. C'est un investissement.

**Q : Render est trop lent en version gratuite ?**
A : Normal, c'est gratuit. Mentionne-le dans ton README comme limitation.

**Q : Combien de temps pour tout faire ?**
A : 20-25h réparties sur 2-3 semaines = réaliste et faisable !

---

## 🎉 CONCLUSION

Tu as tout ce qu'il faut pour réussir !

**Remember** :
- Pas de perfection, juste de la progression
- Chaque commit compte
- Documente tout
- Partage ton travail

**Bon courage ! 💪**

**Questions ? Bloqué quelque part ?**
N'hésite pas à me demander de l'aide à chaque étape !
