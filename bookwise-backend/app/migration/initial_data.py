from model.gender import Gender
from model.user_type import UserType
from configuration.database import Base, engine, Session


def create_user_type():
    session = Session()
    employee = session.query(UserType).filter_by(description='ADMIN').first()
    admin = session.query(UserType).filter_by(description='CLIENT').first()
    if not employee:
        session.add(UserType(description='ADMIN'))
    if not admin:
        session.add(UserType(description='CLIENT'))
    session.commit()


def create_gender():
    session = Session()
    masculine = session.query(Gender).filter_by(description='MASCULINE').first()
    feminine = session.query(Gender).filter_by(description='FEMININE').first()
    if not masculine:
        session.add(Gender(description='MASCULINE'))
    if not feminine:
        session.add(Gender(description='FEMININE'))
    session.commit()


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)