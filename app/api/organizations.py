from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import require_org_admin
from app.models.membership import OrganizationMembership
from uuid import UUID
from app.core.database import get_db
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
)
from app.services.organization import OrganizationService


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)   

@router.get("/", response_model=list[OrganizationRead])
async def get_organizations(
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    return await service.get_organizations()

@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    return await service.get_organization(organization_id)

@router.post(
    "/",
    response_model=OrganizationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    return await service.create_organization(data)

@router.get("/{organization_id}/admin-check")
async def admin_check(
    membership: OrganizationMembership = Depends(require_org_admin),
):
    return {
        "message": "Admin access granted",
        "role": membership.role,
    }