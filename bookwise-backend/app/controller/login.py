from service.login import LoginService
from util.exception.custom_exception import MissingCredentialsError, InvalidCredentialsError, InternalError

login_service = LoginService()


class LoginController:
    @staticmethod
    def login(request_data):
        try:
            token = login_service.login(request_data)
            return token
        except MissingCredentialsError as e:
            raise MissingCredentialsError()
        except InvalidCredentialsError as e:
            raise InvalidCredentialsError()
        except InternalError as e:
            raise InternalError(str(e))


