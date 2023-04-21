from dataclasses import dataclass


@dataclass
class Messages:
    USER_NOT_FOUND = "User with this email not found"
    USER_ALREADY_EXISTS = "User with this email already exists"
    USER_LOGOUT = "User logout"
    USER_CREATED = "User successfully created"

    INVALID_TOKEN = "Invalid token"

    PROFILE_DELETED = "User deleted"

    WRONG_PASSWORD = "Wrong password"
    WRONG_OLD_PASSWORD = "Wrong old password"
    PASSWORDS_NOT_MATCH = "Passwords don't match"
    PASSWORD_RESET = "Password reset"
    NEW_PASSWORD_SIMILAR_OLD = "New password is similar to old one"
    PASSWORD_UPDATED = "Password successfully updated"

    BALANCE_NOT_FOUND = "Balance not found"
    BALANCE_ALREADY_EXISTS = "Balance already exists"
    BALANCE_CREATED = "Balance successfully created"
    BALANCE_TOP_UP = "Balance top up"
    INSUFFICIENT_FUNDS = "Insufficient funds"
    BALANCE_WITHDRAW = "Balance withdraw"

    ACCESS_DENIED = "Access denied"


messages = Messages()
