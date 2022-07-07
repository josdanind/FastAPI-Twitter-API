from decouple import config

# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


user = config('DB_USER')
password = config('DB_PASS')
host = config('DB_HOST')
port = config('DB_PORT')
db_name = config('DB_NAME')

DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

engine = create_engine(DATABASE_URL)

# Cada instancia de SessionLocal sera una sesion de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
