from sqlalchemy import create_engine
from src.load.internal.config.database_configuration import DatabaseConfiguration, get_database_configuration

databaseConfiguration: DatabaseConfiguration = get_database_configuration()
engine = create_engine(
    f"postgresql+psycopg2://{databaseConfiguration.username}:{databaseConfiguration.password}@{databaseConfiguration.host}:{databaseConfiguration.port}/{databaseConfiguration.database_name}"
)

with engine.connect() as conn:
    print("OK")