# Heroes API

A complete CRUD REST API for managing heroes, built with **FastAPI** and **SQLModel**, running on **PostgreSQL** inside Docker.

## Project layout

```
.
├── main.py             # FastAPI application
├── requirements.txt    # Python dependencies
├── Dockerfile          # API container image
├── docker-compose.yml  # Orchestrates api + db services
├── .env.example        # Copy to .env and set your secrets
└── .dockerignore
```

## Quick start

```bash
# 1. Copy and (optionally) edit credentials
cp .env.example .env

# 2. Build and start both services
docker compose up --build

# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

To run in the background:

```bash
docker compose up --build -d
```

## Services

| Service | Image | Port |
|---------|-------|------|
| `api`   | built from `./Dockerfile` | `8000` |
| `db`    | `postgres:16-alpine`      | `5432` |

The `api` service waits for the `db` healthcheck to pass before starting, so tables are created automatically on first boot.

## Environment variables

All variables have safe defaults in `docker-compose.yml` but can be overridden via `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `heroes` | DB username |
| `POSTGRES_PASSWORD` | `heroespassword` | DB password |
| `POSTGRES_DB` | `heroesdb` | Database name |
| `DATABASE_URL` | *(built from above)* | Full DSN passed to the API |

`DATABASE_URL` is constructed automatically in `docker-compose.yml` from the Postgres variables. You can also override it directly if you point the API at an external database.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/heroes/` | Create a hero |
| `GET` | `/heroes/` | List heroes (`?offset=0&limit=20`) |
| `GET` | `/heroes/{id}` | Get one hero |
| `PATCH` | `/heroes/{id}` | Partial update |
| `DELETE` | `/heroes/{id}` | Delete a hero |

### Example

```bash
curl -X POST http://localhost:8000/heroes/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Deadpond", "secret_name": "Dive Wilson"}'
```

## Local development (without Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Uses SQLite fallback automatically when DATABASE_URL is not set
fastapi dev main.py
```

## Useful commands

```bash
# View logs
docker compose logs -f api

# Connect to Postgres directly
docker compose exec db psql -U heroes -d heroesdb

# Stop and remove containers (keeps the volume)
docker compose down

# Stop and wipe the database volume
docker compose down -v
```
