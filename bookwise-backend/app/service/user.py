import bcrypt
from model.user import User
import re
from repository.address import AddressRepository
from repository.credit_card import CreditCardRepository
from repository.gender import GenderRepository
from repository.user import UserRepository
from repository.user_type import UsertypeRepository
from service.address import AddressService
from service.credit_card import CreditCardService
from service.gender import GenderService
from service.user_type import UsertypeService
from util.exception.custom_exception import MissingRequiredFieldError, InvalidEmailFormatError, DuplicateEmailError, \
    InvalidPasswordError, NewUserCreationError, \
    AddressDeletionError, PasswordEncryptionError, AddressValidationError, UserCreationError, UserUpdateError, \
    CPFHasToHaveOnlyNumbers, InvalidFieldLengthError, DuplicateCPFError, SameDataInDatabaseException, \
    UserNotFoundIdError

# created instances
user_repository = UserRepository()
address_repository = AddressRepository()
address_service = AddressService()
user_type_service = UsertypeService()
user_type_repository = UsertypeRepository()
gender_service = GenderService()
gender_repository = GenderRepository()
credit_card_service = CreditCardService()
credit_card_repository = CreditCardRepository()


class UserService:
    @staticmethod
    def validate_user_data_and_field_sizes(request_data):
        required_fields = ['first_name', 'last_name', 'email', 'password', 'cpf', 'phone', 'birthday',
                           'user_type', 'gender', 'zip_code', 'street', 'number', 'complement',
                           'neighborhood', 'city', 'state', 'country', 'card_number', 'type_card',
                           'flag', 'bank', 'country_bank', 'card_name', 'expiration', 'cvv']

        max_lengths = {'first_name': 20, 'last_name': 20, 'email': 50, 'password': 255, 'cpf': 11,
                       'phone': 11, 'birthday': 10, 'user_type': 10, 'gender': 10, 'zip_code': 8,
                       'street': 100, 'number': 6, 'complement': 50, 'neighborhood': 50, 'city': 50,
                       'state': 2, 'country': 6, 'card_number': 16, 'type_card': 10, 'flag': 20,
                       'bank': 50, 'country_bank': 30, 'card_name': 30, 'expiration': 7, 'cvv': 3}

        for field in required_fields:
            if field not in request_data:
                raise MissingRequiredFieldError(field)
            elif not request_data[field]:
                raise MissingRequiredFieldError(field)
            elif field == "cpf":
                if len(request_data[field]) != 11:
                    raise InvalidFieldLengthError(field, 11)
            elif field == "phone":
                if len(request_data[field]) != 11:
                    raise InvalidFieldLengthError(field, 11)
            elif field == "birthday":
                if len(request_data[field]) != 10:
                    raise InvalidFieldLengthError(field, 10)
            elif field == "zip_code":
                if len(request_data[field]) != 8:
                    raise InvalidFieldLengthError(field, 8)
            elif field == "card_number":
                if len(request_data[field]) != 16:
                    raise InvalidFieldLengthError(field, 16)
            elif field == "expiration":
                if len(request_data[field]) != 7:
                    raise InvalidFieldLengthError(field, 7)
            elif field == "cvv":
                if len(request_data[field]) != 3:
                    raise InvalidFieldLengthError(field, 3)
            if field in max_lengths and len(request_data[field]) > max_lengths[field]:
                raise InvalidFieldLengthError(field, max_lengths[field])

    @staticmethod
    def validate_format_and_unique_email(email):
        standard = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(standard, email):
            raise InvalidEmailFormatError(email)
        if not user_repository.get_user_by_email_to_validate_email_exist(email):
            raise DuplicateEmailError(email)

    @staticmethod
    def validate_cpf_email_to_update_user(user_id, cpf, email):
        cpf_exists = user_repository.get_user_by_cpf_to_update(cpf)
        email_exists = user_repository.get_user_by_email_to_update(email)
        if cpf_exists and cpf_exists.id != user_id:
            raise DuplicateCPFError(cpf)
        if email_exists and email_exists.id != user_id:
            raise DuplicateEmailError(email)

    @staticmethod
    def validate_format_and_unique_cpf(cpf):
        if not cpf.isdigit():
            raise CPFHasToHaveOnlyNumbers()
        cpf_exists = user_repository.get_user_by_cpf_to_validate_cpf_exist(cpf)
        if not cpf_exists:
            raise DuplicateCPFError(cpf)
        else:
            return True

    @staticmethod
    def verify_password_for_update(password_front, password_back):
        password_login_encoded = password_front.encode('utf-8')
        user_password_encoded = password_back.encode('utf-8')
        if bcrypt.checkpw(password_login_encoded, user_password_encoded):
            return True
        return False

    @staticmethod
    def create_new_user(user_data, encrypted_password, address_id, user_type_id, gender_id, credit_card_id):
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=encrypted_password,
            cpf=user_data['cpf'],
            phone=user_data['phone'],
            birthday=user_data['birthday'],
            address_id=address_id,
            user_type_id=user_type_id,
            gender_id=gender_id,
            credit_card_id=credit_card_id
        )
        if new_user:
            return new_user
        else:
            raise NewUserCreationError()

    @staticmethod
    def delete_address_if_user_not_created(address_id):
        if not address_service.delete_address_by_id(address_id):
            raise AddressDeletionError(address_id)

    @staticmethod
    def encrypt_password(password):
        try:
            salt = bcrypt.gensalt(rounds=12)
            encrypt_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            encrypted_password = encrypt_password.decode('utf-8')
            return encrypted_password
        except Exception as e:
            raise PasswordEncryptionError(str(e))

    @staticmethod
    def create_user(request_data):
        address_id = 0
        try:
            UserService.validate_user_data_and_field_sizes(request_data)
            UserService.validate_format_and_unique_email(request_data['email'])
            UserService.validate_format_and_unique_cpf(request_data['cpf'])
            encrypted_password = UserService.encrypt_password(request_data['password'])
            new_address = address_service.create_new_address(request_data['zip_code'], request_data['street'],
                                                             request_data['number'], request_data['complement'],
                                                             request_data['neighborhood'], request_data['city'],
                                                             request_data['state'], request_data['country'])
            address_id = address_repository.save_address(new_address)
            user_type_service.validate_user_type(request_data['user_type'])
            usertype_id = user_type_service.find_id(request_data['user_type'])
            gender_service.validate_gender(request_data['gender'])
            gender_id = gender_service.find_id(request_data['gender'])
            credit_card = credit_card_service.create_new_credit_card(request_data['card_number'],
                                                                     request_data['type_card'],
                                                                     request_data['flag'],
                                                                     request_data['bank'],
                                                                     request_data['country_bank'],
                                                                     request_data['card_name'],
                                                                     request_data['expiration'],
                                                                     request_data['cvv'])
            credit_card_id = credit_card_repository.save_credit_card(credit_card)
            new_user = UserService.create_new_user(request_data, encrypted_password, address_id, usertype_id, gender_id,
                                                   credit_card_id)
            user_save = user_repository.create_user_to_database(new_user)
            if user_save:
                return True
            else:
                UserService.delete_address_if_user_not_created(address_id)
        except Exception as e:
            raise e

    @staticmethod
    def update_user(request_data, id_user_token):
        different_values = {}
        same_values = {}
        try:
            user = UserRepository.get_user_by_id(id_user_token)
            UserService.validate_user_data_and_field_sizes(request_data)
            UserService.validate_cpf_email_to_update_user(user.id, request_data['cpf'], request_data['email'])
            user_type_service.validate_user_type(request_data['user_type'])
            gender_service.validate_gender(request_data['gender'])

            supposed_old_user = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "password": user.password,
                "cpf": user.cpf,
                "phone": user.phone,
                "birthday": user.birthday,
                "user_type": user.user_type.description,
                "gender": user.gender.description,
                "zip_code": user.address.zip_code,
                "street": user.address.street,
                "number": user.address.number,
                "complement": user.address.complement,
                "neighborhood": user.address.neighborhood,
                "city": user.address.city,
                "state": user.address.state,
                "country": user.address.country,
                "card_number": user.credit_card.card_number,
                "type_card": user.credit_card.type_card,
                "flag": user.credit_card.flag,
                "bank": user.credit_card.bank,
                "country_bank": user.credit_card.country_bank,
                "card_name": user.credit_card.card_name,
                "expiration": user.credit_card.expiration,
                "cvv": user.credit_card.cvv
            }

            supposed_new_user = {
                "first_name": request_data['first_name'],
                "last_name": request_data['last_name'],
                "email": request_data['email'],
                "password": request_data['password'],
                "cpf": request_data['cpf'],
                "phone": request_data['phone'],
                "birthday": request_data['birthday'],
                "user_type": request_data['user_type'],
                "gender": request_data['gender'],
                "zip_code": request_data['zip_code'],
                "street": request_data['street'],
                "number": request_data['number'],
                "complement": request_data['complement'],
                "neighborhood": request_data['neighborhood'],
                "city": request_data['city'],
                "state": request_data['state'],
                "country": request_data['country'],
                "card_number": request_data['card_number'],
                "type_card": request_data['type_card'],
                "flag": request_data['flag'],
                "bank": request_data['bank'],
                "country_bank": request_data['country_bank'],
                "card_name": request_data['card_name'],
                "expiration": request_data['expiration'],
                "cvv": request_data['cvv']
            }

            table_map = {
                "first_name": 'users',
                "last_name": 'users',
                "email": 'users',
                "password": 'users',
                "cpf": 'users',
                "phone": 'users',
                "birthday": 'users',
                "user_type": 'user_types',
                "gender": 'genders',
                "zip_code": 'addresses',
                "street": 'addresses',
                "number": 'addresses',
                "complement": 'addresses',
                "neighborhood": 'addresses',
                "city": 'addresses',
                "state": 'addresses',
                "country": 'addresses',
                "card_number": 'credit_cards',
                "type_card": 'credit_cards',
                "flag": 'credit_cards',
                "bank": 'credit_cards',
                "country_bank": 'credit_cards',
                "card_name": 'credit_cards',
                "expiration": 'credit_cards',
                "cvv": 'credit_cards'
            }

            for key, value in supposed_old_user.items():
                if key == 'password':
                    if UserService.verify_password_for_update(supposed_new_user['password'], value):
                        same_values[key] = value
                    else:
                        different_values[key] = UserService.encrypt_password(supposed_new_user['password'])
                else:
                    new_value_upper = supposed_new_user[key].upper()
                    old_value_upper = value.upper() if value else None
                    if new_value_upper != old_value_upper:
                        different_values[key] = new_value_upper
                    else:
                        same_values[key] = new_value_upper
            if not different_values:
                raise SameDataInDatabaseException()
            else:
                table_users = 'users'
                for key, value in different_values.items():
                    table = table_map[key]
                    if table == 'users':
                        user_repository.update_user(table, user.id, **{key: value})
                    elif table == 'addresses':
                        address_repository.update_address(table, user.address_id, **{key: value})
                    elif table == 'credit_cards':
                        credit_card_repository.update_credit_card(table, user.credit_card_id, **{key: value})
                    elif table == 'user_types':
                        user_type_id = user_type_repository.get_id_user_type_by_description(
                            different_values['user_type'])
                        user_repository.update_user_type_of_user(table_users, user.id, user_type_id)
                    elif table == 'genders':
                        gender_id = gender_repository.get_id_gender_by_description(
                            different_values['gender'])
                        user_repository.update_gender_of_user(table_users, user.id, gender_id)
            return True
        except Exception as e:
            raise e

    @staticmethod
    def get_profile_user(id_token):
        try:
            user = UserRepository.get_user_by_id(id_token)
            address = AddressRepository.get_address_by_id_of_user(user.id)
            credit_card = CreditCardRepository.get_credit_card_by_id_of_user(user.id)
            user_dict = user.to_dict()
            user_dict['address'] = address.to_dict()
            user_dict['credit_card'] = credit_card.to_dict()
            return user_dict
        except Exception as e:
            raise e

    @staticmethod
    def delete_user(id_token):
        try:
            user = UserRepository.get_user_by_id(id_token)
            if user:
                user_repository.delete_user_by_id(user.id)
                return True
            else:
                raise UserNotFoundIdError(user)
        except Exception as e:
            raise e
