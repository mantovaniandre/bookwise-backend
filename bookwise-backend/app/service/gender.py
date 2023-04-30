from repository.gender import GenderRepository
from util.exception.custom_exception import GenderValidationError, GenderNotFoundError

gender_repository = GenderRepository()


class GenderService:
    @staticmethod
    def validate_gender(gender):
        if gender == 'MASCULINE':
            return True
        if gender == 'FEMININE':
            return True
        else:
            raise GenderValidationError(gender)

    @staticmethod
    def find_id(gender):
        gender_description_id = gender_repository.get_id_gender_by_description(gender)
        if gender_description_id is False:
            raise GenderNotFoundError(gender)
        return gender_description_id
