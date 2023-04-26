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

            user = login_repository.get_user_by_email(email_login_upper)
            email_is_true = LoginService.verify_email(user.email)

            password_is_true = LoginService.verify_password(password_login, user.password)

            if email_is_true and password_is_true:
                token = LoginService.generate_token(user)
                if isinstance(token, bytes):
                    token_decode = token.decode('utf-8')
                else:
                    token_decode = token
                user.token = token_decode
                session.add(user)
                session.commit()
                return token_decode
            else:
                raise ValueError(f"Invalid Credential")
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
    def generate_token(user_id):
        exp = data_time_conversion.dataTimeConversionToSaoPaulo() + datetime.timedelta(minutes=30)
        payload = {
            'user_id': user_id.id,
            'cpf': user_id.cpf,
            'exp': exp.timestamp()
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
