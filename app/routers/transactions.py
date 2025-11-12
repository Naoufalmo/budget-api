from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Transaction, User
from app.schemas import TransactionCreate, TransactionResponse, TransactionUpdate
from app.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
        transaction: TransactionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Créer une nouvelle transaction financière pour l'utilisateur connecté.

    La transaction est automatiquement associée à l'utilisateur authentifié.
    La catégorie doit être soit 'income' (revenu) soit 'expense' (dépense).

    Args:
        transaction: Données de la transaction (title, amount, category, description)
        db: Session de base de données (injectée automatiquement)
        current_user: Utilisateur authentifié (extrait du token JWT)

    Returns:
        Transaction créée avec son ID et la date de création

    Raises:
        HTTPException 400: Catégorie invalide (doit être 'income' ou 'expense')
        HTTPException 401: Token JWT invalide ou expiré
    """
    # Valider la catégorie
    if transaction.category not in ["income", "expense"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La catégorie doit être 'income' ou 'expense'"
        )

    db_transaction = Transaction(
        **transaction.model_dump(),
        user_id=current_user.id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
        skip: int = 0,
        limit: int = 100,
        category: str = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Récupérer la liste des transactions de l'utilisateur avec filtres et pagination.

    Permet de filtrer par catégorie et de paginer les résultats pour
    une meilleure performance avec de grandes quantités de données.

    Args:
        skip: Nombre de transactions à ignorer (pour la pagination)
        limit: Nombre maximum de transactions à retourner (max 100)
        category: Filtre optionnel par catégorie ('income' ou 'expense')
        db: Session de base de données
        current_user: Utilisateur authentifié

    Returns:
        Liste des transactions correspondant aux critères de recherche

    Raises:
        HTTPException 401: Token JWT invalide ou expiré
    """
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    )

    # Filtrer par catégorie si spécifié
    if category:
        query = query.filter(Transaction.category == category)

    transactions = query.offset(skip).limit(limit).all()

    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
        transaction_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Récupérer une transaction spécifique par son ID.

    Seules les transactions appartenant à l'utilisateur connecté peuvent
    être consultées, garantissant la confidentialité des données.

    Args:
        transaction_id: ID unique de la transaction à récupérer
        db: Session de base de données
        current_user: Utilisateur authentifié

    Returns:
        Transaction demandée avec tous ses détails

    Raises:
        HTTPException 401: Token JWT invalide ou expiré
        HTTPException 404: Transaction non trouvée ou n'appartient pas à l'utilisateur
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction non trouvée"
        )

    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
        transaction_id: int,
        transaction_update: TransactionUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Mettre à jour une transaction existante.

    Permet de modifier partiellement ou totalement une transaction.
    Seuls les champs fournis dans la requête seront mis à jour.

    Args:
        transaction_id: ID de la transaction à modifier
        transaction_update: Nouvelles données (champs optionnels)
        db: Session de base de données
        current_user: Utilisateur authentifié

    Returns:
        Transaction mise à jour avec les nouvelles valeurs

    Raises:
        HTTPException 401: Token JWT invalide ou expiré
        HTTPException 404: Transaction non trouvée ou n'appartient pas à l'utilisateur
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction non trouvée"
        )

    # Mettre à jour uniquement les champs fournis
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
        transaction_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Supprimer définitivement une transaction.

    Cette action est irréversible. La transaction sera définitivement
    supprimée de la base de données.

    Args:
        transaction_id: ID de la transaction à supprimer
        db: Session de base de données
        current_user: Utilisateur authentifié

    Returns:
        Aucun contenu (HTTP 204)

    Raises:
        HTTPException 401: Token JWT invalide ou expiré
        HTTPException 404: Transaction non trouvée ou n'appartient pas à l'utilisateur
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction non trouvée"
        )

    db.delete(transaction)
    db.commit()

    return None


@router.get("/stats/summary")
def get_summary(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Obtenir un résumé statistique des finances de l'utilisateur.

    Calcule et retourne les totaux des revenus, des dépenses, le solde
    et le nombre total de transactions pour l'utilisateur connecté.

    Args:
        db: Session de base de données
        current_user: Utilisateur authentifié

    Returns:
        dict: Dictionnaire contenant:
            - total_income (float): Somme de tous les revenus
            - total_expense (float): Somme de toutes les dépenses
            - balance (float): Différence entre revenus et dépenses
            - transaction_count (int): Nombre total de transactions

    Raises:
        HTTPException 401: Token JWT invalide ou expiré
    """
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).all()

    total_income = sum(t.amount for t in transactions if t.category == "income")
    total_expense = sum(t.amount for t in transactions if t.category == "expense")
    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "transaction_count": len(transactions)
    }