import bcrypt
from flask import current_app
import jwt
from model.user import User
import re
from repository.address import AddressRepository
from repository.creditCard import CreditCardRepository
from repository.user import UserRepository
from repository.userversion import UserVersionRepository
from service.address import AddressService
from service.creditCard import CreditCardService
from service.gender import GenderService
from service.usertype import UsertypeService
from service.userversion import UserVersionService

# created instances
user_repository = UserRepository()
address_repository = AddressRepository()
address_service = AddressService()
usertype_service = UsertypeService()
gender_service = GenderService()
credit_card_service = CreditCardService()
credit_card_repository = CreditCardRepository()
user_version_service = UserVersionService()
user_version_repository = UserVersionRepository()


class UserService:
    @staticmethod
    def validate_user_data(user_data):
        required_fields = ['firstName', 'lastName', 'email', 'password', 'cpf', 'phone', 'birthday',
                           'usertype', 'gender', 'zipCode', 'street', 'number', 'complement', 'city', 'state',
                           'country', 'cardNumber', 'typeCard', 'flag', 'bank', 'countryBank',
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
    def validate_token(token):
        user_token = user_repository.get_user_by_token(token)
        if user_token:
            return user_token.id
        else:
            raise ValueError(f"Token {user_token.token} is incorrect.")

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
    def encrypt_password(password):
        salt = bcrypt.gensalt(rounds=12)
        encrypt_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        encrypted_password = encrypt_password.decode('utf-8')
        return encrypted_password

    @staticmethod
    def create_new_user(user_data, encrypted_password, address_id, usertype_id, gender_id, credit_card_id):
        new_user = User(
            first_name=user_data['firstName'],
            last_name=user_data['lastName'],
            email=user_data['email'],
            password=encrypted_password,
            cpf=user_data['cpf'],
            phone=user_data['phone'],
            birthday=user_data['birthday'],
            address_id=address_id,
            usertype_id=usertype_id,
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
    def create_user(user_data):
        address_id = 0
        try:
            UserService.validate_user_data(user_data)

            UserService.validate_email(user_data['email'])

            UserService.validate_cpf(user_data['cpf'])

            encrypted_password = UserService.encrypt_password(user_data['password'])

            new_address = address_service.create_new_address(user_data['zipCode'], user_data['street'],
                                                             user_data['number'],
                                                             user_data['complement'], user_data['neighborhood'],
                                                             user_data['city'],
                                                             user_data['state'], user_data['country'])

            address_id = address_repository.save_address(new_address)

            usertype_service.validate_usertype(user_data['usertype'])

            usertype_id = usertype_service.find_id(user_data['usertype'])

            gender_service.validate_gender(user_data['gender'])

            gender_id = gender_service.find_id(user_data['gender'])

            new_credit_card = credit_card_service.create_new_credit_card(user_data['cardNumber'], user_data['typeCard'],
                                                                         user_data['flag'],
                                                                         user_data['bank'],
                                                                         user_data['countryBank'],
                                                                         user_data['cardName'],
                                                                         user_data['expiration'], user_data['cvv'])

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
    def update_user(front_data, get_id_token):
        address_id = 0
        try:
            user = UserRepository.get_user_by_id(get_id_token)

            UserService.validate_user_data(front_data)

            user_data_base = {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "password": user.password,
                "cpf": user.cpf,
                "phone": user.phone,
                "birthday": user.birthday,
                "usertype": user.usertype.description,
                "gender": user.gender.description,
                "zipCode": user.address.zipcode,
                "street": user.address.street,
                "number": user.address.number,
                "complement": user.address.complement,
                "neighborhood": user.address.neighborhood,
                "city": user.address.city,
                "state": user.address.state,
                "country": user.address.country,
                "cardNumber": user.credit_card.cardNumber,
                "typeCard": user.credit_card.typeCard,
                "flag": user.credit_card.flag,
                "bank": user.credit_card.bank,
                "countryBank": user.credit_card.countryBank,
                "cardName": user.credit_card.cardName,
                "expiration": user.credit_card.expiration,
                "cvv": user.credit_card.cvv
            }

            new_front_data = {
                "firstName": front_data['firstName'],
                "lastName": front_data['lastName'],
                "email": front_data['email'],
                "password": front_data['password'],
                "cpf": front_data['cpf'],
                "phone": front_data['phone'],
                "birthday": front_data['birthday'],
                "usertype": front_data['usertype'],
                "gender": front_data['gender'],
                "zipCode": front_data['zipCode'],
                "street": front_data['street'],
                "number": front_data['number'],
                "complement": front_data['complement'],
                "neighborhood": front_data['neighborhood'],
                "city": front_data['city'],
                "state": front_data['state'],
                "country": front_data['country'],
                "cardNumber": front_data['cardNumber'],
                "typeCard": front_data['typeCard'],
                "flag": front_data['flag'],
                "bank": front_data['bank'],
                "countryBank": front_data['countryBank'],
                "cardName": front_data['cardName'],
                "expiration": front_data['expiration'],
                "cvv": front_data['cvv']
            }

            if user_data_base == new_front_data:

            else:
                user_version = user_version_service.create_new_user_version(user.id, user.address_id,
                                                                            user.credit_card_id, user_data_base)

                user_version_repository.save_user_version_to_database(user_version)

                new_address = address_service.create_new_address(front_data['zipCode'], front_data['street'],
                                                                 front_data['number'],
                                                                 front_data['complement'],
                                                                 front_data['neighborhood'],
                                                                 front_data['city'],
                                                                 front_data['state'], front_data['country'])

                address_id = address_repository.save_address(new_address)

                usertype_service.validate_usertype(front_data['usertype'])

                usertype_id = usertype_service.find_id(front_data['usertype'])

                gender_service.validate_gender(front_data['gender'])

                gender_id = gender_service.find_id(front_data['gender'])

                new_credit_card = credit_card_service.create_new_credit_card(front_data['cardNumber'],
                                                                             front_data['typeCard'],
                                                                             front_data['flag'],
                                                                             front_data['bank'],
                                                                             front_data['countryBank'],
                                                                             front_data['cardName'],
                                                                             front_data['expiration'],
                                                                             front_data['cvv'])

                credit_card_id = credit_card_repository.save_credit_card(new_credit_card)

                encrypted_password = UserService.encrypt_password(front_data['password'])

                create_new_user = UserService.create_new_user

                new_user = UserService.create_new_user(front_data, encrypted_password, address_id, usertype_id,
                                                       gender_id,
                                                       credit_card_id)

                user_repository.save_user_to_database(new_user)
        except Exception as e:
            if address_id:
                UserService.validate_user_created_successfully(address_id)
                raise ValueError(f"{e}")
            else:
                raise ValueError(f"{e}")