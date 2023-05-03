from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from model.user import User
from util.exception.custom_exception import UserNotFoundEmailError, DatabaseError

# created instances
session = Session()


class LoginRepository:
    @staticmethod
    def get_user_by_email(email):
        try:
            user = session.query(User).filter_by(email=email).first()
            if user is None:
                raise UserNotFoundEmailError(email)
            return user
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()



