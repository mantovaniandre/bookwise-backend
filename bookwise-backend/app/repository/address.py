from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from sqlalchemy import text
from model.address import Address
from util.exception.custom_exception import AddressSaveError, AddressDeletionError, DatabaseError

# created instances
session = Session()


class AddressRepository:
    @staticmethod
    def save_address(new_address):
        try:
            session.add(new_address)
            session.commit()
            session.refresh(new_address)
            address_id = new_address.id
            if address_id is not None:
                return address_id
            else:
                session.rollback()
                raise AddressSaveError()
        except Exception as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

    @staticmethod
    def delete_address_by_id(address_id):
        try:
            with Session() as session:
                address = session.query(Address).filter_by(id=address_id).first()
                if address is not None:
                    session.delete(address)
                    session.commit()
                    return True
                else:
                    raise AddressDeletionError(address_id)
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))

    @staticmethod
    def update_address(table_name, address_id, **update_values):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"UPDATE {table_name} SET last_update = '{now}', "
        for column, value in update_values.items():
            query += f"{column} = '{value}', "
        query = query[:-2]
        query += f" WHERE id = {address_id};"
        query = text(query)
        try:
            session.execute(query)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

    @staticmethod
    def get_address_by_id_of_user(user_id):
        try:
            address = session.query(Address).filter_by(id=user_id).first()
            if address is not None:
                return address
            else:
                return False
        except Exception as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()
