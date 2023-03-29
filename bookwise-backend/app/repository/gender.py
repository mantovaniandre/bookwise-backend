from configuration.database import Session
from model.gender import Gender
from sqlalchemy import exc

# created instances
session = Session()


class GenderRepository:
    @staticmethod
    def get_id_gender_by_description(description):
        try:
            description_found = session.query(Gender).filter_by(description=description).first()
            session.commit()
            session.close()
            if description_found is not None:
                return description_found.id
            else:
                return False
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise f"Internal error: {e}"
