FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apk update \
    && apk add --no-cache postgresql-dev gcc musl-dev libffi-dev \
	&& pip3 install --no-cache-dir -r requirements.txt

EXPOSE 83 443

CMD python3 main.py
