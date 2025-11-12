from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    
    # Relations
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)  # "income" ou "expense"
    description = Column(String(500), nullable=True)
    date = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relations
    owner = relationship("User", back_populates="transactions")