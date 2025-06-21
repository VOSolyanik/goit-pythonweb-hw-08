from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict


# Base Contact model with common fields
class ContactBase(BaseModel):
    first_name: str = Field(
        min_length=1, max_length=50, description="First name of the contact"
    )
    last_name: str = Field(
        min_length=1, max_length=50, description="Last name of the contact"
    )
    email: EmailStr = Field(description="Email address of the contact")
    phone: str = Field(
        min_length=1, max_length=20, description="Phone number of the contact"
    )
    birth_date: date = Field(description="Birth date of the contact")
    notes: Optional[str] = Field(
        None, max_length=150, description="Additional notes about the contact"
    )


# Model for creating a new contact
class ContactCreate(ContactBase):
    pass


# Model for updating an existing contact
class ContactUpdate(ContactBase):
    pass


# Model for the response
class ContactResponse(ContactBase):
    id: int
    created_at: datetime | None
    updated_at: Optional[datetime] | None
    model_config = ConfigDict(from_attributes=True)


class ContactListResponse(BaseModel):
    total_count: int
    items: List[ContactResponse]
    model_config = ConfigDict(from_attributes=True)
