from service.login import LoginService

login_service = LoginService()


class LoginController:
    @staticmethod
    def login(user_data):
        try:
            token = login_service.login(user_data)
            return token
        except Exception as e:
            raise ValueError(f"{e}")



