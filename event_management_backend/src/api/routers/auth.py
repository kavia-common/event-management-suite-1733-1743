from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.future import select
from .. import models, schemas, utils
from ..database import get_async_session

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependency to get current user from JWT token
# PUBLIC_INTERFACE
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
    user_id = utils.decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/register", response_model=schemas.UserOut, summary="Register a new user")
async def register(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(models.User).where(models.User.email == user_in.email))
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed = utils.hash_password(user_in.password)
    new_user = models.User(
        email=user_in.email,
        hashed_password=hashed,
        full_name=user_in.full_name,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token, summary="Login for access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(models.User).where(models.User.email == form_data.username))
    user = result.scalars().first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = utils.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut, summary="Get current user")
async def me(current_user: models.User = Depends(get_current_user)):
    return current_user
