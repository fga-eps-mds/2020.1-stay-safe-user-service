from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

from settings import logger


db_url = os.environ.get("SQLALCHEMY_DB_URL")
db = create_engine(db_url)

Session = sessionmaker(db)
session = Session()


def insert_one(element):
    try:
        session.add(element)
        session.commit()

        return "Created successfully!", 201
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400


def get_all(model, identifier = None):
    try:
        if(identifier):
            data = session.query(model).filter(model.user == identifier)
            session.commit()
            return data, 200
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

        if data:
            return data, 200

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400


def update(model, identifier, params):
    try:
        data = session.query(model).get(identifier)
        session.commit()

        if data:
            for param in params:
                setattr(data, param, params[param])
            session.commit()
            return data, 200

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400


def delete(model, identifier):
    session = Session()

    try:
        data = session.query(model).get(identifier)

        if data:
            session.delete(data)
            session.commit()
            return "Deleted successfully!", 204

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400
