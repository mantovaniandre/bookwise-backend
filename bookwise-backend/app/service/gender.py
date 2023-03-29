from repository.gender import GenderRepository
from util.exception.custom_exception import ValidateGenderError, DescriptionGenderError

gender_repository = GenderRepository()


class GenderService:
    @staticmethod
    def validate_gender(description):
        if description == 'Masculine':
            return True
        if description == 'Feminine':
            return True
        else:
            raise ValidateGenderError(description)

    @staticmethod
    def find_id(description):
        gender_description_id = gender_repository.get_id_gender_by_description(description)
        if gender_description_id is False:
            raise DescriptionGenderError(description)
        return gender_description_id
