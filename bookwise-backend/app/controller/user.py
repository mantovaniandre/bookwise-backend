from sqlalchemy.exc import SQLAlchemyError, DatabaseError
from configuration.database import Session
from service.user import UserService
from util.exception.custom_exception import UserCreationError, UserUpdateError

session = Session()


class UserController:
    @staticmethod
    def create_user(request_data):
        try:
            UserService.create_user(request_data)
            return True
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def update_user(request_data, id_user_token):
        try:
            UserService.update_user(request_data, id_user_token)
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_profile_user(id_token):
        try:
            user = UserService.get_profile_user(id_token)
            return user
        except Exception as e:
            session.rollback()
            raise e
