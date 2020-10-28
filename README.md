# 2020.1-stay-safe-user-service

User service of Stay Safe project

## Run

### Flask

#### Build

```bash
$ sudo docker-compose build
```

#### Run api

```bash
$ sudo docker-compose up
```

### Pylint

```bash
$ sudo docker-compose run api sh -c "pylint **/*.py"
```

### Pytest / Coverage

#### To run tests

```bash
$ sudo docker-compose run api coverage run -m pytest
```

#### To report results with Coverage

```bash
$ sudo docker-compose run api coverage report -m
```

#### To add neighborhoods to database

```bash
$ sudo docker-compose run api sh -c "python3 ./static/save_on_db.py"
```
