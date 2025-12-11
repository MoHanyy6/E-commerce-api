# from pydantic_settings import BaseSettings
# from fastapi_mail import ConnectionConfig

# class Settings(BaseSettings):
#     database_hostname: str
#     database_password: str
#     database_port: int
#     database_name: str
#     database_username: str
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int

#     class Config:
#         env_file = ".env"

# settings = Settings()

# EMAIL_CONFIG = ConnectionConfig(
#     MAIL_USERNAME="mohamedfoo27@gmail.com",
#     MAIL_PASSWORD="your_app_password",
#     MAIL_FROM="mohamedfoo27@gmail.com",
#     MAIL_PORT=587,
#     MAIL_STARTTLS=True,       # use this instead of MAIL_TLS
#     MAIL_SSL_TLS=False,        # use this instead of MAIL_SSL
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True
# )
from pydantic_settings import BaseSettings
from fastapi_mail import ConnectionConfig

class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_port: int
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

EMAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME="mohamedfoo27@gmail.com",
    MAIL_PASSWORD="vguq rwfx txse swuq",  # Use app password for Gmail
    MAIL_FROM="mohamedfoo27@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",        # REQUIRED
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
