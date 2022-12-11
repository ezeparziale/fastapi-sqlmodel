# API with Fastapi + SQLModel

API using fastapi and sqlmodel

Features:

- [x] Fastapi
- [X] SQLModel
- [X] Postgres
- [X] Alembic

## :floppy_disk: Installation

```bash
python -m venv env
```

```bash
. env/scripts/activate
```

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

## :wrench: Config

Create `.env` file. Check the example `.env.example`

:construction: Before first run:

Run `docker-compose` :whale: to start the database server

```bash
docker compose -f "docker-compose.yml" up -d --build adminer db
```

and init the database with alembic:

```bash
alembic upgrade head
```

## :runner: Run

```bash
docker compose -f "docker-compose.yml" up -d --build adminer db
```

and

```bash
uvicorn app.main:app --reload --port 8000
```

or using `docker-compose` :whale: for run all services

```bash
docker compose -f "docker-compose.yml" up -d --build
```
