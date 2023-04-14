from repository.usertype import UsertypeRepository

usertype_repository = UsertypeRepository()


class UsertypeService:
    @staticmethod
    def validate_usertype(description):
        if description == 'CLIENT':
            return True
        if description == 'ADMIN':
            return True
        else:
            raise ValueError(f"The usertype: '{description}' not exists.")

    @staticmethod
    def find_id(description):
        usertype_description_id = usertype_repository.get_id_usertype_by_description(description)
        if usertype_description_id is False:
            raise ValueError(f"The usertype: '{description}' not exists to found id.")
        return usertype_description_id
