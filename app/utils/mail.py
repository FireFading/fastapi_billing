from app.config import settings
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


async def send_mail(subject: str, recipients: list, body: str):
    message = MessageSchema(subject=subject, recipients=recipients, body=body, subtype="html")
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_STARTTLS=settings.mail_starttls,
        MAIL_SSL_TLS=settings.mail_ssl_tls,
        MAIL_FROM=settings.mail_from,
        MAIL_FROM_NAME=settings.mail_from_name,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=settings.mail_validate_certs,
    )
    mail = FastMail(conf)
    await mail.send_message(message)


def html_reset_password_mail(reset_password_token: str):
    return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Восстановление пароля</title>
        </head>
        <body>
            <h3>С вашего аккаунта пришел запрос на сброс пароля</h3>
            <p>Для продолжения перейдите по
                <a href="{settings.domain_name}/reset-password/{reset_password_token}"> ссылке</a>
            </p>
            <p>Если это были не Вы, смените пароль</p>
        </body>
        </html>
        """
