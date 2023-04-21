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

    top_up_balance = "/balance/top-up/"
    withdraw_balance = "/balance/withdraw/"
    deposit = "/balance/deposit/"
    history = "/balance/history/"
