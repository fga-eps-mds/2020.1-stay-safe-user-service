# 2020.1-stay-safe-user-service
User service of Stay Safe project

## Run

### Flask
```bash
$ sudo docker-compose up
```

### Pylint
```bash
$ sudo docker-compose run api sh -c "pylint **/*.py"
```

### Pytest
```bash
$ sudo docker-compose run api pytest
```
