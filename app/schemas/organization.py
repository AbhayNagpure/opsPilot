from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=120)


class OrganizationRead(BaseModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)