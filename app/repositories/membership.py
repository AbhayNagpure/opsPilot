from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.membership import OrganizationMembership
from app.schemas.membership import MembershipCreate


class MembershipRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_existing(
        self,
        organization_id,
        user_id,
    ):
        result = await self.db.execute(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        data: MembershipCreate,
    ) -> OrganizationMembership:

        membership = OrganizationMembership(
            organization_id=data.organization_id,
            user_id=data.user_id,
            role=data.role,
        )

        self.db.add(membership)
        await self.db.commit()
        await self.db.refresh(membership)

        return membership