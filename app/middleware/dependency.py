from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.model import database,models
from sqlalchemy.future import select
from . import auth
# from app.model import database
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    async with database.SessionLocal() as session:
        yield session

async def get_user(db: AsyncSession, username: str):
    query = select(models.User).filter(models.User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_current_user(token: str = Depends(oauth_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = auth.decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = await get_user(db, username)
    if user is None:
        raise credentials_exception
    return user