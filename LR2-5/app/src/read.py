from entities import User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import selectinload, sessionmaker

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5433/test_migrations", echo=False
)

session_factory = sessionmaker(engine)

with session_factory() as session:
    statement = select(User).options(selectinload(User.addresses))
    result = session.scalars(statement).all()

    for user in result:
        for address in user.addresses:
            print(
                f"Пользователь: {user.username}; Email: {user.email}; Адрес: {address.street}, {address.city}, {address.country}"
            )
