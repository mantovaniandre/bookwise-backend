from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

DATABASE_URI = config('DATABASE_URL')

# Enhanced engine configuration for production
engine = create_engine(
    DATABASE_URI, 
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections every hour
    pool_size=10,       # Connection pool size
    max_overflow=20,    # Maximum overflow connections
    echo=config('DEBUG', default=False, cast=bool)  # SQL logging in debug mode
)

Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
