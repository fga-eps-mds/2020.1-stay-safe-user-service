import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean, ARRAY, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .db import db

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_stay_safe'

    username = Column(String(20), primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    full_name = Column(String(200), nullable=False)
    occurrence = relationship("Occurrence")

class Occurrence(Base):
    __tablename__ = 'occurrence_stay_safe'

    id_occurrence = Column(Integer, primary_key=True)
    user = Column(String, ForeignKey(User.username))
    register_date_time = Column(DateTime, server_default=func.now(), nullable=False)
    occurrence_date_time = Column(DateTime, nullable=False)
    physical_aggression = Column(Boolean, nullable=False)
    victim = Column(Boolean, nullable=False)
    police_report = Column(Boolean, nullable=False)
    gun = Column(Enum('None', 'Fire', 'White', name='gun'), nullable=False)
    location = Column(ARRAY(Float), nullable=False)
    occurrence_type = Column(Enum('Latrocínio', 'Roubo a transeunte', 'Roubo de Veículo', 'Roubo de Residência', 'Estupro', name='occurrence_type'), nullable=False)

Base.metadata.create_all(db)
