from model.address import Address
from model.user import User
import bcrypt
from model.usertype import UserType
from repository.user import UserRepository
from service.address import AddressService
from service.usertype import UsertypeService
from util.exception.custom_exception import CPFAlreadyExists, EmailAlreadyExists, ValidateUserDataError

# created instances
user_repository = UserRepository()
address_service = AddressService()
usertype_service = UsertypeService()


class UserService:
    @staticmethod
    def validate_user_data(user_data):
        required_fields = ['first_name', 'last_name', 'email', 'password', 'cpf', 'gender', 'phone', 'birthday',
                           'address', 'usertype']

        for field in required_fields:
            if field not in user_data:
                raise ValidateUserDataError(field)

    @staticmethod
    def email_exists(email):
        email_exists = user_repository.get_user_by_email(email)
        if email_exists is False:
            raise EmailAlreadyExists(email)

    @staticmethod
    def cpf_exists(cpf):
        cpf_exists = user_repository.get_user_by_cpf(cpf)
        if cpf_exists is False:
            raise CPFAlreadyExists(cpf)

    @staticmethod
    def encrypt_password(password):
        salt = bcrypt.gensalt()
        encrypt_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return encrypt_password.decode('utf-8')

    @staticmethod
    def create_user(user_data: User, address_id, usertype_id):
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],
            cpf=user_data['cpf'],
            gender=user_data['gender'],
            phone=user_data['phone'],
            birthday=user_data['birthday'],
            address_id=address_id,
            usertype_id=usertype_id
        )
        return new_user

    @staticmethod
    def save_user(user_data):
        UserService.validate_user_data(user_data)

        UserService.email_exists(user_data['email'])

        UserService.cpf_exists(user_data['cpf'])

        UserService.encrypt_password(user_data['password'])

        new_address = address_service.create_address(**user_data['address'])

        address_id = user_repository.save_address(new_address)

        new_usertype = usertype_service.create_usertype(**user_data['usertype'])

        usertype_id = user_repository.save_usertype(new_usertype)

        new_user = UserService.create_user(user_data, address_id, usertype_id)

        user_repository.save_user(new_user)




