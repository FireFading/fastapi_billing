from dataclasses import dataclass


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
