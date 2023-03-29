from configuration.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    cpf = Column(String(20), nullable=False, unique=True)
    gender = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    usertype_id = Column(Integer, ForeignKey('usertypes.id'))
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    address = relationship('Address')
    usertype = relationship('UserType')

    def __init__(self, first_name, last_name, email, password, cpf, gender, phone, birthday, address_id, usertype_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.cpf = cpf
        self.gender = gender
        self.phone = phone
        self.birthday = birthday
        self.address_id = address_id
        self.usertype_id = usertype_id
        self.last_update = datetime.utcnow()

    def __repr__(self):
        return f"<User(id={self.id}, nome='{self.nome}', email='{self.email}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "cpf": self.cpf,
            "gender": self.gender,
            "phone": self.phone,
            "birthday": self.birthday.isoformat(),
            "address_id": self.address_id,
            "usertype_id": self.usertype_id,
            "last_update": self.last_update.isoformat(),
        }

