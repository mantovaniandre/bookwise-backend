from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/bookwise'

engine = create_engine(DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
