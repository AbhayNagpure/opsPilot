from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.membership import MembershipCreate
from app.services.membership import MembershipService


router = APIRouter(
    prefix="/memberships",
    tags=["Memberships"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_membership(
    data: MembershipCreate,
    db: AsyncSession = Depends(get_db),
):
    service = MembershipService(db)
    return await service.create_membership(data)