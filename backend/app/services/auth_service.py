from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserRegister


class AuthError(Exception):
    """Raised on invalid credentials or duplicate registration."""


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def register(self, data: UserRegister) -> User:
        if await self.get_by_email(data.email):
            raise AuthError("Email already registered")

        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )
        self._db.add(user)
        await self._db.flush()
        return user

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise AuthError("Invalid credentials")
        if not user.is_active:
            raise AuthError("Inactive user")
        return user

    @staticmethod
    def issue_token(user: User) -> str:
        return create_access_token(subject=str(user.id))
