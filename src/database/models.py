from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from .db import db

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_stay_safe'

    username = Column(String(20), primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    full_name = Column(String(200), nullable=False)


Base.metadata.create_all(db)
