from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate
from uuid import UUID

class OrganizationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all(self) -> list[Organization]:
        result = await self.db.execute(
            select(Organization)
        )
        return list(result.scalars().all())

    async def get_by_id(self, organization_id: UUID) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(Organization.id == organization_id)
        )

        return result.scalar_one_or_none()
    
    async def get_by_slug(self, slug: str) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(Organization.slug == slug)
        )
        return result.scalar_one_or_none()

    async def create(self, data: OrganizationCreate) -> Organization:
        organization = Organization(
            name=data.name,
            slug=data.slug,
        )

        self.db.add(organization)
        await self.db.commit()
        await self.db.refresh(organization)

        return organization

    