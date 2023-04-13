from model.address import Address
from model.user import User
import bcrypt
import re
from repository.address import AddressRepository
from repository.user import UserRepository
from service.address import AddressService
from service.gender import GenderService
from service.usertype import UsertypeService

# created instances
user_repository = UserRepository()
address_repository = AddressRepository()
address_service = AddressService()
usertype_service = UsertypeService()
gender_service = GenderService()


class UserService:
    @staticmethod
    def validate_user_data(user_data):
        required_fields = ['firstName', 'lastName', 'email', 'password', 'cpf', 'phone', 'birthday',
                           'usertype', 'gender', 'zipCode', 'street', 'number', 'complement', 'complement',
                           'city', 'state', 'country', 'cardNumber', 'typeCard', 'flag', 'bank', 'countryBank',
                           'cardName', 'expiration', 'cvv']

        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Required field '{field}' not provided.")
            elif not user_data[field]:
                raise ValueError(f"Field '{field}' cannot be empty.")

    @staticmethod
    def validate_email(email):
        standard = r"[^@]+@[^@]+\.[^@]+"
        if re.match(standard, email):
            email_exists = user_repository.get_user_by_email(email)
        else:
            raise ValueError(f"email: {email} with undefined pattern")
        if email_exists is False:
            raise ValueError(f"Email {email} already exists.")

    @staticmethod
    def validate_cpf(cpf):
        cpf_exists = True
        if len(cpf) == 14:
            cpf_exists = user_repository.get_user_by_cpf(cpf)
        elif len(cpf) > 14:
            raise ValueError(f"The cpf {cpf} is greater than 14 digits")
        elif len(cpf) < 14:
            raise ValueError(f"The cpf {cpf} is less than 14 digits")
        if cpf_exists is False:
            raise ValueError(f"CPF {cpf} already exists.")

    @staticmethod
    def encrypt_password(password):
        salt = bcrypt.gensalt()
        encrypt_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        encrypted_password = encrypt_password.decode('utf-8')
        return encrypted_password

    @staticmethod
    def create_new_address(zipCode, street, number, complement, neighborhood, city, state, country):
        new_address = Address(
            street=street,
            number=number,
            complement=complement,
            neighborhood=neighborhood,
            city=city,
            state=state,
            zipcode=zipCode,
            country=country
        )
        if new_address:
            return new_address
        else:
            raise ValueError(f"error creating new user.")

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
            raise ValueError(f"error creating new user.")

    @staticmethod
    def validate_user_created_successfully(address_id):
        address_service.delete_address_by_id(address_id)

    @staticmethod
    def register_user(user_data):
        address_id = 0
        try:
            UserService.validate_user_data(user_data)

            UserService.validate_email(user_data['email'])

            UserService.validate_cpf(user_data['cpf'])

            encrypted_password = UserService.encrypt_password(user_data['password'])

            new_address = UserService.create_new_address(user_data['zipCode'], user_data['street'], user_data['number'],
                                                     user_data['complement'], user_data['neighborhood'],
                                                     user_data['city'],
                                                     user_data['state'], user_data['country'])

            address_id = address_repository.save_address(new_address)

            usertype_service.validate_usertype(user_data['usertype']['description'])

            usertype_id = usertype_service.find_id(user_data['usertype']['description'])

            gender_service.validate_gender(user_data['gender']['description'])

            gender_id = gender_service.find_id(user_data['gender']['description'])

            new_user = UserService.create_new_user(user_data, encrypted_password, address_id, usertype_id, gender_id)

            user_repository.save_user_to_database(new_user)
        except Exception as e:
            if address_id:
                UserService.validate_user_created_successfully(address_id)
                raise ValueError(f"{e}")
            else:
                raise ValueError(f"{e}")
