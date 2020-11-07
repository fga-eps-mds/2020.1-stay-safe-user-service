<a href="https://codeclimate.com/github/fga-eps-mds/2020.1-stay-safe-user-service/maintainability"><img src="https://api.codeclimate.com/v1/badges/25f410acd5cf3449085e/maintainability" /></a>
# User Service
User service of Stay Safe project

## Run

### Flask

#### Build

```bash
$ docker-compose build
```

#### Run api

```bash
$ docker-compose up
```

### Pylint

```bash
$ docker-compose run api sh -c "pylint **/*.py"
```

### Pytest / Coverage

#### To run tests

```bash
$ docker-compose run api coverage run -m pytest
```

### Run Sonarqube
```bash
$ docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest
$ docker run -ti -v $(pwd):/usr/src --link sonarqube newtmitch/sonar-scanner -Dsonar.projectName="User Service" -Dsonar.projectKey=userservice
```
Link to see the scans projects: http://localhost:9000/projects

#### To report results with Coverage

```bash
$ docker-compose run api coverage report -m
```

#### To add neighborhoods to database

```bash
$ sudo docker-compose run api sh -c "python3 ./static/save_on_db.py"
```
