import uuid
from datetime import datetime

from app.schemas.balance import Balance
from app.schemas.base import CustomConfig
from app.utils.validators import validate_name, validate_password
from pydantic import BaseModel, EmailStr, validator


class Email(CustomConfig):
    email: EmailStr


class LoginCredentials(Email, BaseModel):
    password: str


class Phone(BaseModel):
    phone: str


class Name(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, name: str | None = None) -> str | None | ValueError:
        return validate_name(name=name)


class CreateUser(Email, Name, Phone, BaseModel):
    password: str

    @validator("password")
    def validate_password(cls, password: str) -> str | ValueError:
        return validate_password(password=password)


class ShowUserOwnTransaction(CustomConfig):
    amount: float
    timestamp: datetime


class User(CustomConfig):
    guid: uuid.UUID
    email: EmailStr | None
    phone: str | None
    name: str | None

    balance: Balance

    transactions: list[ShowUserOwnTransaction]


class UpdatePassword(BaseModel):
    old_password: str
    password: str
    confirm_password: str

    @validator("confirm_password", "password")
    def validate_password(cls, password: str) -> str | ValueError:
        return validate_password(password=password)
