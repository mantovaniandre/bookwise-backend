from configuration.database import Session
from sqlalchemy import exc

from model.address import Address

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
                return False
            session.close()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise f"Internal error: {e}"

    @staticmethod
    def delete_address_by_id(address_id):
        try:
            address = session.query(Address).filter_by(id=address_id).first()
            if address is not None:
                session.delete(address)
                session.commit()
                return True
            else:
                return False
            session.close()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise f"Internal error: {e}"


