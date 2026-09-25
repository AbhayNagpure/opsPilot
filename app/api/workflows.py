from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.workflow import WorkflowCreate, WorkflowRead, WorkflowUpdate
from app.core.database import get_db
from app.core.dependencies import require_org_admin
from app.models.membership import OrganizationMembership
from app.schemas.workflow import WorkflowCreate, WorkflowRead
from app.services.workflow import WorkflowService


router = APIRouter(
    prefix="/organizations/{organization_id}/workflows",
    tags=["Workflows"],
)


@router.post(
    "/",
    response_model=WorkflowRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_workflow(
    organization_id: UUID,
    data: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
    membership: OrganizationMembership = Depends(require_org_admin),
):
    service = WorkflowService(db)

    return await service.create_workflow(
        organization_id,
        data,
    )

@router.get(
    "/",
    response_model=list[WorkflowRead],
)
async def get_workflows(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = WorkflowService(db)
    return await service.get_organization_workflows(
        organization_id
    )


@router.patch(
    "/{workflow_id}",
    response_model=WorkflowRead,
)
async def update_workflow(
    organization_id: UUID,
    workflow_id: UUID,
    data: WorkflowUpdate,
    db: AsyncSession = Depends(get_db),
    membership: OrganizationMembership = Depends(require_org_admin),
):
    service = WorkflowService(db)

    return await service.update_workflow(
        organization_id,
        workflow_id,
        data,
    )


@router.delete(
    "/{workflow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_workflow(
    organization_id: UUID,
    workflow_id: UUID,
    db: AsyncSession = Depends(get_db),
    membership: OrganizationMembership = Depends(require_org_admin),
):
    service = WorkflowService(db)

    await service.delete_workflow(
        organization_id,
        workflow_id,
    )