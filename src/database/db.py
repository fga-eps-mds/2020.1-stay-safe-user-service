import os

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from settings import logger

from datetime import datetime


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


def get_all(model, filter=None):
    try:
        query = session.query(model)
        if str(model.__table__) == "occurrence_stay_safe":
            past_date = datetime.utcnow()\
                           .replace(year=datetime.utcnow().year - 1)
            filter_ = and_(model.occurrence_date_time >= past_date,
                           model.occurrence_date_time <= datetime.utcnow())
            query = query.filter(filter_)
        if filter:
            for attr, value in list(filter.items()):
                if not hasattr(model, attr):
                    return "The object does not have the attribute\
                            passed on query param", 400
                else:
                    filter_ = getattr(model, attr).in_(value)
                query = query.filter(filter_)
        data = query.all()
        return data, 200
    except Exception as error:
        logger.error(error)
        session.rollback()
        return str(error), 400


def get_one(model, identifier):
    try:
        data = session.query(model).get(identifier)

        if data:
            return data, 200

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400


def update(model, identifier, params, username=None):
    try:
        data = session.query(model).get(identifier)
        session.commit()

        if data:
            if username:
                if not getattr(data, 'user') == username:
                    return f"You cannot edit another\
                           user's {model.__name__}", 403

            for param in params:
                setattr(data, param, params[param])
            session.commit()
            return data, 200

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400


def delete(model, identifier, username=None):
    try:
        data = session.query(model).get(identifier)

        if data:
            if username:
                if not getattr(data, 'user') == username:
                    return f"You cannot delete another\
                           user's {model.__name__}", 403

            session.delete(data)
            session.commit()
            return "Deleted successfully!", 204

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return str(error), 400
