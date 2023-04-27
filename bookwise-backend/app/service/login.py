import bcrypt
from configuration.database import Session
from repository.login import LoginRepository
import datetime
from flask import current_app
from util.datatime.data_time_conversion import DataTimeConversion
import jwt

# created instances
session = Session()
login_repository = LoginRepository()

data_time_conversion = DataTimeConversion()


class LoginService:
    @staticmethod
    def login(user_data):
        try:
            email_login = user_data.get('email')
            password_login = user_data.get('password')

            if not email_login or not password_login:
                raise ValueError("Email and password are required")

            email_login_upper = email_login.upper()
            user = login_repository.get_user_by_email(email_login_upper)

            if not user:
                raise ValueError("Invalid Credential")

            password_is_true = LoginService.verify_password(password_login, user.password)

            if password_is_true:
                secret_key = current_app.config['JWT_SECRET_KEY']
                token = LoginService.generate_token(user, secret_key)
                user.token = token
                session.add(user)
                session.commit()
                return token
            else:
                raise ValueError("Invalid Credential")
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal error: {e}")
        finally:
            session.close()

    @staticmethod
    def verify_email(email):
        email_exists = login_repository.get_user_by_email(email)
        if email_exists:
            return True
        else:
            return False

    @staticmethod
    def verify_password(password_login, user_password):
        password_login_encoded = password_login.encode('utf-8')
        user_password_encoded = user_password.encode('utf-8')
        password_correct = bcrypt.checkpw(password_login_encoded, user_password_encoded)
        if password_correct:
            return True
        else:
            raise ValueError(f"failed password check")

    @staticmethod
    def generate_token(user, secret_key):
        exp = data_time_conversion.dataTimeConversionToSaoPaulo() + datetime.timedelta(minutes=30)
        payload = {
            'sub': user.id,
            'cpf': user.cpf,
            'exp': exp.timestamp()
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
