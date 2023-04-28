from configuration.database import Session
from model.user import User

# created instances
session = Session()


class UserRepository:
    @staticmethod
    def get_user_by_email(email):
        try:
            email_exists = session.query(User).filter_by(email=email).first()
            if email_exists is None:
                return True
            else:
                session.rollback()
                return False
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

    @staticmethod
    def get_user_by_id(get_id_token):
        try:
            token_user = session.query(User).filter_by(id=get_id_token).first()
            if token_user is None:
                return False
            else:
                session.rollback()
                return token_user
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

    @staticmethod
    def get_user_by_cpf(cpf):
        try:
            cpf_exists = session.query(User).filter_by(cpf=cpf).first()
            if cpf_exists is None:
                return True
            else:
                session.rollback()
                return False
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

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
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

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
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

    @staticmethod
    def update_user(table_name, user_id, **update_values):
        query = f"UPDATE {table_name} SET "
        for column, value in update_values.items():
            query += f"{column}='{value}', "
        query = query[:-2]
        query += f"WHERE id = {user_id};"
        session.execute(query)
        session.commit()

    @staticmethod
    def update_user_usertype(table_name, user_id, usertype_id):
        query = f"UPDATE {table_name} SET usertype = {usertype_id}"
        query += f"WHERE id = {user_id};"
        session.execute(query)
        session.commit()

    @staticmethod
    def update_user_gender(table_name, user_id, usertype_id):
        query = f"UPDATE {table_name} SET usertype = {usertype_id}"
        query += f"WHERE id = {user_id};"
        session.execute(query)
        session.commit()


