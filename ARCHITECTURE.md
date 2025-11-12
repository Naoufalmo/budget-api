# Architecture du projet

## Couches

1. **Routes** (routers/) : Points d'entrée API
2. **Schémas** (schemas.py) : Validation Pydantic
3. **Modèles** (models.py) : Tables PostgreSQL
4. **Business Logic** : Dans les routers
5. **Database** (database.py) : Connexion SQLAlchemy

## Flow d'une requête - Exemple: Création de transaction

**1. Requête entrante**
```http
POST /api/transactions/
Authorization: Bearer eyJ0eXAiOiJKV1...
Content-Type: application/json

{
  "title": "Courses",
  "amount": 50.0,
  "category": "expense"
}
```

**2. Traitement par couches**
```
Client Request
    ↓
[Router: transactions.py]
    ├─ Vérifie le token JWT
    ├─ Extrait current_user
    └─ Passe à la fonction create_transaction()
    ↓
[Schema: TransactionCreate]
    ├─ Valide title (string)
    ├─ Valide amount (float > 0)
    ├─ Valide category (enum: income/expense)
    └─ ✓ Données conformes
    ↓
[Business Logic dans Router]
    ├─ Crée instance du modèle Transaction
    ├─ Associe user_id = current_user.id
    └─ Ajoute à la session DB
    ↓
[Model: Transaction]
    ├─ Définit la structure (colonnes)
    ├─ Relations (clé étrangère vers User)
    └─ Prepare SQL INSERT
    ↓
[Database Session]
    ├─ db.add(transaction)
    ├─ db.commit()
    └─ db.refresh(transaction)
    ↓
[MySQL]
    ├─ INSERT INTO transactions (...)
    ├─ Retourne transaction.id = 42
    └─ ✓ Sauvegardé
    ↓
Response au Client
```

**3. Réponse**
```json
{
  "id": 42,
  "title": "Courses",
  "amount": 50.0,
  "category": "expense",
  "date": "2025-11-03T19:13:01",
  "user_id": 1
}
```