import os
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    """The actual DB table."""
    id: int | None = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    """Payload accepted when creating a hero (no id)."""
    pass


class HeroRead(HeroBase):
    """Response model – always includes the id."""
    id: int


class HeroUpdate(SQLModel):
    """All fields optional for partial updates (PATCH semantics)."""
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///database.db",  # fallback for local dev without Docker
)

# SQLite needs check_same_thread=False; PostgreSQL does not (and rejects it).
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

# Schema is managed by Alembic (run via `alembic upgrade head` before startup).
# SQLModel.metadata.create_all() is intentionally NOT called here.
app = FastAPI(title="Heroes API", version="1.0.0")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.post("/heroes/", response_model=HeroRead, status_code=201, tags=["heroes"])
def create_hero(hero: HeroCreate, session: SessionDep) -> Hero:
    """Create a new hero."""
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroRead], tags=["heroes"])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 20,
) -> list[Hero]:
    """List all heroes with optional pagination."""
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroRead, tags=["heroes"])
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    """Get a single hero by ID."""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead, tags=["heroes"])
def update_hero(hero_id: int, hero_update: HeroUpdate, session: SessionDep) -> Hero:
    """Partially update a hero."""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    update_data = hero_update.model_dump(exclude_unset=True)
    hero.sqlmodel_update(update_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.delete("/heroes/{hero_id}", status_code=204, tags=["heroes"])
def delete_hero(hero_id: int, session: SessionDep) -> None:
    """Delete a hero."""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
