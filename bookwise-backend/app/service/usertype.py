from repository.usertype import UsertypeRepository
from util.exception.custom_exception import ValidateUsertypeError, DescriptionUsertypeError

usertype_repository = UsertypeRepository()


class UsertypeService:
    @staticmethod
    def validate_usertype(description):
        if description == 'Employee':
            return True
        if description == 'Admin':
            return True
        else:
            raise ValidateUsertypeError(description)

    @staticmethod
    def find_id(description):
        usertype_description_id = usertype_repository.get_id_usertype_by_description(description)
        if usertype_description_id is False:
            raise DescriptionUsertypeError(description)
        return usertype_description_id
