from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError

from utils.auth_utils import (
    authenticate_user,
    create_user,
    create_access_token,
)

from db import db_dependency
from schemas.auth_schemas import Token, UserRequest, UserResponse
from models.user_model import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/create-user", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserRequest, db: db_dependency):
    user = create_user(user.email, user.password, user.full_name, db)
    token = create_access_token(
        data={"sub": user.email, "id": user.id}
    )
    return token
