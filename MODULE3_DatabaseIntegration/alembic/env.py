import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# 1. Environment and Path Bootstrapping
load_dotenv()

# Appends current execution path context so Python cleanly finds your local modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

# Import your Base catalog registry target (task 1:94)
from Hands_on_6.orm.models import Base

# 2. Extract Configuration Frameworks
config = context.config

# Programmatically inject the hidden .env URL directly into the active Alembic engine config
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set up your metadata target catalog tracking layout
target_metadata = Base.metadata

# ==============================================================================
# MIGRATION EXECUTION MODES
# ==============================================================================

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    Emits raw SQL scripts to stdout instead of accessing a live server.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    Creates an engine connection pool and targets a live database.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()