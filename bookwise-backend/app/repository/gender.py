from configuration.database import Session
from model.gender import Gender
from util.exception.custom_exception import GenderNotFoundError, DatabaseError


class GenderRepository:
    @staticmethod
    def get_id_gender_by_description(description):
        with Session() as session:
            gender = session.query(Gender).filter_by(description=description).first()
            if gender is None:
                raise GenderNotFoundError(description)
            else:
                return gender.id

