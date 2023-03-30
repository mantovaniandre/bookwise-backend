from repository.gender import GenderRepository

gender_repository = GenderRepository()


class GenderService:
    @staticmethod
    def validate_gender(description):
        if description == 'Masculine':
            return True
        if description == 'Feminine':
            return True
        else:
            raise ValueError(f"The usertype: '{description}' not exists.")

    @staticmethod
    def find_id(description):
        gender_description_id = gender_repository.get_id_gender_by_description(description)
        if gender_description_id is False:
            raise ValueError(f"The gender: '{description}' not exists to found id.")
        return gender_description_id
