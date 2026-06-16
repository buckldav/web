import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Import SQLModel metadata + all models so autogenerate can see the tables.
from sqlmodel import SQLModel
import main  # noqa: F401 – registers Hero (and any future models) with SQLModel.metadata

# ---------------------------------------------------------------------------
# Alembic Config
# ---------------------------------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Point autogenerate at SQLModel's shared metadata.
target_metadata = SQLModel.metadata


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_url() -> str:
    """Read the database URL from the environment (set in docker-compose or .env)."""
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Export it before running alembic, or use docker compose."
        )
    return url


# ---------------------------------------------------------------------------
# Migration runners
# ---------------------------------------------------------------------------

def run_migrations_offline() -> None:
    """Emit SQL to stdout without a live DB connection (useful for review/CI)."""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Connect to the DB and apply migrations directly."""
    cfg = config.get_section(config.config_ini_section, {})
    cfg["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        cfg,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,       # detect column type changes
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
