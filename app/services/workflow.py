from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.workflow import WorkflowUpdate
from app.repositories.organization import OrganizationRepository
from app.repositories.workflow import WorkflowRepository
from app.schemas.workflow import WorkflowCreate


class WorkflowService:

    def __init__(self, db: AsyncSession):
        self.workflow_repository = WorkflowRepository(db)
        self.organization_repository = OrganizationRepository(db)

    async def create_workflow(
        self,
        organization_id,
        data: WorkflowCreate,
    ):
        organization = await self.organization_repository.get_by_id(
            organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        return await self.workflow_repository.create(
            organization_id,
            data,
        )

    async def get_organization_workflows(self, organization_id):
        return await self.workflow_repository.get_by_organization(
            organization_id
        )

    async def update_workflow(
        self,
        organization_id: UUID,
        workflow_id: UUID,
        data: WorkflowUpdate,
    ):
        workflow = await self.workflow_repository.get_by_id(workflow_id)

        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workflow not found",
            )

        if workflow.organization_id != organization_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workflow not found in this organization",
            )

        return await self.workflow_repository.update(
            workflow,
            data,
        )

    async def delete_workflow(
        self,
        organization_id: UUID,
        workflow_id: UUID,
    ):
        workflow = await self.workflow_repository.get_by_id(workflow_id)

        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workflow not found",
            )

        if workflow.organization_id != organization_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workflow not found in this organization",
            )

        await self.workflow_repository.delete(workflow)