import datetime
from sqlalchemy import (
    Column, String, Integer, Float,
    ForeignKey, DateTime, Boolean, ARRAY, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import CompositeType

from settings import BCRYPT
from database.db import db
from utils.formatters import get_row_dict

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_stay_safe'

    username = Column(String(20), primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    full_name = Column(String(200), nullable=False)
    device_token = Column(String(50), nullable=True)
    show_notifications = Column(Boolean, nullable=False)
    occurrence = relationship("Occurrence")
    rating = relationship("Rating")
    favorite_places = relationship("FavoritePlace")

    def __init__(self, username, email, password, full_name, device_token=None, show_notifications=False):
        self.username = username
        self.email = email
        self.password = BCRYPT.generate_password_hash(
            password).decode('utf-8')
        self.full_name = full_name
        self.device_token = device_token
        self.show_notifications = show_notifications

    def to_dict(self):
        user = {
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'device_token': self.device_token,
            'show_notifications': self.show_notifications
        }

        return user


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
        Enum('Latrocínio', 'Roubo a Transeunte', 'Roubo de Veículo',
             'Roubo de Residência', 'Estupro', 'Furto a Transeunte',
             'Furto de Veículo', name='occurrence_type'),
        nullable=False)

    def to_dict(self):
        occurrence = {
            'id_occurrence': self.id_occurrence,
            'occurrence_type': self.occurrence_type,
            'occurrence_date_time': str(self.occurrence_date_time),
            'physical_aggression': self.physical_aggression,
            'victim': self.victim,
            'police_report': self.police_report,
            'gun': self.gun,
            'location': self.location,
            'register_date_time': str(self.register_date_time)
        }

        return occurrence


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
    neighborhood = relationship("Neighborhood", back_populates="rating")
    rating_neighborhood = Column(Integer, nullable=False)
    details = Column(
        CompositeType(
            'details',
            [
                Column('lighting', Boolean),
                Column('movement_of_people', Boolean),
                Column('police_rounds', Boolean)
            ]
        )
    )

    def to_dict(self, del_null_attr=True):
        # getting the details
        details = {}
        for field in self.details._fields:
            value = self.details.__getattribute__(field)
            if del_null_attr:
                if value is not None:
                    details.update({field: value})
            else:
                details.update({field: value})

        rating = {
            'details': details,
            'id_rating': self.id_rating,
            'user': self.user,
            'rating_neighborhood': self.rating_neighborhood,
            'neighborhood': get_row_dict(self.neighborhood)
        }

        return rating


class FavoritePlace(Base):
    __tablename__ = 'favorite_places_stay_safe'

    id_place = Column(Integer, primary_key=True)
    user = Column(String, ForeignKey(User.username))
    name = Column(String(30), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


Base.metadata.create_all(db)
