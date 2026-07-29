
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
from contextlib import contextmanager

from src.load.internal.config.database_configuration import DatabaseConfiguration, get_database_configuration

#@lru_cache
def get_engine():
    databaseConfiguration: DatabaseConfiguration = get_database_configuration()
    return create_engine(
        f"postgresql+psycopg2://{databaseConfiguration.username}:{databaseConfiguration.password}@{databaseConfiguration.host}:{databaseConfiguration.port}/{databaseConfiguration.database_name}",
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        isolation_level="READ COMMITTED",
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_startup_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()