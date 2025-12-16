from engine import engine
from entities import Address, Order, Product, User
from sqlalchemy.orm import sessionmaker

session_factory = sessionmaker(engine)

with session_factory() as session:
    users = session.query(User).all()
    addresses = session.query(Address).all()
    descriptions = [
        "Software engineer passionate about open-source projects and clean code.",
        "Digital marketer specializing in SEO and content strategy.",
        "Student at MIT studying Artificial Intelligence and Robotics.",
        "Freelance graphic designer with 5+ years of experience in branding.",
        "Coffee lover, traveler, and aspiring novelist.",
    ]

    for i in range(len(users)):
        users[i].description = descriptions[i]
    session.commit()

    products_data = [
        {"name": "Book", "price": 10.99},
        {"name": "Chair", "price": 15.25},
        {"name": "Clock", "price": 5.10},
        {"name": "Watch", "price": 25.99},
        {"name": "PlayStation", "price": 100},
    ]

    products = []
    for data in products_data:
        product = Product(**data)
        session.add(product)
        products.append(product)
    session.commit()

    for i in range(5):
        session.add(
            Order(
                user_id=users[i].id,
                address_id=addresses[i].id,
                product_id=products[i].id,
            )
        )
    session.commit()
