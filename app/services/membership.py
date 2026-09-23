from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.membership import MembershipRepository
from app.repositories.organization import OrganizationRepository
from app.repositories.user import UserRepository
from app.schemas.membership import MembershipCreate


class MembershipService:

    def __init__(self, db: AsyncSession):
        self.membership_repository = MembershipRepository(db)
        self.organization_repository = OrganizationRepository(db)
        self.user_repository = UserRepository(db)

    async def create_membership(self, data: MembershipCreate):
        organization = await self.organization_repository.get_by_id(
            data.organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        user = await self.user_repository.get_by_id(data.user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        existing = await self.membership_repository.get_existing(
            data.organization_id,
            data.user_id,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a member of this organization",
            )

        return await self.membership_repository.create(data)