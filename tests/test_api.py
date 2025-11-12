import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Setup/Teardown de la base de données de test
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_root():
    """Test de la route racine"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test du health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user():
    """Test de création d'un utilisateur"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_register_duplicate_user():
    """Test de création d'un utilisateur avec email déjà existant"""
    # Créer le premier utilisateur
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    # Essayer de créer un deuxième avec le même email
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser2",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400

def test_login():
    """Test de connexion"""
    # Créer un utilisateur
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    # Se connecter
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_transaction():
    """Test de création d'une transaction"""
    # Créer et connecter un utilisateur
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Créer une transaction
    response = client.post(
        "/api/transactions/",
        json={
            "title": "Salaire",
            "amount": 3000.0,
            "category": "income",
            "description": "Salaire mensuel"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Salaire"
    assert data["amount"] == 3000.0
    assert data["category"] == "income"

def test_get_transactions():
    """Test de récupération des transactions"""
    # Créer utilisateur et se connecter
    client.post("/api/auth/register",
                json={
                    "email": "123@exemple.com",
                    "username": "AsapRocky",
                    "password": "123"
                })

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "AsapRocky",
            "password": "123"
        }
    )
    token = login_response.json()["access_token"]

    # Créer 3 transactions
    response = client.post(
        "/api/transactions/",
        json={
            "title": "Salaire",
            "amount": 3000.0,
            "category": "income",
            "description": "Salaire mensuel"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    response = client.post(
        "/api/transactions/",
        json={
            "title": "Chichi",
            "amount": 15000.0,
            "category": "expense",
            "description": "Depense inutile"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    response = client.post(
        "/api/transactions/",
        json={
            "title": "Cadeaux",
            "amount": 700.0,
            "category": "expense",
            "description": "Tous les cadeaux effectues"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # 3. Récupérer la liste
    response = client.get(
        "/api/transactions/",
        headers={"Authorization": f"Bearer {token}"}
    )

    # 4. Vérifier qu'on a bien 3 transactions
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 3

    transactionsList = ["Salaire", "Chichi", "Cadeaux"]
    assert transactions[0]["title"] in transactionsList
    assert transactions[1]["title"] in transactionsList
    assert transactions[2]["title"] in transactionsList


def test_update_transaction():
    """Test de modification d'une transaction"""
    # 1. Créer utilisateur et transaction
    client.post("/api/auth/register",
                json={
                    "email": "123@exemple.com",
                    "username": "AsapRocky",
                    "password": "123"
                })

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "AsapRocky",
            "password": "123"
        }
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/transactions/",
        json={
            "title": "Salaire",
            "amount": 3000.0,
            "category": "income",
            "description": "Salaire mensuel"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # 2. Modifier le montant
    response = client.put(
        "/api/transactions/1",
        json={
            "title": "Test",
            "amount": 0.0,
            "category": "expense",
            "description": "Test"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # 3. Vérifier que c'est bien modifié
    updated_transaction = response.json()

    assert updated_transaction["title"] == "Test"
    assert updated_transaction["amount"] == 0.0
    assert updated_transaction["category"] == "expense"
    assert updated_transaction["description"] == "Test"

def test_delete_transaction():
    """Test de suppression d'une transaction"""
    client.post("/api/auth/register",
                json={
                    "email": "123@exemple.com",
                    "username": "AsapRocky",
                    "password": "123"
                })

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "AsapRocky",
            "password": "123"
        }
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/transactions/",
        json={
            "title": "Salaire",
            "amount": 3000.0,
            "category": "income",
            "description": "Salaire mensuel"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # ✅ STOCKER LA RÉPONSE DU DELETE
    delete_response = client.delete(
        "/api/transactions/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 204


def test_get_transaction_not_found():
    """Test de récupération d'une transaction inexistante"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    login_response = client.post("/api/auth/login", data={"username": "testuser", "password": "123"})
    token = login_response.json()["access_token"]

    # Essayer de récupérer une transaction qui n'existe pas
    response = client.get("/api/transactions/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_update_transaction_not_found():
    """Test de modification d'une transaction inexistante"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    login_response = client.post("/api/auth/login", data={"username": "testuser", "password": "123"})
    token = login_response.json()["access_token"]

    response = client.put(
        "/api/transactions/999",
        json={"title": "Test", "amount": 100.0, "category": "expense", "description": "Test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_delete_transaction_not_found():
    """Test de suppression d'une transaction inexistante"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    login_response = client.post("/api/auth/login", data={"username": "testuser", "password": "123"})
    token = login_response.json()["access_token"]

    response = client.delete("/api/transactions/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_get_transactions_with_category_filter():
    """Test de filtrage par catégorie"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    login_response = client.post("/api/auth/login", data={"username": "testuser", "password": "123"})
    token = login_response.json()["access_token"]

    # Créer des transactions de différentes catégories
    client.post("/api/transactions/",
                json={"title": "Salaire", "amount": 3000.0, "category": "income", "description": "Test"},
                headers={"Authorization": f"Bearer {token}"})

    client.post("/api/transactions/",
                json={"title": "Courses", "amount": 50.0, "category": "expense", "description": "Test"},
                headers={"Authorization": f"Bearer {token}"})

    # Filtrer par catégorie
    response = client.get("/api/transactions/?category=income", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 1
    assert transactions[0]["category"] == "income"


def test_get_transactions_with_pagination():
    """Test de pagination"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    login_response = client.post("/api/auth/login", data={"username": "testuser", "password": "123"})
    token = login_response.json()["access_token"]

    # Créer 5 transactions
    for i in range(5):
        client.post("/api/transactions/",
                    json={"title": f"Transaction {i}", "amount": 100.0, "category": "expense", "description": "Test"},
                    headers={"Authorization": f"Bearer {token}"})

    # Tester skip et limit
    response = client.get("/api/transactions/?skip=2&limit=2", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 2


def test_login_wrong_password():
    """Test de connexion avec mauvais mot de passe"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "correctpassword"})

    response = client.post("/api/auth/login", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401


def test_login_user_not_found():
    """Test de connexion avec utilisateur inexistant"""
    response = client.post("/api/auth/login", data={"username": "nonexistent", "password": "password"})
    assert response.status_code == 401


def test_access_protected_route_without_token():
    """Test d'accès à une route protégée sans token"""
    response = client.get("/api/transactions/")
    assert response.status_code == 401


def test_access_protected_route_with_invalid_token():
    """Test d'accès avec token invalide"""
    response = client.get("/api/transactions/", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_register_duplicate_username():
    """Test de création d'un utilisateur avec username déjà pris"""
    # Créer le premier utilisateur
    client.post("/api/auth/register",
                json={"email": "user1@example.com", "username": "testuser", "password": "password123"})

    # Essayer avec un autre email mais même username
    response = client.post("/api/auth/register",
                           json={"email": "user2@example.com", "username": "testuser", "password": "password123"})

    assert response.status_code == 400
    assert "nom d'utilisateur" in response.json()["detail"].lower()


def test_create_transaction_invalid_category():
    """Test de création d'une transaction avec catégorie invalide"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    login_response = client.post("/api/auth/login", data={"username": "testuser", "password": "123"})
    token = login_response.json()["access_token"]

    # Essayer de créer une transaction avec catégorie invalide
    response = client.post("/api/transactions/",
                           json={"title": "Test", "amount": 100.0, "category": "invalid_category",
                                 "description": "Test"},
                           headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    assert "catégorie" in response.json()["detail"].lower()


def test_get_single_transaction_by_id():
    """Test de récupération d'une transaction spécifique par ID"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    login_response = client.post("/api/auth/login", data={"username": "testuser", "password": "123"})
    token = login_response.json()["access_token"]

    # Créer une transaction
    create_response = client.post("/api/transactions/",
                                  json={"title": "Salaire", "amount": 3000.0, "category": "income",
                                        "description": "Test"},
                                  headers={"Authorization": f"Bearer {token}"})

    transaction_id = create_response.json()["id"]

    # Récupérer cette transaction spécifique
    response = client.get(f"/api/transactions/{transaction_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["id"] == transaction_id
    assert response.json()["title"] == "Salaire"


def test_get_summary():
    """Test du résumé des transactions"""
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    login_response = client.post("/api/auth/login", data={"username": "testuser", "password": "123"})
    token = login_response.json()["access_token"]

    # Créer des transactions
    client.post("/api/transactions/",
                json={"title": "Salaire", "amount": 3000.0, "category": "income", "description": "Test"},
                headers={"Authorization": f"Bearer {token}"})

    client.post("/api/transactions/",
                json={"title": "Courses", "amount": 500.0, "category": "expense", "description": "Test"},
                headers={"Authorization": f"Bearer {token}"})

    # Récupérer le résumé
    response = client.get("/api/transactions/stats/summary", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 3000.0
    assert data["total_expense"] == 500.0
    assert data["balance"] == 2500.0
    assert data["transaction_count"] == 2


def test_token_with_username_none():
    """Test d'un token avec username None (cas edge)"""
    # Créer un token invalide manuellement avec username = None
    from app.auth import create_access_token
    from datetime import timedelta

    # Token avec sub=None
    invalid_token = create_access_token(data={"sub": None}, expires_delta=timedelta(minutes=15))

    response = client.get("/api/transactions/", headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401


def test_token_without_expires_delta():
    """Test de création de token sans expires_delta"""
    from app.auth import create_access_token

    # Créer un token sans spécifier expires_delta (utilise la valeur par défaut)
    token = create_access_token(data={"sub": "testuser"})

    # Le token devrait être valide
    assert token is not None
    assert len(token) > 0


def test_expired_token():
    """Test avec un token expiré"""
    from app.auth import create_access_token
    from datetime import timedelta

    # Créer un utilisateur
    client.post("/api/auth/register",
                json={"email": "test@example.com", "username": "testuser", "password": "123"})

    # Créer un token qui expire immédiatement (dans le passé)
    expired_token = create_access_token(
        data={"sub": "testuser"},
        expires_delta=timedelta(seconds=-1)  # Expire dans le passé
    )

    # Essayer d'utiliser le token expiré
    response = client.get("/api/transactions/", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401


def test_malformed_token():
    """Test avec un token complètement invalide (malformé)"""
    # Token qui va causer une JWTError lors du décodage
    malformed_tokens = [
        "completely_invalid_token",
        "not.a.jwt",
        "abc.def.ghi",
        "",
    ]

    for bad_token in malformed_tokens:
        response = client.get("/api/transactions/", headers={"Authorization": f"Bearer {bad_token}"})
        assert response.status_code == 401


def test_token_with_missing_sub():
    """Test d'un token sans le champ 'sub' (username)"""
    from app.auth import SECRET_KEY, ALGORITHM
    from jose import jwt
    from datetime import datetime, timedelta, timezone

    # Créer un token SANS le champ "sub"
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        "iat": datetime.now(timezone.utc)
        # Pas de "sub" !
    }
    token_without_sub = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    response = client.get("/api/transactions/", headers={"Authorization": f"Bearer {token_without_sub}"})
    assert response.status_code == 401


def test_token_signed_with_wrong_key():
    """Test d'un token signé avec une mauvaise clé"""
    from jose import jwt
    from datetime import datetime, timedelta, timezone
    from app.auth import ALGORITHM

    # Créer un token avec une MAUVAISE clé secrète
    wrong_secret = "wrong_secret_key_123456789"
    payload = {
        "sub": "testuser",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    wrong_token = jwt.encode(payload, wrong_secret, algorithm=ALGORITHM)

    response = client.get("/api/transactions/", headers={"Authorization": f"Bearer {wrong_token}"})
    assert response.status_code == 401

