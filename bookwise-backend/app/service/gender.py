from repository.gender import GenderRepository

gender_repository = GenderRepository()


class GenderService:
    @staticmethod
    def validate_gender(gender):
        if gender == 'MASCULINE':
            return True
        if gender == 'FEMININE':
            return True
        else:
            raise ValueError(f"The usertype: '{gender}' not exists.")

    @staticmethod
    def find_id(gender):
        gender_description_id = gender_repository.get_id_gender_by_description(gender)
        if gender_description_id is False:
            raise ValueError(f"The gender: '{gender}' not exists to found id.")
        return gender_description_id
