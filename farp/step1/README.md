# Heroes API

A complete CRUD REST API for managing heroes, built with **FastAPI** and **SQLModel**.

## Features

- Full CRUD: Create, Read (list + single), Update (partial PATCH), Delete
- SQLite database via SQLModel / SQLAlchemy
- Separate request / response models (no id leakage on create)
- Session-per-request via FastAPI dependency injection
- Pagination with `offset` & `limit`
- Auto-generated interactive docs at `/docs`

## Models

| Model        | Purpose                              |
|-------------|--------------------------------------|
| `Hero`       | DB table (id, name, secret_name, age)|
| `HeroCreate` | Request body for POST (no id)        |
| `HeroRead`   | Response body (always has id)        |
| `HeroUpdate` | Partial update body (all optional)   |

## Setup

```bash
# 1. Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run in development mode (auto-reload)
fastapi dev main.py
```

The API will be available at **http://127.0.0.1:8000**.  
Interactive docs: **http://127.0.0.1:8000/docs**

## Endpoints

| Method   | Path               | Description          |
|----------|--------------------|----------------------|
| `POST`   | `/heroes/`         | Create a hero        |
| `GET`    | `/heroes/`         | List heroes (paged)  |
| `GET`    | `/heroes/{id}`     | Get one hero         |
| `PATCH`  | `/heroes/{id}`     | Partially update     |
| `DELETE` | `/heroes/{id}`     | Delete a hero        |

### Example request

```bash
curl -X POST http://localhost:8000/heroes/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Deadpond", "secret_name": "Dive Wilson"}'
```

### Pagination

```
GET /heroes/?offset=0&limit=10
```
