from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password

class UserService:

    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, data: UserCreate):
        existing_user = await self.repository.get_by_email(data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        hashed_password = hash_password(data.password)

        return await self.repository.create(
            data,
            hashed_password,
        )

 