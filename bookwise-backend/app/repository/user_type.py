from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from model.user_type import UserType
from util.exception.custom_exception import UserTypeNotFoundError, DatabaseError, UserTypeCreationError

# created instances
session = Session()


class UsertypeRepository:
    @staticmethod
    def get_id_user_type_by_description(description):
        try:
            user = session.query(UserType.id).filter_by(description=description).first()
            if user is None:
                return UserTypeNotFoundError(description)
            else:
                return user.id
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

    @staticmethod
    def save_user_type(new_usertype):
        try:
            session.add(new_usertype)
            session.commit()
            session.refresh(new_usertype)
            usertype_id = new_usertype.id
            if usertype_id is not None:
                return usertype_id
            else:
                session.rollback()
                raise UserTypeCreationError()
        except Exception as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()
