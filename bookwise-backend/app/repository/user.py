from configuration.database import Session
from sqlalchemy import exc
from model.user import User

# created instances
session = Session()


class UserRepository:
    @staticmethod
    def get_user_by_email(email):
        try:
            email_exists = session.query(User).filter_by(email=email).first()
            session.close()
            if email_exists is None:
                return True
            else:
                session.rollback()
                return False
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise f"Internal error: {e}"

    @staticmethod
    def get_user_by_cpf(cpf):
        try:
            cpf_exists = session.query(User).filter_by(cpf=cpf).first()
            session.close()
            if cpf_exists is None:
                return True
            else:
                session.rollback()
                return False
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise f"Internal error: {e}"

    @staticmethod
    def save_user_to_database(new_user):
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            user_id = new_user.id
            if user_id is not None:
                return True
            else:
                session.rollback()
                return False
            session.close()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise f"Internal error: {e}"

    @staticmethod
    def save_usertype(new_usertype):
        try:
            session.add(new_usertype)
            session.commit()
            session.refresh(new_usertype)
            usertype_id = new_usertype.id
            if usertype_id is not None:
                return usertype_id
            else:
                session.rollback()
                return False
            session.close()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise f"Internal error: {e}"

