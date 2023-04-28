from configuration.database import Session

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
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

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
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

    @staticmethod
    def update_address(table_name, address_id, **update_values):
        query = f"UPDATE {table_name} SET "
        for column, value in update_values.items():
            query += f"{column}='{value}', "
        query = query[:-2]
        query += f"WHERE id = {address_id};"
        session.execute(query)
        session.commit()
