from configuration.database import Session
from model.usertype import UserType
from sqlalchemy import exc

# created instances
session = Session()


class UsertypeRepository:
    @staticmethod
    def get_id_usertype_by_description(description):
        try:
            description_found = session.query(UserType).filter_by(description=description).first()
            session.commit()
            if description_found is not None:
                return description_found.id
            else:
                return False
            session.close()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise f"Internal error: {e}"
