import asyncio
import random
from faker import Faker
from src.database.db import session_manager
from src.database.models import Contact

fake = Faker()


def create_contacts():
    return [
        Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=45),
        )
        for _ in range(random.randint(10, 15))
    ]


async def seed():
    contacts = create_contacts()
    async with session_manager.session() as session:
        session.add_all(contacts)
        await session.commit()
    print("Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
