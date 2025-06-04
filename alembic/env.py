# alembic/env.py
import os
import sys
from logging.config import fileConfig
from app.database.database import Base 
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import app.models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Add your project to the Python path ---
# This allows Alembic to find your 'app' module and its submodules
# Adjust the path if your alembic directory is not at the top level of your project root.
# Assuming 'alembic' folder is in your project root and 'app' is also there:
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# add your model's MetaData object here
# for 'autogenerate' support
from app.database.database import Base # <-- Import your Base from database.py

target_metadata = Base.metadata # <-- Set target_metadata to your Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url") # Reads from alembic.ini
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

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # This uses engine_from_config which reads the [alembic] section
    # of alembic.ini, including the sqlalchemy.url you set there.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}), # Gets [alembic] section
        prefix="sqlalchemy.", # Looks for sqlalchemy.url, sqlalchemy.pool_recycle, etc.
        poolclass=pool.NullPool, # Good for migration script that runs and exits
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