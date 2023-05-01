from configuration.database import Session
from service.login import LoginService

login_service = LoginService()
session = Session()


class LoginController:
    @staticmethod
    def login(request_data):
        try:
            token = login_service.login(request_data)
            return token
        except Exception as e:
            session.rollback()
            raise e


