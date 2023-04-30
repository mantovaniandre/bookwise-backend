from configuration.database import Session
from model.gender import Gender
from util.exception.custom_exception import GenderNotFoundError, DatabaseError

# created instances
session = Session()


class GenderRepository:
    @staticmethod
    def get_id_gender_by_description(description):
        try:
            gender = session.query(Gender).filter_by(description=description).first()
            if gender is None:
                raise GenderNotFoundError(description)
            else:
                return gender.id
        except Exception as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

