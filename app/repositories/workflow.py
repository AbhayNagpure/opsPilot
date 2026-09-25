from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate


class WorkflowRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        organization_id,
        data: WorkflowCreate,
    ) -> Workflow:
        workflow = Workflow(
            organization_id=organization_id,
            name=data.name,
            description=data.description,
        )

        self.db.add(workflow)
        await self.db.commit()
        await self.db.refresh(workflow)

        return workflow

    async def get_by_organization(
        self,
        organization_id,
    ) -> list[Workflow]:

        result = await self.db.execute(
            select(Workflow).where(
                Workflow.organization_id == organization_id
            )
        )

        return list(result.scalars().all())

    async def get_by_id(self, workflow_id: UUID) -> Workflow | None:
        result = await self.db.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        return result.scalar_one_or_none()


    async def update(
        self,
        workflow: Workflow,
        data,
    ) -> Workflow:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(workflow, field, value)

        await self.db.commit()
        await self.db.refresh(workflow)

        return workflow

    async def delete(self, workflow: Workflow) -> None:
        await self.db.delete(workflow)
        await self.db.commit()