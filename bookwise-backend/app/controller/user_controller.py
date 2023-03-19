from flask import jsonify
from werkzeug.security import generate_password_hash
from model.address_model import Address
from model.user_model import User
from model.usertype_model import UserType
from sqlalchemy.exc import IntegrityError

from service.database import db


class UserController:
    def create_user(data):
        try:
            required_fields = ['first_name', 'last_name', 'phone', 'cpf', 'email', 'password', 'user_type_id', 'gender',
                               'birthday', 'address']
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required field(s).'}, 400

            email = data.get('email')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {'error': 'Email already in use.'}, 400

            user_type = UserType.query.get(data['user_type_id'])

            if user_type is None:
                return {'error': 'User type not found.'}, 404

            new_address = Address(
                street=data['address']['street'],
                number=data['address']['number'],
                complement=data['address'].get('complement', None),
                city=data['address']['city'],
                state=data['address']['state'],
                zipcode=data['address']['zipcode'],
                country=data['address']['country']
            )

            db.session.add(new_address)
            db.session.flush()

            hashed_password = generate_password_hash(data['password'])

            new_user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                birthday=data['birthday'],
                address=new_address,
                user_type=user_type,
                cpf=data['cpf'],
                email=data['email'],
                password=data['password'],
                gender=data['gender'],
            )

            db.session.add(new_user)
            db.session.commit()

            return new_user.to_dict(), 201

        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Database error. Please try again later.'}, 500

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

