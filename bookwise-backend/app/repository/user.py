from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from model.user import User
from sqlalchemy.orm import joinedload
from sqlalchemy import text

from util.exception.custom_exception import UserNotFoundEmailError, DatabaseError, UserNotFoundIdError, UserCPFError, \
    UserCreationError, UserDeletionError

# created instances
session = Session()


class UserRepository:
    @staticmethod
    def get_user_by_email_to_validate_email_exist(email):
        with Session() as session:
            try:
                user = session.query(User).filter_by(email=email).first()
                if user is None:
                    return True
                else:
                    return False
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def get_user_by_cpf_to_update(cpf):
        with Session() as session:
            query = text('SELECT * FROM users WHERE cpf=:cpf')
            values = {'cpf': cpf}
            try:
                result = session.execute(query, values)
                user_data = result.fetchone()
            except Exception as e:
                raise DatabaseError(str(e))
            return user_data

    @staticmethod
    def get_user_by_email_to_update(email):
        with Session() as session:
            query = text('SELECT * FROM users WHERE email=:email')
            values = {'email': email}
            try:
                result = session.execute(query, values)
                user_data = result.fetchone()
            except Exception as e:
                raise DatabaseError(str(e))
            return user_data

    @staticmethod
    def get_user_by_id(user_id):
        with Session() as session:
            try:
                user = session.query(User).options(
                    joinedload(User.address),
                    joinedload(User.user_type),
                    joinedload(User.gender),
                    joinedload(User.credit_card)
                ).filter_by(id=user_id).first()
                if not user:
                    raise UserNotFoundIdError(user_id)
                return user
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def get_user_by_cpf_to_validate_cpf_exist(cpf):
        with Session() as session:
            try:
                user = session.query(User).filter_by(cpf=cpf).first()
                if user is None:
                    return True
                else:
                    return False
            except Exception as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def create_user_to_database(new_user):
        with Session() as session:
            try:
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                user_id = new_user.id
                if user_id is not None:
                    return True
                else:
                    session.rollback()
                    raise UserCreationError()
            except Exception as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def update_user(table_name, book_id, **update_values):
        with Session() as session:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = f"UPDATE {table_name} SET last_update = '{now}', "
            for column, value in update_values.items():
                query += f"{column} = '{value}', "
            query = query[:-2]
            query += f" WHERE id = {book_id};"
            query = text(query)
            try:
                session.execute(query)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def update_user_type_of_user(table_users, user_id, user_type_id):
        with Session() as session:
            try:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = f"UPDATE {table_users} SET user_type_id = {user_type_id}, last_update = '{now}' "
                query += f" WHERE id = {user_id};"
                query = text(query)
                session.execute(query)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def update_gender_of_user(table_users, user_id, gender_id):
        with Session() as session:
            try:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = f"UPDATE {table_users} SET gender_id = {gender_id}, last_update = '{now}' "
                query += f" WHERE id = {user_id};"
                query = text(query)
                session.execute(query)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def delete_user_by_id(user_id):
        with Session() as session:
            try:
                user = session.query(User).filter_by(id=user_id).first()
                if user is not None:
                    session.delete(user)
                    session.commit()
                    return True
                else:
                    raise UserDeletionError(user_id)
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))
