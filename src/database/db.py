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

        return "Criação bem-sucedida", 201
    except Exception as error:
        logger.error(error)
        session.rollback()

        if "UniqueViolation" in str(error._message):
            if "pkey" in str(error._message):
                return "Este nome de usuário já está sendo utilizado", 400
            elif "mail" in str(error._message):
                return "Este e-mail já está sendo utilizado", 400

        return "Algo deu errado, tente novamente mais tarde", 400


def get_all(model, filters_=None):
    try:
        query = session.query(model)
        if str(model.__table__) == "occurrence_stay_safe":
            past_date = datetime.utcnow()\
                .replace(year=datetime.utcnow().year - 1)
            filter_ = and_(model.occurrence_date_time >= past_date,
                           model.occurrence_date_time <= datetime.utcnow())
            query = query.filter(filter_)
        if filters_:
            for attr, value in list(filters_.items()):
                if not hasattr(model, attr):
                    return "O objeto não possui o atributo passado como parâmetro", 400
                else:
                    filters_ = getattr(model, attr).in_(value)
                query = query.filter(filters_)
        data = query.all()
        return data, 200
    except Exception as error:
        logger.error(error)
        session.rollback()
        return "Algo deu errado, tente novamente mais tarde", 400


def get_one(model, identifier):
    try:
        data = session.query(model).get(identifier)

        if data:
            return data, 200

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return "Algo deu errado, tente novamente mais tarde", 400


def update(model, identifier, params, username=None):
    try:
        data = session.query(model).get(identifier)
        session.commit()

        if data:
            if username:
                if not getattr(data, 'user') == username:
                    return f"Você não pode editar o objeto de outro usuário", 403

            for param in params:
                setattr(data, param, params[param])
            session.commit()
            return data, 200

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return "Algo deu errado, tente novamente mais tarde", 400


def delete(model, identifier, username=None):
    try:
        data = session.query(model).get(identifier)

        if data:
            if username:
                if not getattr(data, 'user') == username:
                    return f"Você não pode deletar o objeto de outro usuário", 403

            session.delete(data)
            session.commit()
            return "Deleção bem-sucedida", 204

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return "Algo deu errado, tente novamente mais tarde", 400
