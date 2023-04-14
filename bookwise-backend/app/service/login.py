import bcrypt

from configuration.database import Session
from repository.login import LoginRepository

import datetime
from flask import request, jsonify
from functools import wraps
from configuration.secret_key import SECRET_KEY
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
            email_login = user_data['email']
            email_login_upper = email_login.upper()
            password_login = user_data['password']
            password_login_encrypt = LoginService.encrypt_password(password_login)

            user = login_repository.get_user_by_email(email_login_upper)
            email_is_true = LoginService.verify_email(user.email)

            user_password_encrypted = bcrypt.hashpw(password_login.encode('utf-8'), bcrypt.gensalt())
            password_teste_database = user.password
            # Comparar senhas criptografadas
            password_from_database = "$2b$12$4WMP2QkxFnh6MP80MMfZYOivFFgHTOLZYSI0gJ2YUcqiq0V6Rh6pq"

            print(password_teste_database)
            print(password_from_database)
            passwords_match = bcrypt.checkpw(password_login.encode('utf-8'), password_from_database.encode('utf-8'))

            if passwords_match:
                print("Senha correta!")
            else:
                print("Senha incorreta!")

            password_is_true = LoginService.verify_password(user.password, password_login_encrypt)

            if email_is_true and password_is_true:
                token = LoginService.generate_token(user.id)
                token_decode = token.decode('utf-8')
                return token_decode
            else:
                raise ValueError(f"Invalid Credential")
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal error: {e}")

    @staticmethod
    def verify_email(email):
        email_exists = login_repository.get_user_by_email(email)
        if email_exists:
            return True
        else:
            return False

    @staticmethod
    def verify_password(password_login_encrypt, user_password):
        password_correct = bcrypt.checkpw(password_login_encrypt.encode('utf-8'), user_password.encode('utf-8'))
        if password_correct:
            return password_correct
        else:
            raise ValueError(f"failed password check")

    @staticmethod
    def generate_token(user_id):
        payload = {
            'exp': data_time_conversion + datetime.timedelta(days=1),
            'iat': data_time_conversion,
            'sub': user_id
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'mensagem': 'Token de autenticação ausente'}), 401
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_id = payload['sub']
            except jwt.ExpiredSignatureError:
                return jsonify({'mensagem': 'Token expirado'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'mensagem': 'Token inválido'}), 401
            return f(user_id, *args, **kwargs)
        return decorator

    @staticmethod
    def encrypt_password(password):
        salt = bcrypt.gensalt(rounds=12)
        encrypt_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        encrypted_password = encrypt_password.decode('utf-8')
        return encrypted_password
