from repository.user_type import UsertypeRepository
from util.exception.custom_exception import InvalidUserTypeError, UserTypeNotFoundError

usertype_repository = UsertypeRepository()


class UsertypeService:
    @staticmethod
    def validate_user_type(description):
        if description == 'CLIENT':
            return True
        if description == 'ADMIN':
            return True
        else:
            raise InvalidUserTypeError(description)

    @staticmethod
    def find_id(description):
        usertype_description_id = usertype_repository.get_id_user_type_by_description(description)
        if usertype_description_id is False:
            raise UserTypeNotFoundError(description)
        return usertype_description_id
