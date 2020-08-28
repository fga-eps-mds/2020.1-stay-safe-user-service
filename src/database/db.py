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

        return "User created successfully!", 201
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400


def get_all(model):
    try:
        data = session.query(model).all()
        session.commit()

        return data, 200
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400


def get_one(model, identifier):
    try:
        data = session.query(model).get(identifier)
        session.commit()

        return data, 200
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 200


def delete(model, identifier):
    session = Session()

    try:
        data = session.query(model).get(identifier)
        session.delete(data)
        session.commit()

        return "User deleted successfully!", 200
    except Exception as error:
        logger.error(error)
        session.rollback()

        return "User not found!", 404
