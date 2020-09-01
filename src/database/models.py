from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from .db import db


Base = declarative_base()


class User(Base):
    __tablename__ = 'user_stay_safe'

    username = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)
    full_name = Column(String)


Base.metadata.create_all(db)
