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

        return "Created successfully!", 201
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

        return str(error), 404

# def update(model, identifier, params):
#     try:
#         data = session.query(model).get(identifier)
#         for param in params:
#             data = {**data, param: params[param]}
#             # data.full_name = "Saraaaa Magalhaes"

#         session.commit()
        
#         return [], 200

#     except Exception as error:
#         logger.error(error)
#         session.rollback()

#         return str(error), 400

def delete(model, identifier):
    session = Session()

    try:
        data = session.query(model).get(identifier)
        session.delete(data)
        session.commit()
        return "Deleted successfully!", 204
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 404
