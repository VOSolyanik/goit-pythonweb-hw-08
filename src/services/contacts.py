from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repo = ContactRepository(db)

    async def get_contacts_list(
        self,
        skip: int = 0,
        limit: int = 100,
        search_text: Optional[str] = None,
        upcoming_birthdays: Optional[bool] = None,
    ):
        return await self.repo.get_contacts_list(
            skip, limit, search_text, upcoming_birthdays
        )

    async def get_contact(self, contact_id: int):
        contact = await self.repo.get_contact_by_id(contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact

    async def create_contact(self, body: ContactCreate):
        return await self.repo.create_contact(body)

    async def update_contact(self, contact_id: int, body: ContactUpdate):
        contact = await self.repo.update_contact(contact_id, body)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact

    async def remove_contact(self, contact_id: int):
        contact = await self.repo.remove_contact(contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
