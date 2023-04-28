import bcrypt
from flask import current_app
import jwt

from model.credit_card import CreditCard
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
    def validate_user_data(user_data):
        required_fields = ['first_name', 'last_name', 'email', 'password', 'cpf', 'phone', 'birthday',
                           'user_type', 'gender', 'zip_code', 'street', 'number', 'complement',
                           'neighborhood', 'city', 'state','country', 'card_number', 'type_card',
                           'flag', 'bank', 'country_bank', 'card_name', 'expiration', 'cvv']

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
        if len(cpf) == 11:
            cpf_exists = user_repository.get_user_by_cpf(cpf)
        elif len(cpf) > 11:
            raise ValueError(f"The cpf {cpf} is greater than 14 digits")
        elif len(cpf) < 11:
            raise ValueError(f"The cpf {cpf} is less than 14 digits")
        if cpf_exists is False:
            raise ValueError(f"CPF {cpf} already exists.")

    @staticmethod
    def verify_password_for_update(password_front, password_back):
        password_login_encoded = password_front.encode('utf-8')
        user_password_encoded = password_back.encode('utf-8')
        return bcrypt.checkpw(password_login_encoded, user_password_encoded)

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
            raise ValueError(f"error creating new user.")

    @staticmethod
    def validate_user_created_successfully(address_id):
        address_service.delete_address_by_id(address_id)

    @staticmethod
    def encrypt_password(password):
        salt = bcrypt.gensalt(rounds=12)
        encrypt_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        encrypted_password = encrypt_password.decode('utf-8')
        return encrypted_password

    @staticmethod
    def create_user(user_data):
        address_id = 0
        try:
            UserService.validate_user_data(user_data)

            UserService.validate_email(user_data['email'])

            UserService.validate_cpf(user_data['cpf'])

            encrypted_password = UserService.encrypt_password(user_data['password'])

            new_address = address_service.create_new_address(user_data['zip_code'],
                                                             user_data['street'],
                                                             user_data['number'],
                                                             user_data['complement'],
                                                             user_data['neighborhood'],
                                                             user_data['city'],
                                                             user_data['state'],
                                                             user_data['country'])

            address_id = address_repository.save_address(new_address)

            user_type_service.validate_user_type(user_data['user_type'])

            usertype_id = user_type_service.find_id(user_data['user_type'])

            gender_service.validate_gender(user_data['gender'])

            gender_id = gender_service.find_id(user_data['gender'])

            new_credit_card = credit_card_service.create_new_credit_card(user_data['card_number'],
                                                                         user_data['type_card'],
                                                                         user_data['flag'],
                                                                         user_data['bank'],
                                                                         user_data['country_bank'],
                                                                         user_data['card_name'],
                                                                         user_data['expiration'],
                                                                         user_data['cvv'])

            credit_card_id = credit_card_repository.save_credit_card(new_credit_card)

            new_user = UserService.create_new_user(user_data, encrypted_password, address_id, usertype_id, gender_id,
                                                   credit_card_id)

            user_repository.save_user_to_database(new_user)
        except Exception as e:
            if address_id:
                UserService.validate_user_created_successfully(address_id)
                raise ValueError(f"{e}")
            else:
                raise ValueError(f"{e}")

    @staticmethod
    def update_user(front_data, id_token):
        different_values = {}
        same_values = {}

        try:
            user = UserRepository.get_user_by_id(id_token)

            UserService.validate_user_data(front_data)

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
                "first_name": front_data['first_name'],
                "last_name": front_data['last_name'],
                "email": front_data['email'],
                "password": front_data['password'],
                "cpf": front_data['cpf'],
                "phone": front_data['phone'],
                "birthday": front_data['birthday'],
                "user_type": front_data['user_type'],
                "gender": front_data['gender'],
                "zip_code": front_data['zip_code'],
                "street": front_data['street'],
                "number": front_data['number'],
                "complement": front_data['complement'],
                "neighborhood": front_data['neighborhood'],
                "city": front_data['city'],
                "state": front_data['state'],
                "country": front_data['country'],
                "card_number": front_data['card_number'],
                "type_card": front_data['type_card'],
                "flag": front_data['flag'],
                "bank": front_data['bank'],
                "country_bank": front_data['country_bank'],
                "card_name": front_data['card_name'],
                "expiration": front_data['expiration'],
                "cvv": front_data['cvv']
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
                        different_values[key] =  UserService.encrypt_password(supposed_new_user['password'])
                elif value != supposed_new_user[key]:
                    different_values[key] = supposed_new_user[key]
                else:
                    same_values[key] = supposed_new_user[key]

            if not different_values:
                raise ValueError(f"The data is the same as in the database..")
            else:
                for key, value in different_values.items():
                    table = table_map[key]
                    if table == 'users':
                        user_repository.update_user(table, user.id, **{key: value})
                    elif table == 'addresses':
                        address_repository.update_address(table, user.address_id, **{key: value})
                    elif table == 'credit_cards':
                        credit_card_repository.update_credit_card(table, user.credit_card_id, **{key: value})
                    elif table == 'user_types':
                        user_type_id = user_type_repository.get_id_usertype_by_description(
                            different_values['user_type'])
                        user_repository.update_user_usertype(table, user.id, user_type_id)
                    elif table == 'genders':
                        gender_id = gender_repository.get_id_gender_by_description(
                            different_values['gender'])
                        user_repository.update_user_gender(table, user.id, gender_id)
        except Exception as e:
            raise ValueError(f"{e}")

