from uuid import UUID

from pydantic import BaseModel


class MembershipCreate(BaseModel):
    organization_id: UUID
    user_id: UUID
    role: str = "member"