import datetime
from sqlalchemy import (
    Column, String, Integer, Float,
    ForeignKey, DateTime, Boolean, ARRAY, Enum, Sequence
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .db import db
from settings import BCRYPT

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_stay_safe'

    username = Column(String(20), primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    full_name = Column(String(200), nullable=False)
    occurrence = relationship("Occurrence")
    rating = relationship("Rating")

    def __init__(self, username, email, password, full_name):
        self.username = username,
        self.email = email,
        self.password = BCRYPT.generate_password_hash(
            password).decode('utf-8'),
        self.full_name = full_name


class Occurrence(Base):
    __tablename__ = 'occurrence_stay_safe'

    id_occurrence = Column(Integer, primary_key=True)
    user = Column(String, ForeignKey(User.username))
    register_date_time = Column(DateTime,
                                default=datetime.datetime.now,
                                nullable=False)
    occurrence_date_time = Column(DateTime, nullable=False)
    physical_aggression = Column(Boolean, nullable=False)
    victim = Column(Boolean, nullable=False)
    police_report = Column(Boolean, nullable=False)
    gun = Column(Enum('None', 'Fire', 'White', name='gun'), nullable=False)
    location = Column(ARRAY(Float), nullable=False)
    occurrence_type = Column(
        Enum('Latrocínio', 'Roubo a transeunte', 'Roubo de Veículo',
             'Roubo de Residência', 'Estupro', name='occurrence_type'),
        nullable=False)


class Neighborhood(Base):
    __tablename__ = 'neighborhood_stay_safe'

    id_neighborhood = Column(Integer, primary_key=True)
    neighborhood = Column(String(80), nullable=False)
    city = Column(String(80), nullable=False)
    state = Column(String(2), nullable=False)
    rating = relationship("Rating")


class Rating(Base):
    __tablename__ = 'rating_stay_safe'

    id_rating = Column(Integer, primary_key=True)
    user = Column(String, ForeignKey(User.username))
    id_neighborhood = Column(Integer, ForeignKey(Neighborhood.id_neighborhood))
    rating_neighborhood = Column(Integer, nullable=False)
    details = Column(
        Enum("bad lighting", "low movement of people", "few police rounds",
             "good lighting", "good movement of people",
             "frequent police rounds", name='details'),
        nullable=False)


Base.metadata.create_all(db)
