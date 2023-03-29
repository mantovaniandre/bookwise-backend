from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/bookwise'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()