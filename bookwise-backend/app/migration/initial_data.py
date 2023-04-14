from configuration.database import Session
from model.gender import Gender
from model.usertype import UserType
from configuration.database import Base, engine, Session


def create_userType():
    session = Session()
    employee = session.query(UserType).filter_by(description='Admin').first()
    admin = session.query(UserType).filter_by(description='Client').first()
    if not employee:
        session.add(UserType(description='Admin'))
    if not admin:
        session.add(UserType(description='Client'))
    session.commit()


def create_gender():
    session = Session()
    masculine = session.query(Gender).filter_by(description='Masculine').first()
    feminine = session.query(Gender).filter_by(description='Feminine').first()
    if not masculine:
        session.add(Gender(description='Masculine'))
    if not feminine:
        session.add(Gender(description='Feminine'))
    session.commit()

def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)