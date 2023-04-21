from dataclasses import dataclass


@dataclass
class User:
    email = "test@mail.ru"
    password = "TestPassword123!"
    name = "TestName"
    phone = "89999999999"
    wrong_password = "WrongPassword"


@dataclass
class Urls:
    login = "/accounts/login/"
    register = "/accounts/register/"
    logout = "/accounts/logout/"
    info = "/accounts/info/"

    create_balance = "/balance/create/"
    top_up_balance = "/balance/top-up/"
    withdraw_balance = "/balance/withdraw/"
    deposit = "/balance/deposit/"
    history = "/balance/history/"


register_user_schema = {
    "email": User.email,
    "name": User.name,
    "phone": User.phone,
    "password": User.password,
}

login_credentials_schema = {"email": User.email, "password": User.password}

wrong_login_credentials_schema = {"email": User.email, "password": User.wrong_password}

top_up_balance_schema = {"amount": 100}
withdraw_balance_schema = {"amount": -10}
