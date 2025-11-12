from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# Schémas pour User
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Schémas pour Transaction
class TransactionBase(BaseModel):
    title: str
    amount: float
    category: str  # "income" ou "expense"
    description: Optional[str] = None

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

class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int
    date: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)

# Schémas pour Authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
