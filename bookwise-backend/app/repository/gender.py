from configuration.database import Session
from model.gender import Gender

# created instances
session = Session()


class GenderRepository:
    @staticmethod
    def get_id_gender_by_description(description):
        try:
            description_found = session.query(Gender).filter_by(description=description).first()
            session.commit()
            if description_found is not None:
                return description_found.id
            else:
                return False
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()
