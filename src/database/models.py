from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from .db import db


Base = declarative_base()


class User(Base):
    __tablename__ = 'user_stay_safe'

    cpf = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)


Base.metadata.create_all(db)  # create tables
