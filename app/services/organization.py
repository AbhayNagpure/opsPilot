from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.organization import OrganizationRepository
from app.schemas.organization import OrganizationCreate
from uuid import UUID

class OrganizationService:

    def __init__(self, db: AsyncSession):
        self.repository = OrganizationRepository(db)

    async def get_organizations(self):
        return await self.repository.get_all()

    async def get_organization(self, organization_id: UUID):
        organization = await self.repository.get_by_id(organization_id)

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        return organization

    async def create_organization(self, data: OrganizationCreate):
        existing_organization = await self.repository.get_by_slug(data.slug)

        if existing_organization:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization with this slug already exists",
            )

        return await self.repository.create(data)