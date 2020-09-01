from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from .db import db

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_stay_safe'

    username = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

Base.metadata.create_all(db)
