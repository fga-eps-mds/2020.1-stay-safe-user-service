from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

from settings import logger


db_url = os.environ.get("SQLALCHEMY_DB_URL")
db = create_engine(db_url, echo=True)

Session = sessionmaker(db)
session = Session()


def insert_one(element):
    try:
        session.add(element)
        session.commit()
    except Exception as error:
        logger.error(error)
        session.rollback()


def get_all(model):
    try:
        data = session.query(model).all()
        session.commit()

        return data
    except Exception as error:
        logger.error(error)
        session.rollback()

        return None


def get_one(model, identifier):
    try:
        data = session.query(model).get(identifier)
        session.commit()

        return data
    except Exception as error:
        logger.error(error)
        session.rollback()

        return None


def delete(model, identifier):
    session = Session()

    try:
        data = session.query(model).get(identifier)
        session.delete(data)

        session.commit()
    except Exception as error:
        logger.error(error)
        session.rollback()
