from sqlalchemy.orm import sessionmaker

from engine import engine
from entities import User, Address

session_factory = sessionmaker(engine)

with session_factory() as session:
    users_data = [
        {'username': 'John', 'email': 'john@example.com'},
        {'username': 'Dan', 'email': 'dan@example.com'},
        {'username': 'Ban', 'email': 'ban@exampl.com'},
        {'username': 'Steve', 'email': 'steve@example.com'},
        {'username': 'Robert', 'email': 'robert@example.com'}
    ]

    users = []
    for data in users_data:
        user = User(**data)
        users.append(user)
        session.add(user)

    session.commit()

    addresses_data = [
        {'user_id': users[0].id, 'street': '123 Maple Avenue', 'city': 'Portland', 'country': 'USA'},
        {'user_id': users[1].id, 'street': '456 Oak Street', 'city': 'Austin', 'country': 'USA'},
        {'user_id': users[2].id, 'street': '789 Elm Boulevard', 'city': 'Chicago', 'country': 'USA'},
        {'user_id': users[3].id, 'street': '321 Pine Road', 'city': 'Miami', 'country': 'USA'},
        {'user_id': users[4].id, 'street': '654 Cedar Lane', 'city': 'Denver', 'country': 'USA'},
    ]

    for address in addresses_data:
        session.add(Address(**address))

    session.commit()