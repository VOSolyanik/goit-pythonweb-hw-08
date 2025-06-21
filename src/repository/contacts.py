from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, or_, extract
from datetime import date, timedelta

from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate, ContactListResponse


class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_contacts_list(
        self,
        skip: int = 0,
        limit: int = 100,
        search_text: Optional[str] = None,
        upcoming_birthdays: Optional[bool] = None,
    ) -> ContactListResponse:
        base_query = select(Contact)
        count_query = select(func.count(Contact.id))
        filters = []

        if search_text:
            filters.append(self._get_search_filter(search_text))

        if upcoming_birthdays:
            filters.append(self._get_upcoming_birthdays_filter())

        if filters:
            base_query = base_query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))

        count_result = await self.db.execute(count_query)
        total_count = count_result.scalar() or 0

        query = base_query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        contacts = result.scalars().all()

        return ContactListResponse(items=contacts, total_count=total_count)

    def _get_search_filter(self, search_text: str):
        return or_(
            func.lower(Contact.first_name).like(f"%{search_text}%"),
            func.lower(Contact.last_name).like(f"%{search_text}%"),
            func.lower(Contact.email).like(f"%{search_text}%"),
        )

    def _get_upcoming_birthdays_filter(self):
        today = date.today()
        future_date = today + timedelta(days=7)
        return and_(
            and_(
                extract("month", Contact.birth_date) == today.month,
                extract("day", Contact.birth_date) >= today.day,
            ),
            and_(
                extract("month", Contact.birth_date) == future_date.month,
                extract("day", Contact.birth_date) <= future_date.day,
            ),
        )

    async def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, body: ContactCreate) -> Contact:
        new_contact = Contact(**body.model_dump())

        self.db.add(new_contact)
        try:
            await self.db.commit()
            await self.db.refresh(new_contact)
            return new_contact
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=400, detail="Contact with this email already exists"
            ) from e

    async def update_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)

        if contact:
            for key, value in body.dict(exclude_unset=True).items():
                setattr(contact, key, value)

            try:
                await self.db.commit()
                await self.db.refresh(contact)
                return contact
            except IntegrityError as e:
                await self.db.rollback()
                raise HTTPException(
                    status_code=400, detail="Contact with this email already exists"
                ) from e
        return contact

    async def remove_contact(self, contact_id: int) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)

        if contact:
            await self.db.delete(contact)
            await self.db.commit()

        return contact
