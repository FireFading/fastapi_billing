from dataclasses import dataclass
from datetime import datetime

import jwt
from app.config import settings
from app.controllers.users import user_controller


@dataclass
class User:
    email = "test@mail.ru"
    password = "TestPassword123!"
    name = "TestName"
    phone = "89999999999"
    wrong_password = "WrongPassword123@"
    new_password = "NewPassword123@"


@dataclass
class Urls:
    login = "/accounts/login/"
    register = "/accounts/register/"
    logout = "/accounts/logout/"
    change_password = "/accounts/change-password/"
    info = "/accounts/info/"
    forgot_password = "/accounts/forgot-password/"
    reset_password = "/accounts/reset-password/"

    create_balance = "/balance/create/"
    top_up_balance = "/balance/top-up/"
    withdraw_balance = "/balance/withdraw/"
    deposit = "/balance/deposit/"
    history = "/balance/history/"

    transfer = "/transfers/"


def create_fake_token(
    expires_in: datetime = datetime(1999, 1, 1), email: str = User.email
) -> str:
    to_encode = {"exp": expires_in, "email": email, "is_active": True}
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)


reset_password_token = user_controller.create_token(email=User.email)

register_user_schema = {
    "email": User.email,
    "name": User.name,
    "phone": User.phone,
    "password": User.password,
}

register_user_schema2 = {
    "email": "another@mail.ru",
    "name": User.name,
    "phone": "891209029301",
    "password": User.password,
}

login_credentials_schema = {"email": User.email, "password": User.password}
login_credentials_schema2 = {
    "email": register_user_schema2.get("email"),
    "password": User.password,
}

wrong_login_credentials_schema = {"email": User.email, "password": User.wrong_password}

top_up_balance_schema = {"amount": 100}
withdraw_balance_schema = {"amount": 10}

transfer_schema = {"to": register_user_schema2.get("email"), "amount": 70}

balance_after_transactions = top_up_balance_schema.get(
    "amount"
) - withdraw_balance_schema.get("amount")

change_password_schema = {
    "old_password": User.password,
    "password": User.new_password,
    "confirm_password": User.new_password,
}

wrong_change_password_schema = {
    "old_password": User.password,
    "password": User.new_password,
    "confirm_password": User.wrong_password,
}

wrong_old_password_schema = {
    "old_password": User.wrong_password,
    "password": User.wrong_password,
    "confirm_password": User.wrong_password,
}

only_old_passwords_schema = {
    "old_password": User.password,
    "password": User.password,
    "confirm_password": User.password,
}
