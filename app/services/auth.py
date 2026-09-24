from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token, verify_password
from app.core.security import verify_password
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest


class AuthService:

    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def authenticate_user(self, data: LoginRequest):
        user = await self.user_repository.get_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(str(user.id))

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }