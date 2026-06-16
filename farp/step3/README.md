# Heroes API

A complete CRUD REST API for managing heroes, built with **FastAPI**, **SQLModel**, **Alembic**, and **PostgreSQL**, orchestrated with Docker Compose.

## Project layout

```
.
├── main.py                          # FastAPI application + SQLModel models
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # API container image
├── docker-compose.yml               # Orchestrates db → migrate → api
├── alembic.ini                      # Alembic config (URL read from env)
├── alembic/
│   ├── env.py                       # Wired to SQLModel metadata + DATABASE_URL
│   ├── script.py.mako               # Migration file template
│   └── versions/
│       └── fb17b1e5b937_create_hero_table.py   # Initial migration
├── .env.example                     # Copy to .env and set your secrets
└── .dockerignore
```

## Quick start

```bash
cp .env.example .env          # optionally change credentials

docker compose up --build
# 1. db       — Postgres starts and passes healthcheck
# 2. migrate  — runs `alembic upgrade head`, then exits 0
# 3. api      — uvicorn starts on :8000

# API:  http://localhost:8000
# Docs: http://localhost:8000/docs
```

## Services

| Service   | What it does | Exits? |
|-----------|-------------|--------|
| `db`      | Postgres 16 | no (restart: unless-stopped) |
| `migrate` | `alembic upgrade head` | yes (restart: no) |
| `api`     | `uvicorn main:app` | no (restart: unless-stopped) |

`api` waits for `migrate: service_completed_successfully`, so the schema is always up to date before the app serves traffic.

## Working with Alembic migrations

> All commands below require `DATABASE_URL` to be set (or use `docker compose run`).

### Generate a new migration after changing a model

```bash
# Option A — inside the running migrate container
docker compose run --rm migrate alembic revision --autogenerate -m "add_power_column"

# Option B — locally (with a venv and DATABASE_URL exported)
export DATABASE_URL=postgresql://heroes:heroespassword@localhost:5432/heroesdb
alembic revision --autogenerate -m "add_power_column"
```

Alembic diffs your SQLModel definitions against the live schema and writes a new file to `alembic/versions/`.

### Apply migrations

```bash
# Docker
docker compose run --rm migrate alembic upgrade head

# Local
alembic upgrade head
```

### Useful migration commands

```bash
alembic current          # which revision the DB is on
alembic history --verbose  # full migration history
alembic upgrade head     # apply all pending migrations
alembic downgrade -1     # roll back one migration
alembic downgrade base   # roll back everything
```

### Workflow for a schema change

1. Edit `main.py` — add/rename/remove a field on a SQLModel class.
2. Generate: `alembic revision --autogenerate -m "describe_the_change"`
3. Review the generated file in `alembic/versions/` — autogenerate is good but not perfect.
4. Commit both `main.py` and the new migration file.
5. Deploy: `docker compose up --build` runs `alembic upgrade head` automatically.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `heroes` | DB username |
| `POSTGRES_PASSWORD` | `heroespassword` | DB password |
| `POSTGRES_DB` | `heroesdb` | Database name |
| `DATABASE_URL` | *(built from above)* | Full DSN used by the API and Alembic |

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/heroes/` | Create a hero |
| `GET` | `/heroes/` | List heroes (`?offset=0&limit=20`) |
| `GET` | `/heroes/{id}` | Get one hero |
| `PATCH` | `/heroes/{id}` | Partial update |
| `DELETE` | `/heroes/{id}` | Delete a hero |

## Local development (without Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Uses SQLite fallback when DATABASE_URL is unset
export DATABASE_URL=sqlite:///database.db
alembic upgrade head
fastapi dev main.py
```

## Useful Docker commands

```bash
docker compose logs -f api          # tail API logs
docker compose exec db psql -U heroes -d heroesdb   # Postgres shell
docker compose down                 # stop (keeps volume)
docker compose down -v              # stop + wipe database
```
