from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://postgres:postgres@localhost:5433/test_migrations',
    echo=True
)