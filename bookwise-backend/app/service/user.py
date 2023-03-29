from model.user import User
import bcrypt
from repository.address import AddressRepository
from repository.user import UserRepository
from service.address import AddressService
from service.gender import GenderService
from service.usertype import UsertypeService
from util.exception.custom_exception import CPFAlreadyExists, EmailAlreadyExists, ValidateUserDataError, NewUserError, \
    RegisterUserError

# created instances
user_repository = UserRepository()
address_repository = AddressRepository()
address_service = AddressService()
usertype_service = UsertypeService()
gender_service = GenderService()


class UserService:
    @staticmethod
    def validate_user_data(user_data):
        required_fields = ['first_name', 'last_name', 'email', 'password', 'cpf', 'phone', 'birthday',
                           'address', 'usertype', 'gender']

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
    def create_new_user(user_data: User, encrypted_password, address_id, usertype_id, gender_id):
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=encrypted_password,
            cpf=user_data['cpf'],
            phone=user_data['phone'],
            birthday=user_data['birthday'],
            address_id=address_id,
            usertype_id=usertype_id,
            gender_id=gender_id
        )
        if new_user:
            return new_user
        else:
            raise NewUserError()

    @staticmethod
    def validate_user_created_successfully(address_id):
        address_service.delete_address_by_id(address_id)

    @staticmethod
    def register_user(user_data):
        try:
            UserService.validate_user_data(user_data)

            UserService.email_exists(user_data['email'])

            UserService.cpf_exists(user_data['cpf'])

            encrypted_password = UserService.encrypt_password(user_data['password'])

            new_address = address_service.create_address(**user_data['address'])

            address_id = address_repository.save_address(new_address)

            usertype_service.validate_usertype(user_data['usertype']['description'])

            usertype_id = usertype_service.find_id(user_data['usertype']['description'])

            gender_service.validate_gender(user_data['gender']['description'])

            gender_id = gender_service.find_id(user_data['gender']['description'])

            new_user = UserService.create_new_user(user_data, encrypted_password, address_id, usertype_id, gender_id)

            user_repository.save_user_to_database(new_user)
        except Exception as e:
            UserService.validate_user_created_successfully(address_id)
            raise RegisterUserError(e)


