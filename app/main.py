# app/main.py - Point d'entrée de l'API Budget

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, transactions

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Budget API",
    description="API de gestion de budget personnel",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])

@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API Budget!",
        "documentation": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
