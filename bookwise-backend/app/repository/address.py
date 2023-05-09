from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from model.address import Address
from util.exception.custom_exception import AddressSaveError, AddressDeletionError, DatabaseError, AddressUpdatingError, \
    GetAddressByIdOfUserError


class AddressRepository:
    @staticmethod
    def save_address(new_address):
        try:
            with Session() as session:
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
            raise DatabaseError(str(e))

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
    def update_address(address_id, **update_values):
        with Session() as session:
            try:
                address = session.query(Address).filter_by(id=address_id).first()
                if not address:
                    raise AddressUpdatingError(address_id)
                for column, value in update_values.items():
                    setattr(address, column, value)
                address.last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def get_address_by_id_of_user(user_id):
        with Session() as session:
            try:
                address = session.query(Address).filter_by(id=user_id).first()
                if address is not None:
                    return address
                else:
                    raise GetAddressByIdOfUserError(user_id)
            except Exception as e:
                session.rollback()
                raise DatabaseError(str(e))
