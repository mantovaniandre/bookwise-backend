from configuration.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    cpf = Column(String(20), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    usertype_id = Column(Integer, ForeignKey('usertypes.id'))
    gender_id = Column(Integer, ForeignKey('genders.id'))
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    address = relationship('Address', back_populates='user')
    usertype = relationship('UserType', back_populates='user')
    gender = relationship('Gender', back_populates='user')

    def __init__(self, first_name, last_name, email, password, cpf, phone, birthday, address_id, usertype_id, gender_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.cpf = cpf
        self.phone = phone
        self.birthday = birthday
        self.address_id = address_id
        self.usertype_id = usertype_id
        self.gender_id = gender_id
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}'," \
               f"email='{self.email}', password='{self.password}', cpf='{self.cpf}', phone='{self.phone}'," \
               f"birthday='{self.birthday}', address_id='{self.address_id}', usertype_id='{self.usertype_id}'," \
               f"last_update='{self.last_update}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "cpf": self.cpf,
            "phone": self.phone,
            "birthday": self.birthday.isoformat(),
            "address_id": self.address_id,
            "usertype_id": self.usertype_id,
            "gender_id": self.gender_id,
            "last_update": data_time_conversion.dataTimeConversionToSaoPaulo(),
        }

