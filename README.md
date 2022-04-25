## Homework for Pyforge course 
1. Clone the project

Prerequisites:
- Docker & Docker Compose;

## DEV mode
1. Run all services in Docker Compose.
```shell
$ docker-compose -f docker-compose.dev.yml up -d --build 
```
2. Create DB tables
```shell
$ docker-compose exec web python manage.py create_db
```
3. Seed DB data
```shell
$ docker-compose exec web python manage.py seed_db
```
4. Service will be available on
- `http://127.0.0.1:5000/`

## PROD mode
1. Update the entrypoint file permissions locally
```shell
$ chmod +x services/web/entrypoint.prod.sh
```
2. Run all services in Docker Compose
_(The database tables and data will be created automatically)_
```shell
$ docker-compose -f docker-compose.prod.yml up -d --build
```
3. Service will be available on
- `localhost:1337`

## Tests
1. Run all services in Docker Compose.
```shell
$ docker-compose -f docker-compose.test.yml up -d --build
```
2. Run tests
```shell
$ docker-compose exec web pytest
```
